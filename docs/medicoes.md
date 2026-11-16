# Medições

Quem mede é o dono; o Claude anota. Preparado em 2026-11-16, **antes de qualquer medição**: as colunas "Esperado" vêm
do esquema do manual (`docs/pesquisa.md`), as outras ficam em branco até a bancada.

Regra geral: qualquer via do flat acima de **3,4 V** para tudo, antes de ligar o Pico.

Para medir, usar a página guiada (`docs/guia-medicoes.html`, publicada em
https://claude.ai/artifact/1Gud8oKmZ5HQ2eygCHr3Kf): um cartão por medição, com desenho, e um botão que copia tudo para
o chat. As tabelas abaixo recebem o resultado.

## Antes de ligar na tomada

1. Fotos que faltam: a traseira inteira (porta `CB902`), a placa principal na região do `IC305` e do `IC4`, e o flat
   com uma régua ao lado.
2. Flat de 15 vias: passo e largura (esperado: passo de 1,25 mm, uns 17,5 mm da primeira à última via).
3. Continuidade, com o aparelho **fora da tomada**:

| De | Para | Esperado | Medido |
|---|---|---|---|
| Vias 1 e 9 do flat (`DGND`) | Entre si | Bip | |
| Perna `OUT` do `U701` | Pernas 1 e 2 do `IC702` | Bip (é assim que se acha a perna `OUT`) | |
| Perna `G` do `U701` | `DGND` | Bip | |
| `DGND` do flat | `DGND` do `CB301` | Bip | |

Anotar de que lado o `U701` foi olhado (pela frente, com a lente virada para quem olha, ou por trás, pelo lado das
soldas) e a ordem das pernas encontrada: o esquema diz `OUT`, `G`, `VCC`.

## Com o aparelho ligado

Ponta preta no `DGND` (via 1 ou 9). No `CB304`, pelas janelas do conector, guiando-se pelos **nomes** da serigrafia:
os números se invertem entre as duas placas.

### As 15 vias (numeração do `CB701`, placa frontal)

| Via | Nome | Esperado (V) | Parado, sem disco | Tocando | Observação |
|---|---|---|---|---|---|
| 15 | `FL_/CS` | 3,3 | | | |
| 14 | `FL_DATA` | 0 | | | Muda o tempo todo: o multímetro mostra uma média |
| 13 | `FL_CLK` | 3,3 | | | Idem |
| 12 | `FL_/RST` | 3,3 | | | |
| 11 | `D+3.3V` | 3,4 | | | |
| 10 | `REM` | 3,4 | | | Apertar uma tecla do controle: a leitura deve tremer |
| 9 | `DGND` | 0 | | | |
| 8 | `LED_POWER` | 3,3 | | | |
| 7 | `LED_PDIRECT` | 0 | | | Com o PURE DIRECT ligado: |
| 6 | `LED_/USB1` | 3,4 | | | No modo USB: |
| 5 | `LED_/USB2` | 3,4 | | | No modo USB: |
| 4 | `KEY_0` | 3,4 | | | STOP / PAUSE / abrir apertados: 0,2–0,3 / 0,9–1,0 / 2,0–2,1 |
| 3 | `KEY_1` | 3,4 | | | PLAY / próxima / anterior apertados: idem |
| 2 | `KEY_2` | 3,4 | | | PURE DIRECT / CD/USB apertados: ~0 / 0,9–1,0 |
| 1 | `DGND` | 0 | | | |

### Receptor e alimentação

| Ponto | Esperado | Medido | Observação |
|---|---|---|---|
| `U701`, perna `OUT`, em repouso | 3,3 V | | |
| `U701`, perna `VCC` | 3,3 V | | |
| `CB301`, `D+5` | 5,0 V | | |
| `CB301`, `+B2` | ~12 V, sem regulador | | Alternativa para o Pico, com regulador próprio |
| Dissipador do `IC801` (7805), depois de 30 min tocando | — | | Morno ou quente? O Pico pede mais 50 a 100 mA |

## Teste de interferência do Wi-Fi (passo 2b)

Pico num saquinho, no power bank, transmitindo sem parar. Disco em pausa, volume do amp alto.

| Perto de | Ruído na saída? | O disco pula? | RSSI (tampa fechada) |
|---|---|---|---|
| Placa de saída analógica (NJM2068) | | | |
| DAC (`IC302`) | | | |
| Leitor óptico | | | |
| Placa frontal (onde o Pico vai ficar) | | | |

## Para a saída B (tomada inteligente)

Desligar pela tomada, com o botão da frente apertado, e ligar de novo:

| Pergunta | Resposta |
|---|---|
| Liga sozinho? | |
| Volta no modo em que estava (CD ou USB)? | |
| O PURE DIRECT volta como estava? | |
| Lê o disco sozinho (mostra faixas e tempo)? | |

## Registro

As leituras na ordem em que foram feitas, com data e hora.
