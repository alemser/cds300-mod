#!/usr/bin/env python3
"""Testa no computador a descrição da ponte (firmware/device.py).

    python3 tools/test_device.py
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "firmware"))

import device   # noqa: E402

d = json.loads(json.dumps(device.describe("abcd1234")))
assert d["api"] == 1
assert d["kind"] == "cd_player"
assert d["model"] == "Yamaha CD-S300"
assert d["bridge_version"] == "abcd1234"
assert d["display"] == {"columns": 12, "rows": 1}
assert d["features"] == ["update", "wifi_setup", "control"]
assert len(d["keys"]) == 30 and len(set(d["keys"])) == 30
assert d["keys"][:4] == ["cd_usb", "pure_direct", "eject", "play"]
assert "power_toggle" not in d["keys"]                  # o controle do CD-S300 não tem tecla de ligar
# Um CD player não tem entradas, volume nem tom: a app esconde o que falta.
assert "inputs" not in d and "volume_db" not in d and "tone_db" not in d
assert device.NAME == "cds300"                          # o tools/enviar.py e a descoberta usam este nome
print("tudo certo")
