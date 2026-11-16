"""Parser for the CD-S300 front-panel VFD bus, as seen by the Pico's sniffer (display.py).

The protocol comes from the logic-analyzer capture captures/02-tocando.lac (docs/descobertas-protocolo.md):

- One frame per command: /CS low, a command byte, then its data bytes, LSB first, data valid on the rising clock.
- The command's high nibble is the command, the low nibble an address (Princeton PT6302-style controller):
    0x1n  write characters to the display RAM, starting at position n (positions 0-11 are the 12 characters,
          12 and 13 the two icon grids)
    0x2n  write custom characters, starting at custom character n, 5 bytes each (the icon grids show custom
          characters 0 and 1, so their bits are the icons)
    0x3n  (not seen yet) write the additional-data RAM
    other configuration (0x50 brightness?, 0x63, 0x70); kept raw
- The microcontroller rewrites everything every ~38 ms.

The sniffer hands over 32-bit words: MARKER when /CS falls (a frame begins), otherwise a data byte in bits 24-31.

Runs the same in MicroPython (Pico) and CPython (tools/test_vfd.py).
"""

MARKER = 0xFFFFFFFF
TEXT_LEN = 12
ICON_POS = (12, 13)
RAM_LEN = 16
CHANGES_KEPT = 32


def byte_of(word):
    """The data byte of a sniffer word, or None for a frame marker or a malformed word."""
    if word == MARKER or word & 0xFFFFFF:
        return None
    return word >> 24


class Screen:
    """The display's contents, rebuilt from the frames the microcontroller sends to the glass."""

    def __init__(self):
        self.ram = bytearray(b" " * RAM_LEN)        # display RAM: character codes per position
        self.custom = {}                            # custom character number -> 5 bytes
        self.config = {}                            # command byte -> data bytes (hex), for unknown commands
        self.frames = 0
        self.bad = 0                                # words that were neither a marker nor a byte
        self.changes = []                           # [(ms, text, icons hex)], newest last
        self._frame = None
        self._last = (self.text(), self.icons().hex())     # a blank screen is not a change

    # ---------------------------------------------------------------- input

    def feed(self, word, now_ms=0):
        """One word from the sniffer. Returns True when what the display shows changed."""
        if word == MARKER:
            return self._close(now_ms)
        b = byte_of(word)
        if b is None:
            self.bad += 1
            return False
        if self._frame is not None:
            self._frame.append(b)
        return False

    def flush(self, now_ms=0):
        """Closes the frame in progress (the last one stays open until the next marker)."""
        return self._close(now_ms, reopen=False)

    def _close(self, now_ms, reopen=True):
        frame, self._frame = self._frame, (bytearray() if reopen else None)
        if not frame:
            return False
        self.frames += 1
        self._apply(frame)
        return self._note(now_ms)

    def _apply(self, frame):
        cmd, data = frame[0], frame[1:]
        kind, addr = cmd & 0xF0, cmd & 0x0F
        if kind == 0x10:
            for i, c in enumerate(data):
                self.ram[(addr + i) % RAM_LEN] = c
        elif kind == 0x20:
            for i in range(len(data) // 5):
                self.custom[(addr + i) & 0x0F] = bytes(data[5 * i:5 * i + 5])
        else:
            self.config["%02X" % cmd] = bytes(data).hex()

    # ---------------------------------------------------------------- output

    def text(self):
        return "".join(chr(c) if 32 <= c < 127 else "?" for c in self.ram[:TEXT_LEN])

    def icons(self):
        """The 10 bytes behind the two icon grids (5 per grid)."""
        out = b""
        for pos in ICON_POS:
            out += self.custom.get(self.ram[pos], b"\x00" * 5) if self.ram[pos] < 16 else b"\x00" * 5
        return out

    def lit(self):
        """The lit icon dots as "grid.byte.bit" strings, e.g. "13.0.3": the names for the icon map."""
        out = []
        for i, b in enumerate(self.icons()):
            for bit in range(8):
                if b >> bit & 1:
                    out.append("%d.%d.%d" % (ICON_POS[i // 5], i % 5, bit))
        return out

    def _note(self, now_ms):
        now = (self.text(), self.icons().hex())
        if now == self._last:
            return False
        self._last = now
        self.changes.append((now_ms, now[0], now[1]))
        if len(self.changes) > CHANGES_KEPT:
            self.changes.pop(0)
        return True

    def debug(self):
        """GET /display: everything known, for mapping the icons and checking the reader."""
        return {"text": self.text(), "icons": self.icons().hex(), "lit": self.lit(),
                "ram": bytes(self.ram).hex(), "custom": {str(k): v.hex() for k, v in self.custom.items()},
                "config": self.config, "frames": self.frames, "bad": self.bad,
                "changes": [{"ms": ms, "text": t, "icons": i} for ms, t, i in self.changes]}
