# Descobertas do protocolo

O que as capturas do analisador lógico mostram sobre o display e o controle remoto. Preparado em 2026-11-16, **antes
de qualquer captura**: por enquanto só a ligação, a lista de capturas e as perguntas. As respostas entram aqui, com o
nome do arquivo em `captures/` que as prova.

## Ligação

Analisador: o Pico 2 W com o LogicAnalyzer (`logicanalyzer-sp103`). Canal N = GPIO(N+1).

| Canal | GPIO | Pino físico | Via do flat | Onde pegar |
|---|---|---|---|---|
| 1 | GP2 | 4 | `FL_/CS` | Resistor do display (`R701` a `R704`), lado do `CB701` |
| 2 | GP3 | 5 | `FL_CLK` | Idem |
| 3 | GP4 | 6 | `FL_DATA` | Idem |
| 4 | GP5 | 7 | `FL_/RST` | Idem (o de 10 Ω, código `100`) |
| 5 | GP6 | 9 | `REM` | Perna `OUT` do `U701` ou a via `REM` |
| — | GND | 3 | `DGND` | Via 1 ou 9 |

Dar aos canais os nomes `CS`, `CLK`, `DATA`, `RST` e `REM` no programa: o `tools/fl_decode.py` usa os nomes antes dos
números. Qual resistor é de qual via se confirma com o multímetro (continuidade até a via no `CB701`): anotar em
`docs/medicoes.md`.

Tudo é de 3,3 V: sem o cuidado dos 5 V do SP103. O Mac **na bateria** (o aparelho não tem terra).

Frequência de captura: começar com 10 MHz e baixar se a captura ficar curta demais para o que se quer ver. O
`fl_decode.py` avisa se o relógio do display estiver rápido demais para a frequência usada.

## As capturas

Um arquivo por cena, em `captures/`, com o número na frente. Ler cada uma com:

```sh
python3 tools/fl_decode.py captures/01-liga.lac
```

Cinco capturas bastam para o leitor de telas da fase 1 (o estado: tocando, pausado, parado, faixa, tempo, disco,
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
| Velocidade do relógio, borda em que o dado vale, ordem dos bits | | |
| Tamanho dos quadros e se o `/CS` sobe entre bytes | | |
| O microcontrolador manda **letras ou pontos**? | | |
| Como os ícones (grades 13 e 14) são acesos: play, pause e os modos | | |
| De quanto em quanto tempo o display é reescrito | | |
| O que o `DIMMER` manda | | |
| O controle remoto: NEC, endereço 79/86, os tempos de verdade | | |
| A porta RS-232 fala algo sozinha? | | |
