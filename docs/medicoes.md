# Medições

Quem mede é o dono; o Claude anota. Preparado em 2026-11-16, **antes de qualquer medição**: o "Esperado" vem do
esquema do manual (`docs/pesquisa.md`).

Para medir, usar a página guiada (`docs/guia-medicoes.html`, publicada em
https://claude.ai/artifact/1Gud8oKmZ5HQ2eygCHr3Kf): um cartão por medição, com desenho, e um botão que copia tudo para
o chat. A tabela abaixo recebe o resultado.

## O que decide antes de soldar

Só o que muda uma decisão agora: se o Pico pode se ligar às vias que vai usar, onde soldar o fio do controle remoto,
se o `D+5` aguenta o Pico e em qual solda do `CB701` vai cada fio (`docs/plano.md`, "A ligação"). Qualquer via acima de **3,4 V** para tudo.

| Medida | Aparelho | Esperado | Medido | Decide |
|---|---|---|---|---|
| Soldas do `CB701` de `DGND`, `FL_/CS`, `FL_CLK`, `FL_DATA` e `FL_/RST`: bip desde a janela do `CB304`, marcadas com caneta | Fora da tomada | Uma solda por via | | Onde soldar os fios de leitura |
| Perna do `U701` que bipa com duas pernas vizinhas do `IC702` | Fora da tomada | Uma só (`OUT`) | | Onde soldar o fio do IR |
| `D+3.3V` | Ligado, parado | 3,4 V | | A placa frontal é de 3,3 V |
| `FL_/CS` | Ligado, parado | 3,3 V | | O Pico pode escutar o display |
| `FL_/RST` | Ligado, parado | 3,3 V | | Idem |
| `REM` | Ligado, parado | 3,4 V | | Idem, para o controle |
| `U701`, perna `OUT`, em repouso | Ligado, parado | 3,3 V | | O Pico pode puxar a linha para 0 |
| `D+5` (no `CB301`) | Ligado | 4,75 a 5,25 V | | Alimentar o Pico pelo `D+5` |
| Dissipador do `IC801` depois de 30 min tocando | Desligado | Morno | | Idem: se estiver quente demais, medir o `+B2` (~12 V) |

## Fica para depois

- **As outras 11 vias do flat** (LEDs, teclas, `FL_DATA`, `FL_CLK`): o Pico não se liga nelas. A média do
  multímetro em `FL_DATA` e `FL_CLK` não mostra o pico da tensão; o analisador lógico mostra o display melhor.
- **Teste de interferência do Wi-Fi** (passo 2b do plano): precisa de um Pico transmitindo. Entra no primeiro teste
  da ponte dentro do aparelho, junto com o RSSI com a tampa fechada.
- **Como o aparelho volta depois de tirado da tomada** (saída B): só se a tomada Wi-Fi um dia fizer falta.
- **Fotos da traseira (`CB902`) e do `IC305`/`IC4`**: servem às ideias de mais tarde (RS-232, erros de leitura,
  S/PDIF).

## Registro

As leituras na ordem em que foram feitas, com data e hora.

- **2026-11-16, 16h:** passo do flat de 15 vias medido por foto, com uma fita métrica encostada no `CB304` (fotos
  `20261116_160859.jpg` e `20261116_160947.jpg`, fora do repositório): do 1º ao 15º contato, 17,4 e 18,1 mm, ou seja
  passo de **1,25 mm** (com 1,0 mm seriam 14 mm). Confere com os conectores `52044`/`52045` do esquema. O cabo de
  câmera do Raspberry Pi (15 vias, 1,0 mm) não serve.
- **2026-11-16, tarde** (página guiada):
  - Mapa do `CB701` confirmado com três bips: janela 2 do `CB304` → baixo 7ª, janela 6 → baixo 5ª, janela 1 → cima
    8ª. As posições do plano valem.
  - Saída do `U701`: **perna C** (a de baixo, na foto `20261116_111503.jpg`).
  - Ligado, parado, sem disco, preta na cima 5ª (`DGND`): `D+3.3V` 3,28 V, `FL_/CS` 2,92 V (média: cai a 0 a cada
    escrita do display), `FL_/RST` 3,27 V, `REM` 3,28 V, saída do `U701` 3,0 V. Nada acima de 3,4 V.
  - `D+5` **5,05 V** e `+B2` **12,00 V** (no `CB301`). O dissipador do `IC801` não foi medido (o "frio" do texto
    copiado é o campo que ficou preenchido); a temperatura fica para o primeiro teste com o Pico ligado.
- **2026-11-16, 18h:** seis fios soldados (fotos `20261116_175957.jpg` e `20261116_180004.jpg`, cópias em
  `docs/guia/`). Conferência com o bip pelas pontas soltas, aparelho fora da tomada: **nenhum curto**.

