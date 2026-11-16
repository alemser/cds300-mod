#!/usr/bin/env python3
"""Testa no computador os comandos pela rede (firmware/control.py), com uma linha de IR de mentira.

    python3 tools/test_control.py
"""

import asyncio
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "firmware"))

import control   # noqa: E402
import web       # noqa: E402  (o web.py da base roda no computador: só usa json e asyncio)


class FakeRemote:
    def __init__(self):
        self.keys = []
        self.busy = False

    def sending(self):
        return self.busy

    def send(self, key):
        self.keys.append(key)

    def status(self):
        return {"sent": len(self.keys), "sending": self.busy}


class FakeState:
    def to_dict(self):
        return {"power": None, "version": 0}


class FakeWriter:
    def __init__(self):
        self.data = b""

    def write(self, data):
        self.data += data

    async def drain(self):
        pass


def call(ctl, method, path):
    """(status, corpo) de um pedido, como o web.Publisher o entrega à rota."""
    writer = FakeWriter()
    asyncio.run(ctl.handle(web.Request(method, path, {}, None), writer))
    head, _, body = writer.data.partition(b"\r\n\r\n")
    status = int(head.split()[1])
    return status, (json.loads(body) if b"application/json" in head else body)


assert control.check("play", False) is None
assert control.check("play", True) == "busy"
assert control.check("power_toggle", False) == "unknown key"    # o CD-S300 não tem tecla de ligar
assert control.check(None, False) == "unknown key"

remote = FakeRemote()
ctl = control.Control(FakeState(), remote)

# Uma tecla pelo /control: sai, e a resposta é o estado.
assert call(ctl, "POST", "/control?target=key&name=play") == (200, {"power": None, "version": 0})
assert remote.keys == ["play"]

# A mesma tecla pelo /ir/send: a resposta é o estado da linha.
assert call(ctl, "POST", "/ir/send?cmd=next") == (200, {"sent": 2, "sending": False})
assert remote.keys == ["play", "next"]
assert call(ctl, "GET", "/ir") == (200, {"sent": 2, "sending": False})

# Nada sai quando o pedido está errado ou a linha está ocupada.
assert call(ctl, "POST", "/control?target=key&name=nope") == (400, {"error": "unknown key"})
assert call(ctl, "POST", "/control?target=key") == (400, {"error": "unknown key"})
assert call(ctl, "POST", "/control?target=volume&dir=up") == (400, {"error": "unknown target"})
assert call(ctl, "POST", "/ir/send") == (400, {"error": "unknown key"})
remote.busy = True
assert call(ctl, "POST", "/control?target=key&name=stop") == (400, {"error": "busy"})
assert call(ctl, "GET", "/control?target=key&name=stop")[0] == 404
assert remote.keys == ["play", "next"]

print("tudo certo")
