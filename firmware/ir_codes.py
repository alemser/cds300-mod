"""Os códigos do controle remoto do CD-S300, como pulsos na linha do IR.

Formato NEC: início longo, o endereço 79, o inverso dele (86), o comando e o inverso do comando, sempre com o bit
menos significativo primeiro, e um pulso final. Os comandos são os da tabela do manual de serviço (página 56,
docs/pesquisa.md). Os nomes são os do groove-rig (internal/catalog/models/yamaha_cd_s300.yaml), e o
tools/test_ir.py confere os bits contra aquele arquivo.

O controle do CD-S300 não tem tecla de ligar: o aparelho não tem standby (docs/plano.md, "Ligar e desligar").

Os tempos são os do padrão NEC, não medidos neste aparelho: ainda não houve captura da linha do IR.

frame() roda igual no MicroPython (Pico) e no Python do computador.
"""

ADDRESS = 0x79

# Na ordem do controle: modo, transporte, modos de tocar, tela, números, pastas.
KEYS = ("cd_usb", "pure_direct", "eject",
        "play", "pause", "stop", "previous", "next", "rewind", "fast_forward",
        "repeat", "shuffle", "program", "repeat_a_b",
        "display", "dimmer",
        "digit_1", "digit_2", "digit_3", "digit_4", "digit_5", "digit_6", "digit_7", "digit_8", "digit_9", "digit_0",
        "enter", "clear", "folder_down", "folder_up")

COMMANDS = {"cd_usb": 0x6F, "pure_direct": 0x6E, "eject": 0x01,
            "play": 0x02, "pause": 0x55, "stop": 0x56, "previous": 0x04, "next": 0x07,
            "rewind": 0x05, "fast_forward": 0x06,
            "repeat": 0x08, "shuffle": 0x1B, "program": 0x0C, "repeat_a_b": 0x09,
            "display": 0x0A, "dimmer": 0x54,
            "digit_0": 0x10, "digit_1": 0x11, "digit_2": 0x12, "digit_3": 0x13, "digit_4": 0x14,
            "digit_5": 0x15, "digit_6": 0x16, "digit_7": 0x17, "digit_8": 0x18, "digit_9": 0x19,
            "enter": 0x3F, "clear": 0x0D, "folder_down": 0x6A, "folder_up": 0x69}

LEADER_MARK, LEADER_SPACE = 9000, 4500      # µs
MARK, SPACE_0, SPACE_1 = 560, 560, 1690
END_SPACE = 40000       # silêncio depois do código: o receptor precisa dele para separar duas teclas seguidas


def frame(key):
    """Os tempos em µs de uma tecla: linha em 0, linha solta, linha em 0, e assim por diante. Termina em espaço."""
    command = COMMANDS[key]
    words = [LEADER_MARK, LEADER_SPACE]
    for byte in (ADDRESS, ADDRESS ^ 0xFF, command, command ^ 0xFF):
        for bit in range(8):
            words += [MARK, SPACE_1 if byte >> bit & 1 else SPACE_0]
    words += [MARK, END_SPACE]
    return words
