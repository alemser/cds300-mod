"""Comandos ao CD-S300 pela rede (contrato do amp-link, "control").

    POST /control?target=key&name=play     uma tecla do controle (ir_codes.KEYS); responde com o estado
    POST /ir/send?cmd=play                 a mesma tecla; responde com o estado da linha do IR
    GET  /ir                               o estado da linha do IR e a lista de teclas

Por enquanto só existe o alvo "key": os outros alvos do contrato (volume, tom) são de amplificador. Pedir o resultado
("vá para a faixa 5") em vez da tecla depende de ler o display, e vem depois das capturas.

Um pedido por vez: enquanto uma tecla está saindo, a seguinte recebe "busy". Uma tecla leva uns 110 ms, com o
silêncio do fim.

check() roda igual no MicroPython (Pico) e no Python do computador (tools/test_control.py).
"""

import ir_codes


def check(key, sending):
    """O texto do erro para mostrar ao usuário (em inglês, como no contrato), ou None se a tecla pode sair."""
    if key not in ir_codes.COMMANDS:
        return "unknown key"
    if sending:
        return "busy"
    return None


class Control:
    def __init__(self, state, remote):
        self.state = state
        self.remote = remote

    def _press(self, key):
        error = check(key, self.remote.sending())
        if error is None:
            self.remote.send(key)
        return error

    async def handle(self, req, writer):
        """Rotas /control e /ir (ver web.Publisher)."""
        from web import reply, reply_json
        if req.path == "/ir" and req.method == "GET":
            return await reply_json(writer, self.remote.status())
        if req.method != "POST" or req.path not in ("/control", "/ir/send"):
            return await reply(writer, "404 Not Found", "text/plain", b"not found\n")
        if req.path == "/control":
            if req.query.get("target") != "key":
                return await reply_json(writer, {"error": "unknown target"}, "400 Bad Request")
            key = req.query.get("name")
        else:
            key = req.query.get("cmd")
        error = self._press(key)
        if error:
            return await reply_json(writer, {"error": error}, "400 Bad Request")
        await reply_json(writer, self.state.to_dict() if req.path == "/control" else self.remote.status())
