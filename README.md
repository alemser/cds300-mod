# CD-S300 mod

O terceiro aparelho modificado, depois do SP103 (`sp103-display-proxy`) e do MR 780 (`mr780-mod`): o CD player
**Yamaha CD-S300**. Um Raspberry Pi Pico 2 W dentro do aparelho, que lê o que ele mostra no display, publica o estado
na rede e o comanda pelo Wi-Fi, com os códigos do controle remoto mandados por fio.

É o primeiro aparelho que não é amplificador. Por isso o contrato do `amp-link` deixa de ser só de amps: os aparelhos
são achados na rede e cada um diz o que é e o que sabe fazer (`docs/plano.md`, "O protocolo comum").

## Situação (2026-11-16)

Início. Nada medido, nada soldado. O que existe:

- Vinte e quatro fotos do aparelho aberto (`docs/images/`), oito delas sem a frente do gabinete.
- O **manual de serviço** (57 páginas, com esquema), na cópia local em `docs/manual/`. Ele respondeu quase tudo o que
  no MR 780 precisou de multímetro: a pinagem do cabo do display, as tensões, a fonte e os códigos do controle remoto
  (`docs/pesquisa.md`).

O que o manual já decidiu:

| Assunto | O que se sabe |
|---|---|
| Display | VFD com o controlador dentro do vidro, comandado por 4 fios (`FL_/CS`, `FL_CLK`, `FL_DATA`, `FL_/RST`), em **3,3 V** |
| Onde ligar | No cabo flat de **15 vias** entre a placa principal (`CB304`) e a placa frontal (`CB701`). Todas as vias são de lógica, 0 a 3,3 V |
| Controle remoto | Código de cliente `79`, 29 teclas, todas com o código no manual. O sinal do receptor passa pela via `REM` |
| Alimentação do Pico | `D+5` (regulador 7805 da fonte). Falta medir a folga |
| Ligar e desligar | **Não há standby.** O botão da frente é uma chave na entrada dos 230 V, e o controle remoto não tem tecla de ligar |

O último item muda o projeto: com o aparelho desligado, o Pico também está desligado. As saídas possíveis estão em
`docs/plano.md`, "Ligar e desligar".

Sem o aparelho na bancada, começou o firmware: a **base da ponte** (`firmware/ponte.py`), que configura o Wi-Fi sem
cabo pela rede `AmpLink-CDS300-XXXX`, é achada pela app Amp Link sem IP digitado, se atualiza pelo Wi-Fi e manda as
30 teclas do controle remoto (`POST /control?target=key&name=play`). O `/state` ainda vem todo `null`. **Nada disso
rodou num Pico ainda**: só os testes no computador. As teclas só chegam ao aparelho depois que o fio do IR for
ligado.

Pronto para a bancada: as tabelas das medições (`docs/medicoes.md`), a ligação e a lista das capturas
(`docs/descobertas-protocolo.md`) e o `tools/fl_decode.py`, que lê as capturas do analisador.

Decidido: ligar e desligar fica na saída A (a ponte some com o aparelho desligado), com uma tomada Wi-Fi depois se
fizer falta; o contrato passa a se chamar **DeviceLink**, em etapas (`docs/plano.md`, "O protocolo comum").

Próximo passo: conferir as tensões do flat com o multímetro e capturar o display com o analisador lógico
(`docs/plano.md`, passos 2 e 3).

## Documentos

| Documento | Conteúdo |
|---|---|
| [`docs/plano.md`](docs/plano.md) | O plano, passo a passo, as ideias de customização e o protocolo comum |
| [`docs/pesquisa.md`](docs/pesquisa.md) | O que o manual de serviço e as fotos dizem: display, conectores, fonte, microcontrolador, códigos do controle |
| [`docs/medicoes.md`](docs/medicoes.md) | As medições da bancada: tabelas prontas, com o esperado do esquema |
| [`docs/descobertas-protocolo.md`](docs/descobertas-protocolo.md) | A ligação do analisador, as capturas a fazer e o que elas mostram |

O manual de serviço fica só na cópia local, em `docs/manual/` (tem direitos autorais, não vai para o GitHub).

## Fotos (`docs/images/`, 2026-11-16)

