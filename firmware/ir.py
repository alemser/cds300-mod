"""Manda as teclas do controle remoto ao CD-S300 pela linha do IR, por fio.

Ligação prevista (ainda não feita nem testada no aparelho; docs/plano.md):

    GP15 = saída do receptor de IR (U701), antes da porta IC702

Não serve a via REM do cabo flat: ela sai de uma porta lógica que a empurra para 3,3 V, e o Pico brigaria com ela
(docs/pesquisa.md, "O receptor").

REGRA DE SEGURANÇA (a mesma do SP103): o GP15 NUNCA vai a 1. O valor de saída fica em 0 e só a direção muda, na força
mínima (2 mA). A linha sobe pelo resistor de dentro do receptor.

O PIO só segura a linha em 0 durante um tempo já contado. Enquanto espera o próximo tempo, ela fica solta: se o DMA
parar no meio, a linha não fica presa em 0 e o controle remoto segue ativo. O DMA entrega os tempos sozinho, então
uma pausa do Python não estraga o código enviado.

O PIO e o DMA vêm do ir.py do sp103-display-proxy, onde funcionam no amp desde 2026-11-06.

Sem o fio ligado, mandar uma tecla não faz mal: o pino fica solto e nada o lê.
"""

import time
from array import array

import rp2
from machine import Pin, mem32

import ir_codes

IR_PIN = 15
_PADS_BANK0 = 0x40038000
_DRIVE_MASK = 0x3 << 4
_PIO_BASE = (0x50200000, 0x50300000, 0x50400000)
_TXF0 = 0x010                   # fila de entrada (TX) da máquina 0; as outras seguem de 4 em 4
_DREQ_PIO_TX0 = (0, 8, 16)      # pedido de DMA "a fila TX tem espaço"


@rp2.asm_pio(set_init=rp2.PIO.IN_LOW)
def _pulses():
    # A 1 MHz: cada volta do jmp dura 1 µs. Cada par de palavras: linha em 0, linha solta.
    pull()
    mov(x, osr)
    set(pindirs, 1)             # linha em 0
    label("mark")
    jmp(x_dec, "mark")
    set(pindirs, 0)             # solta a linha antes de esperar a próxima palavra
    pull()
    mov(x, osr)
    label("space")
    jmp(x_dec, "space")


class Remote:
    def __init__(self, sm_id=0):
        self.line = Pin(IR_PIN, Pin.IN, pull=None)
        self.sm = rp2.StateMachine(sm_id, _pulses, freq=1_000_000, set_base=Pin(IR_PIN))
        self.sm.exec("set(pins, 0)")
        self.sm.exec("set(pindirs, 0)")
        pad = _PADS_BANK0 + 4 + 4 * IR_PIN
        mem32[pad] = mem32[pad] & ~_DRIVE_MASK & ~1     # 2 mA, borda lenta
        self.sm.active(1)
        pio, sm = divmod(sm_id, 4)
        self._fifo = _PIO_BASE[pio] + _TXF0 + 4 * sm
        self.dma = rp2.DMA()
        self._ctrl = self.dma.pack_ctrl(size=2, inc_read=True, inc_write=False,
                                        treq_sel=_DREQ_PIO_TX0[pio] + sm)
        self._words = None              # o DMA lê daqui: não pode sumir durante o envio
        self._until = time.ticks_ms()
        self.sent = 0

    def sending(self):
        return time.ticks_diff(self._until, time.ticks_ms()) > 0

    def send(self, key):
        words = ir_codes.frame(key)
        self._words = array("I", words)
        self._until = time.ticks_add(time.ticks_ms(), sum(words) // 1000 + 10)
        self.dma.config(read=self._words, write=self._fifo, count=len(words), ctrl=self._ctrl, trigger=True)
        self.sent += 1

    def status(self):
        return {"commands": list(ir_codes.KEYS), "sending": self.sending(), "sent": self.sent,
                "line": self.line.value()}
