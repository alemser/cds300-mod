#!/usr/bin/env python3
"""Confere o tools/fl_decode.py com uma captura inventada: um quadro de display e uma tecla NEC.

    python3 tools/test_fl_decode.py

A captura é montada aqui, no formato do .lac, e apagada no fim. Não substitui as capturas reais: só garante que o
decodificador corta os quadros, lê os bits na borda certa e decodifica o NEC do jeito que o firmware/ir_codes.py manda.
"""

import base64
import contextlib
import io
import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "firmware"))

import fl_decode    # noqa: E402
import ir_codes     # noqa: E402

FREQ = 2_000_000                # 0,5 µs por amostra
failures = []


def check(cond, msg):
    if not cond:
        failures.append(msg)
        print("FALHOU:", msg)


def display_signals(payload_frames, half=4, gap=40):
    """/CS, CLK e DATA: relógio parado em 1, dado trocado com o relógio em 0 e lido na subida, bit menos significativo
    primeiro. half = amostras por meio período."""
    cs, clk, data = [1] * 20, [1] * 20, [0] * 20
    for frame in payload_frames:
        cs += [0] * half
        clk += [1] * half
        data += [data[-1]] * half
        for byte in frame:
            for j in range(8):
                bit = byte >> j & 1
                cs += [0] * (2 * half)
                clk += [0] * half + [1] * half
                data += [data[-1]] * (half // 2) + [bit] * (2 * half - half // 2)   # troca no meio da parte baixa
        cs += [0] * half + [1] * gap
        clk += [1] * (half + gap)
        data += [data[-1]] * (half + gap)
    return cs, clk, data


def nec_signal(key, lead_us=2000):
    rem = [1] * int(lead_us * FREQ / 1e6)
    for i, us in enumerate(ir_codes.frame(key)):
        rem += [0 if i % 2 == 0 else 1] * int(us * FREQ / 1e6)
    return rem


def write_lac(path, signals):
    n = max(len(s) for s in signals.values())
    chans = []
    for num, (name, s) in enumerate(signals.items()):
        s = s + [s[-1]] * (n - len(s))
        chans.append({"ChannelNumber": num, "ChannelName": name, "Samples": base64.b64encode(bytes(s)).decode()})
    with open(path, "w") as f:
        json.dump({"Settings": {"Frequency": FREQ, "PreTriggerSamples": 0, "PostTriggerSamples": n,
                                "CaptureChannels": chans}}, f)


def main():
    sent = [[0x40], [0xC0, 0x12, 0xA5, 0xFF], [0x8F]]
    cs, clk, data = display_signals(sent)
    rst = [1] * len(cs)
    rst[5:25] = [0] * 20
    rem = nec_signal("play")

    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "fake.lac")
        write_lac(path, {"FL_/CS": cs, "FL_CLK": clk, "FL_DATA": data, "FL_/RST": rst, "REM": rem})
        freq, sig = fl_decode.load_lac(path)
        check(freq == FREQ and set(sig) == {"CS", "CLK", "DATA", "RST", "REM"}, f"sinais pelo nome: {sorted(sig)}")

        frs = fl_decode.frames(sig["CS"], sig["CLK"], sig["DATA"])
        check([len(f["bits"]) for f in frs] == [8, 32, 8], f"bits por quadro: {[len(f['bits']) for f in frs]}")
        got = [fl_decode.to_bytes(f["bits"], msb_first=False) for f in frs]
        check(got == sent, f"bytes LSB primeiro: {got}")
        msb = fl_decode.to_bytes(frs[0]["bits"], msb_first=True)
        check(msb == [0x02], f"0x40 lido com o MSB primeiro vira 0x02: {msb}")

        wrong = [fl_decode.to_bytes(f["bits"], False) for f in fl_decode.frames(sig["CS"], sig["CLK"], sig["DATA"],
                                                                                 "falling")]
        check(wrong != sent, "na borda errada os bytes não podem sair iguais")

        high, low, _ = fl_decode.clock_stats(sig["CLK"], sig["CS"], freq)
        check(high == 2.0 and low == 2.0, f"relógio de 2 µs alto e 2 µs baixo: {high}, {low}")
        check(len(fl_decode.groups(frs, freq)) == 1, "três quadros com 20 µs entre eles são um grupo só")

        rp = fl_decode.pulses_low(sig["RST"], freq)
        check(len(rp) == 1 and rp[0][1] == 10.0, f"/RST: um pulso de 10 µs: {rp}")

        keys = fl_decode.nec(sig["REM"], freq)
        check(len(keys) == 1 and keys[0]["key"] == "play" and keys[0]["bytes"] == [0x79, 0x86, 0x02, 0xFD],
              f"NEC: {keys}")

        with contextlib.redirect_stdout(io.StringIO()) as out:
            fl_decode.report(path, show_bits=True)
        text = out.getvalue()
        check("LSB: C0 12 A5 FF" in text and "79 86 02 FD  play" in text, "relatório:\n" + text)

    print("tudo certo" if not failures else f"{len(failures)} falha(s)")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