| Foto | O que mostra |
|---|---|
| `20261116_082804.jpg` | A placa frontal por trás, com a serigrafia das vias do flat ao lado do `CB701`, e parte da fonte |
| `20261116_082821.jpg` | Canto da fonte, com o `CB807` (4 fios para a placa frontal: filamento do VFD e −27 V) |
| `20261116_082833.jpg` | A fonte: retificadores, capacitores e o conector do transformador |
| `20261116_082851.jpg` | Traseira: saída analógica, coaxial e óptica |
| `20261116_082858.jpg` | Traseira: etiqueta (230 V, 50 Hz, 13 W) e a entrada de força de 2 pinos |
| `20261116_082908.jpg` | Frente, lado esquerdo: botão de ligar, USB, CD/USB, PURE DIRECT |
| `20261116_082914.jpg` | Frente, centro: bandeja e o display |
| `20261116_082918.jpg` | Frente, lado direito: as teclas de transporte |
| `20261116_083847.jpg` | O `CB304` na placa principal, de perto: uma janela por via, com o contato à mostra |
| `20261116_083859.jpg` | O `CB304` pelo outro lado, com o reforço azul do flat e as soldas do conector |
| `20261116_084546.jpg` | As 15 soldas do `CB701` atrás da placa frontal, e os resistores em série do display |
| `20261116_084556.jpg` | A serigrafia com o nome das 15 vias na placa frontal, e o `W702` (filamento e −27 V) |
| `20261116_084609.jpg` | Atrás da placa frontal, na região do `IC702`, com a folha de plástico isolante |
| `20261116_084629.jpg` | Placa principal: o `IC2` (LC786922) e o conector do leitor óptico |
| `20261116_084644.jpg` | Placa principal: o conector da fonte `CB301` com os nomes, o `IC7`, o `IC303` e o `CB304` com os nomes das vias |
| `20261116_084657.jpg` | A placa de saída analógica (os dois NJM2068) |
| `20261116_111148.jpg` | O display aceso, sem a frente do gabinete: os 12 caracteres, os ícones e as pernas do vidro |
| `20261116_111152.jpg` | As plaquinhas do USB e do PURE DIRECT, com os LEDs e as teclas |
| `20261116_111202.jpg` | Visão geral sem a frente do gabinete (carimbo 18 AUG 2017 no chassi) |
| `20261116_111455.jpg` | Atrás da plaquinha do PURE DIRECT: `W701A`, `W703`, `D702` |
| `20261116_111459.jpg` | Atrás do display: as trilhas que saem do vidro |
| `20261116_111503.jpg` | Atrás do receptor de IR: as 3 pernas do `U701`, a porta `IC702` |
| `20261116_111509.jpg` | Atrás do `CB701`: os resistores do display `R701` a `R704` |
| `20261116_111519.jpg` | Atrás do `CB701` com as legendas, o `W702` (tensão alta) ao lado, e o `CB301` da placa principal |

## Pastas

- `firmware/`: o programa do Pico (MicroPython).
  - Deste projeto: `ponte.py` (o programa), `device.py` (o `/device`), `ir_codes.py` (os códigos do controle),
    `ir.py` (a linha do IR) e `control.py` (as rotas `/control` e `/ir`).
  - **Cópias da base comum** (repositório `amp-link`, pasta `firmware-base/`): `wifi.py`, `web.py`, `ota.py`,
    `udp.py`, `listeners.py` e `main.py`. Mudar lá e copiar com `python3 ../amp-link/firmware-base/copiar.py`,
    nunca aqui.
  - `main.py` (o porteiro das atualizações) e `secrets.py` (a senha das atualizações, fora do git) só vão ao Pico
    pelo cabo; o resto vai pelo Wi-Fi com `python3 tools/enviar.py`.
- `tools/`: os testes no computador, o `enviar.py` e o `fl_decode.py` (lê as capturas do analisador). O `enviar.py`, o `test_wifi.py` e o `test_listeners.py` também
  vêm da base.
- `captures/`: capturas do analisador lógico (a criar).

## Testar no computador

```sh
for t in wifi listeners device ir control fl_decode; do python3 tools/test_$t.py; done
python3 ../amp-link/firmware-base/copiar.py --conferir    # as cópias da base estão em dia?
```

O `test_ir.py` compara os códigos com o modelo do `groove-rig` (`~/Projects/groove-rig`).

## Instalar no Pico (pelo cabo, uma vez)

```sh
cp firmware/secrets.example.py firmware/secrets.py    # e preencher UPDATE_PASSWORD
mpremote fs cp firmware/*.py : + reset
```

Sem rede salva, o Pico abre a rede `AmpLink-CDS300-XXXX`: na app Amp Link, "Set up the amp's Wi-Fi". Daí em diante,
atualizações só pelo Wi-Fi: `python3 tools/enviar.py`.
