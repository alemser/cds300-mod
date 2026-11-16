# Medições

Quem mede é o dono; o Claude anota. Preparado em 2026-11-16, **antes de qualquer medição**: o "Esperado" vem do
esquema do manual (`docs/pesquisa.md`).

Para medir, usar a página guiada (`docs/guia-medicoes.html`, publicada em
https://claude.ai/artifact/1Gud8oKmZ5HQ2eygCHr3Kf): um cartão por medição, com desenho, e um botão que copia tudo para
o chat. A tabela abaixo recebe o resultado.

## O que decide a fase 1

Só o que muda uma decisão agora: se o Pico pode se ligar às vias que vai usar, onde soldar o fio do controle remoto,
se o `D+5` aguenta o Pico e qual extensão do flat comprar. Qualquer via acima de **3,4 V** para tudo.

| Medida | Aparelho | Esperado | Medido | Decide |
|---|---|---|---|---|
| Flat: do 1º ao 15º contato (passo = ÷ 14) | Fora da tomada | 17,5 mm (passo 1,25) | | A extensão a comprar |
| Perna do `U701` que bipa com duas pernas vizinhas do `IC702` | Fora da tomada | Uma só (`OUT`) | | Onde soldar o fio do IR |
| `D+3.3V` | Ligado, parado | 3,4 V | | A placa frontal é de 3,3 V |
| `FL_/CS` | Ligado, parado | 3,3 V | | O Pico pode escutar o display |
| `FL_/RST` | Ligado, parado | 3,3 V | | Idem |
| `REM` | Ligado, parado | 3,4 V | | Idem, para o controle |
| `U701`, perna `OUT`, em repouso | Ligado, parado | 3,3 V | | O Pico pode puxar a linha para 0 |
| `D+5` (no `CB301`) | Ligado | 4,75 a 5,25 V | | Alimentar o Pico pelo `D+5` |
| Dissipador do `IC801` depois de 30 min tocando | Desligado | Morno | | Idem: se estiver quente demais, medir o `+B2` (~12 V) |

## Fica para depois

- **As outras 11 vias do flat** (LEDs, teclas, `FL_DATA`, `FL_CLK`): o Pico não se liga nelas na fase 1. A média do
  multímetro em `FL_DATA` e `FL_CLK` não mostra o pico da tensão; o analisador lógico mostra o display melhor.
- **Teste de interferência do Wi-Fi** (passo 2b do plano): precisa de um Pico transmitindo. Entra no primeiro teste
  da ponte dentro do aparelho, junto com o RSSI com a tampa fechada.
- **Como o aparelho volta depois de tirado da tomada** (saída B): só se a tomada Wi-Fi um dia fizer falta.
- **Fotos da traseira (`CB902`) e do `IC305`/`IC4`**: servem às ideias de mais tarde (RS-232, erros de leitura,
  S/PDIF).

## Registro

As leituras na ordem em que foram feitas, com data e hora.
