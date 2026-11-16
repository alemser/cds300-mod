"""GET /device: quem é esta ponte e o que ela sabe fazer.

O contrato está no repositório amp-link (docs/contrato.md). Tudo aqui é fixo enquanto o programa roda: o cliente lê
uma vez ao conectar. A versão é a mesma do GET /update.

Por enquanto (2026-11-16) a ponte do CD-S300 sabe se atualizar, configurar o Wi-Fi e mandar as teclas do controle
remoto. O estado do aparelho depende das capturas do display (docs/plano.md, passo 3). Cada capacidade nova entra em
FEATURES quando existir de verdade.

"kind" e "keys" ainda não estão no contrato (api 1): são a proposta do api 2 (docs/plano.md, "O protocolo comum"). Um
cliente de hoje ignora o que não conhece. Um CD player não tem entradas, volume nem tom, então esses campos não vêm.

describe() roda igual no MicroPython (Pico) e no Python do computador (tools/test_device.py).
"""

import ir_codes

API = 1                         # só muda quando algo deixa de ser compatível
NAME = "cds300"                 # o nome na descoberta e na rede (cds300.local, AmpLink-CDS300-XXXX); o enviar.py lê
KIND = "cd_player"
MODEL = "Yamaha CD-S300"
COLUMNS, ROWS = 12, 1           # o VFD: 1 linha de 12 caracteres, mais os ícones (docs/pesquisa.md)
FEATURES = ("update", "wifi_setup", "control")


def describe(version):
    return {"api": API, "kind": KIND, "model": MODEL, "bridge_version": version,
            "display": {"columns": COLUMNS, "rows": ROWS},
            "keys": list(ir_codes.KEYS),
            "features": list(FEATURES)}


async def handle(req, writer):
    """Rota /device (ver web.Publisher)."""
    import ota
    from web import reply, reply_json
    if req.path != "/device":
        return await reply(writer, "404 Not Found", "text/plain", b"not found\n")
    await reply_json(writer, describe(await ota.current_version()))
