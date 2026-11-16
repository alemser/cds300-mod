# Descobertas do protocolo

O que as capturas do analisador lógico mostram sobre o display e o controle remoto. Preparado em 2026-11-16, **antes
de qualquer captura**: por enquanto só a ligação, a lista de capturas e as perguntas. As respostas entram aqui, com o
nome do arquivo em `captures/` que as prova.

## Ligação

Analisador: o Pico 2 W com o LogicAnalyzer (`logicanalyzer-sp103`). Canal N = GPIO(N+1).

| Canal | GPIO | Pino físico | Sinal | Onde |
|---|---|---|---|---|
| 1 | GP2 | 4 | `FL_/CS` | Conector dos fios soldados no `CB701` (`docs/plano.md`, "A ligação") |
| 2 | GP3 | 5 | `FL_CLK` | Idem |
| 3 | GP4 | 6 | `FL_DATA` | Idem |
| 4 | GP5 | 7 | `FL_/RST` | Idem |
| 5 | GP6 | 9 | `IR` | Idem: o fio da perna `OUT` do `U701` |
| — | GND | 3 | `DGND` | Idem |

Dar aos canais os nomes `CS`, `CLK`, `DATA`, `RST` e `REM` no programa: o `tools/fl_decode.py` usa os nomes antes dos
números.

Tudo é de 3,3 V: sem o cuidado dos 5 V do SP103. O Mac **na bateria** (o aparelho não tem terra).

Frequência de captura: começar com 10 MHz e baixar se a captura ficar curta demais para o que se quer ver. O
`fl_decode.py` avisa se o relógio do display estiver rápido demais para a frequência usada.

## As capturas

Um arquivo por cena, em `captures/`, com o número na frente. Ler cada uma com:

```sh
python3 tools/fl_decode.py captures/01-liga.lac
```

Cinco capturas bastam para o leitor de telas (o estado: tocando, pausado, parado, faixa, tempo, disco,
bandeja, modos). O controle remoto vai junto, no canal 5, em todas.

| Arquivo | Cena | Feita? |
|---|---|---|
| `01-liga` | Ligar com disco: `LOADING`, depois faixas e tempo total. Trigger na descida do `FL_/RST` ou do `FL_/CS` | |
| `02-tocando` | Play pelo controle e uns segundos tocando (o tempo correndo); depois pause, próxima e stop | |
| `03-display` | A tecla DISPLAY (faixa, restante, total) e o DIMMER | |
| `04-modos` | REPEAT, RANDOM, PROGRAM, A/B e PURE DIRECT: os ícones | |
| `05-bandeja` | Abrir e fechar a bandeja, terminando em `NO DISC` | |

Para depois, só se a ideia correspondente for feita: um CD com CD-Text e um pendrive com MP3 (texto do disco), e a
escuta do `232C_TX` da porta `CB902` (nada mais dessa porta).

## Perguntas

| Pergunta | Resposta | Captura |
|---|---|---|
| Velocidade do relógio, borda em que o dado vale, ordem dos bits | 62 kHz (6 µs alto, 10 µs baixo); dado lido na subida; **bit menos significativo primeiro** | `02-tocando` |
| Tamanho dos quadros e se o `/CS` sobe entre bytes | Um quadro por comando, com os dados dele (8 a 104 bits); o `/CS` só sobe no fim do quadro | `02-tocando` |
| O microcontrolador manda **letras ou pontos**? | **Letras, em ASCII.** Os ícones são dois caracteres desenhados por ele (abaixo) | `02-tocando` |
| Como os ícones (grades 13 e 14) são acesos: play, pause e os modos | As posições 13 e 14 mostram os caracteres especiais 0 e 1; os pontos deles são os ícones. Falta saber qual bit é qual ícone | `02-tocando` |
| De quanto em quanto tempo o display é reescrito | Ciclo de ~38 ms, em três grupos a 12,7 ms um do outro | `02-tocando` |
| O que o `DIMMER` manda | | |
| O controle remoto: NEC, endereço 79/86, os tempos de verdade | | |
| A porta RS-232 fala algo sozinha? | | |

## O protocolo (captura `02-tocando`, 2026-11-16)

Captura a 1 MHz, 200 ms, com o disco tocando a faixa 1 em 0:07. Os bytes abaixo estão com o bit menos significativo
primeiro, já como o vidro os lê. O ciclo se repete a cada ~38 ms:

| Grupo | Quadro | Leitura |
|---|---|---|
| 1 | `20` + `00 00 00 00 00` `08 04 00 00 00` | Desenha os caracteres especiais 0 e 1 (5 bytes cada). São os ícones |
| 2 | `10` + `20 20 31 20 20 20 20 30 3A 30 37 20` | Escreve o texto a partir da posição 0: `"  1    0:07 "` (faixa 1, tempo 0:07) |
| 3 | `63` | Configuração (provavelmente o número de grades) |
| 3 | `50 A0` | Configuração (provavelmente o brilho; o `DIMMER` deve mudar este) |
| 3 | `70` | Configuração (provavelmente "display aceso") |
| 3 | `1C 00 01` | Escreve a partir da posição 12 os caracteres 0 e 1: as duas grades de ícones |

Os códigos lembram os controladores de VFD da Princeton (PT6302 e parecidos): o comando no nibble de cima, o endereço
no de baixo. Não confirmado: a folha de dados do vidro não está no manual.

O que isso quer dizer para o leitor de telas:

- O texto vem pronto, em ASCII: não precisa de tabela de fonte.
- O estado (play, pause, modos) está nos 10 bytes dos caracteres especiais. Falta o mapa bit → ícone, a levantar com
  o Pico dentro do aparelho, registrando cada mudança enquanto as teclas são apertadas: mais fácil que capturas de
  200 ms.

## Icon map and state (on the device, 2026-11-16)

Mapped with the panel keys while the Pico logged every icon change (`GET /display`, `icon_changes`). Dots are
named `grid.byte.bit` (`vfd.Screen.lit`):

| Dot | Meaning |
|---|---|
| `13.0.3` | Play (lit while playing) |
| `13.1.3` | Pause |
| `13.1.2` | Disc in the tray (off with the tray open; back on at `LOADING`) |

Text: `track  elapsed` while playing or paused, `tracks  total` when stopped with a disc, `track  0:00` when a track
is picked while stopped, `LOADING` after closing the tray. Next and previous change only the text.

`vfd.Player` turns this into `/state`: `transport` (playing, paused, stopped, loading, open), `media` (track,
elapsed) and `disc` (tracks, total, remembered from the stopped display until the tray opens).

Still to map, with the remote: repeat, random, A-B, program, USB mode, Pure Direct, dimmer.
