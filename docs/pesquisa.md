# CD-S300: o que o manual de serviço e as fotos dizem (2026-11-16)

Fonte: o manual de serviço da Yamaha (2009, 57 páginas), na cópia local `docs/manual/cd-s300-service-manual.pdf`, com
o texto em `.txt` ao lado. As páginas citadas são as impressas no manual. As tensões são as que o esquema traz
impressas: **nenhuma foi medida ainda neste aparelho.**

## Resumo

- Display VFD serial de 3,3 V, com o controlador dentro do vidro. Quatro fios de lógica.
- Um cabo flat de 15 vias leva tudo o que interessa: display, controle remoto, LEDs e teclas. Só lógica, 0 a 3,3 V.
- Os fios de tensão alta do VFD (filamento e −27 V) vão por **outro** cabo, de 4 fios. Não se mexe nele.
- Sem standby: a chave da frente corta os 230 V.
- Todos os códigos do controle remoto estão no manual.

## O display (página 22, esquema na 43)

- `V701`, modelo **14-ST-68GINK**, na placa frontal (`OPERATION (1)`).
- 14 grades. As grades 1 a 12 são os 12 caracteres, cada um uma matriz de **5×7 pontos** (35 ânodos, `D0` a `D34`).
  As grades 13 e 14 são os ícones (play, pause, TRACK, TOTAL, REMAIN, PROG, RNDM, REP, FOLDER, A-B, USB, MP3, WMA, AAC
  e os outros).
- O controlador está dentro do vidro. Pinos de lógica: `CS` (seleção), `CP` (relógio), `DA` (dados), `RESET`, `OSC`.
  Só entrada: o microcontrolador escreve, o display não responde.
- Alimentação do vidro: `VDD` 3,3 V, `VFL` −28 V, filamento `F1`/`F2` em corrente alternada sobre −21,7 V.
- **Não se sabe ainda** se o microcontrolador manda códigos de caracteres ou os pontos de cada caractere. A captura
  responde. Se forem pontos, o leitor precisa de uma tabela de fontes, e o Pico pode desenhar qualquer coisa.

## O cabo flat de 15 vias (esquema, página 43)

Liga o `CB304` da placa principal ao `CB701` da placa frontal. É onde o Pico entra. A serigrafia da placa frontal
(`20261116_082804.jpg`) confere com o esquema.

| Via | Nome | Tensão no esquema | O que é |
|---|---|---|---|
| 15 | `FL_/CS` | 3,3 V | Seleção do display |
| 14 | `FL_DATA` | 0 V | Dados para o display |
| 13 | `FL_CLK` | 3,3 V | Relógio do display |
| 12 | `FL_/RST` | 3,3 V | Reset do display |
| 11 | `D+3.3V` | 3,4 V | Alimentação da lógica da placa frontal |
| 10 | `REM` | 3,4 V | Sinal do receptor do controle remoto, em repouso alto |
| 9 | `DGND` | 0 V | Terra digital |
| 8 | `LED_POWER` | 3,3 V | LED de ligado |
| 7 | `LED_PDIRECT` | 0 V | LED do PURE DIRECT |
| 6 | `LED_/USB1` | 3,4 V | LED do USB, laranja |
| 5 | `LED_/USB2` | 3,4 V | LED do USB, verde |
| 4 | `KEY_0` | 3,4 V | Teclas STOP, PAUSE, abrir/fechar |
| 3 | `KEY_1` | 3,4 V | Teclas PLAY, próxima, anterior |
| 2 | `KEY_2` | 3,4 V | Teclas PURE DIRECT, CD/USB |
| 1 | `DGND` | 0 V | Terra digital |

Entre o conector e o vidro, cada via do display tem um resistor em série (10 a 100 Ω, `R701` a `R704`).

### O que as fotos de perto mostram (2026-11-16)

- **A numeração se inverte na placa principal.** A tabela acima é a do `CB701` (placa frontal). No `CB304` o esquema
  (página 42) conta ao contrário: a via 1 é o `FL_/CS` e a via 15 é o `DGND`. Para não errar, guiar-se pelos **nomes
  na serigrafia**, que existem nas duas placas, e não pelos números.
- Na placa frontal, a serigrafia traz as 15 vias pelo nome, na ordem da tabela (`20261116_084556.jpg`). Na placa
  principal, ao lado do `CB304`, estão escritas só algumas (`KEY-2`, `KEY-0`, `LED-/USB1`, `LED-POWER`, `REM`,
  `FL-/RST`, `FL-DATA`), na mesma ordem (`20261116_084644.jpg`).
- **Os conectores:** o esquema os marca como `52044` (frontal) e `52045` (principal), que na Molex são conectores de
  flat de **passo 1,25 mm**. Conferir com a régua antes de comprar a extensão: 15 vias devem dar uns 17,5 mm entre a
  primeira e a última. O flat tem reforço azul nas duas pontas e a marca `AWM 20624 80C 60V VW-1`.
- **Dá para medir sem soldar.** O `CB304` fica em pé na placa principal e tem uma janela por via, com o contato de
  metal à mostra (`20261116_083847.jpg`): a ponta do multímetro alcança cada via. Na placa frontal, as 15 soldas do
  `CB701` ficam viradas para dentro do aparelho, em duas fileiras (`20261116_084546.jpg`).
- O conector da fonte na placa principal (`CB301`) fica a poucos centímetros do `CB304`, com os nomes na serigrafia
  (`D+5`, `DGND`, `+B2` e os outros). A alimentação do Pico e os sinais saem do mesmo canto.
- Atrás da placa frontal, na região do receptor e do `IC702`, há uma folha de plástico isolante colada
  (`20261116_084609.jpg`). Para soldar o fio do controle remoto ali, ela precisa ser levantada.
- Os chips conferem com o manual: `IC2` LC786922, `IC7` LC87F1HC, e os dois NJM2068 na placa de saída analógica.

### Com a frente do gabinete tirada (fotos de 2026-11-16, 11h)

Sem a frente de alumínio, a placa frontal (`YA984-1`, mais as pequenas `YA984-3` do USB e a do PURE DIRECT) fica de pé,
com o lado das soldas virado para dentro do aparelho e alcançável de cima. Tudo o que o Pico precisa está nesse lado.

- **O receptor de IR (`U701`)** tem as 3 pernas soldadas atrás da placa, ao lado da porta `IC702` (5 pernas, SOT-23)
  e dos `C717`/`C719` (`20261116_111503.jpg`). É ali que entra o fio do controle remoto. Qual das três pernas é a saída
  (`OUT`) se confirma com o multímetro: é a que tem continuidade com as pernas 1 e 2 do `IC702` (as duas entradas da
  porta). O esquema põe as pernas na ordem `OUT`, `G`, `VCC`.
- **Os resistores do display** (`R701` a `R704`) ficam entre as soldas do `CB701` e o vidro, numa fileira só, com os
  códigos `100` (10 Ω, o do `FL_/RST`) e `101` (100 Ω) visíveis (`20261116_111509.jpg`, `20261116_111519.jpg`). Os
  dois lados de cada um são bons pontos para as pontas do analisador lógico.
- **Os fios perigosos ficam a uns 2 cm:** o `W702` (`FLGND`, `ACFL1`, `ACFL2`, `-27`) está à esquerda do `CB701`, do
  mesmo lado da placa (`20261116_111519.jpg`). As trilhas dele descem para o filamento, longe dos resistores do
  display.
- **O display** (`20261116_111148.jpg`): além dos 12 caracteres e dos ícones já conhecidos, o vidro tem os círculos
  de 1 a 5 (de trocador de discos, que o CD-S300 não usa) e o "15". As pernas ficam todas na borda de cima.
- A placa do USB (`YA984-3`) e a do PURE DIRECT têm os LEDs `D751` (USB, duas cores) e `D702`, as teclas `SW708`
  (USB) e `SW703` (PURE DIRECT), e recebem os fios `W751`, `W703` e `W701A` da placa frontal
  (`20261116_111152.jpg`, `20261116_111455.jpg`).
- O chassi tem o carimbo **18 AUG 2017** (`20261116_111202.jpg`): este aparelho foi fabricado oito anos depois do
  manual (2009). Até aqui, toda serigrafia conferida bate com o manual, mas uma revisão do firmware ou da placa é
  possível. Mais um motivo para conferir com o multímetro antes de soldar.

### As teclas do painel (página 30)

Cada via `KEY_x` é uma entrada analógica do microcontrolador, com 10 kΩ para 3,3 V. Cada tecla liga a via ao terra
por um resistor diferente:

| Via | 820 Ω (0,2 a 0,3 V) | 3,3 kΩ (0,9 a 1,0 V) | 12 kΩ (2,0 a 2,1 V) |
|---|---|---|---|
| `KEY_0` | STOP | PAUSE | abrir/fechar |
| `KEY_1` | PLAY | próxima / avançar | anterior / voltar |
| `KEY_2` | PURE DIRECT (100 Ω) | CD/USB | — |

Todas as teclas do painel existem no controle remoto. Imitar as teclas pelas vias `KEY_x` só serve como reserva.

## O controle remoto

### O receptor (esquema, página 43)

O receptor `U701` (GP1UE271RK) está na placa frontal. A saída dele entra nas duas entradas de uma porta AND
(`IC702`, TC7SH08), usada só como reforço, e a saída da porta é a via `REM`, que vai ao pino 15 (`IR`) do
microcontrolador.

Consequência: a via `REM` é empurrada para 3,3 V e para 0 V por uma saída forte. **Não dá para só puxá-la para
baixo com o Pico**, como numa saída de receptor comum. Dois caminhos, a decidir na bancada:

- Ligar o Pico na **saída do `U701`** (antes da porta), que é fraca e aceita ser puxada para baixo. O receptor
  continua funcionando.
- Ou passar a via `REM` por dentro do Pico (ele recebe da placa frontal e entrega à principal), se o flat for
  cortado de qualquer jeito na fase 2.

### Os códigos (página 56)

Código de cliente **`79`** em todas as teclas. O formato não está escrito no manual, mas é **NEC, endereço 79/86**:
o `groove-rig` já tem o modelo (`internal/catalog/models/yamaha_cd_s300.yaml`), e seis teclas aprendidas no oceano em
2026-09-24 com este aparelho (abrir/fechar, play, stop, pause, anterior, próxima) decodificam para os mesmos códigos.

O manual fecha as duas dúvidas anotadas no `groove-rig`: a tecla **A/B é `09`** (acrescentada lá em 2026-11-16) e o **DIMMER é `54`**. O
`power_toggle` (`60`) que o `groove-rig` traz vem de outros modelos da família: o controle do CD-S300 não tem essa
tecla e o aparelho não tem standby, então não deve fazer nada aqui.

| Tecla | Código | Tecla | Código | Tecla | Código |
|---|---|---|---|---|---|
| CD/USB | `6F` | 1 | `11` | voltar (◄◄) | `05` |
| PURE DIRECT | `6E` | 2 | `12` | avançar (►►) | `06` |
| abrir/fechar | `01` | 3 | `13` | pause | `55` |
| PROGRAM | `0C` | 4 | `14` | anterior | `04` |
| REPEAT | `08` | 5 | `15` | play | `02` |
| RANDOM | `1B` | 6 | `16` | próxima | `07` |
| DIMMER | `54` | 7 | `17` | stop | `56` |
| A/B | `09` | 8 | `18` | FOLDER ▼ | `6A` |
| DISPLAY | `0A` | 9 | `19` | FOLDER ▲ | `69` |
| ENTER | `3F` | 0 | `10` | | |
| CLEAR | `0D` | | | | |

**Não existe tecla de ligar**, nem código de ligar.

## A fonte (esquema, página 45; diagrama de blocos, página 33)

- Fonte linear. A entrada de 230 V passa pelo fusível `F801` (500 mA) e pela chave **`SW801` (POWER ON/OFF)**, que é o
  botão da frente, e só então chega ao transformador `T801`. Desligado no botão, nada no aparelho tem energia.
- Linhas no conector `CB806` (10 vias, para o `CB301` da placa principal):

| Via | Nome | Tensão | Uso |
|---|---|---|---|
| 1 | `M2GND` | 0 | Terra do motor |
| 2 | `+B2` | 12 V, sem regulador | Entrada do conversor do USB (`IC301`) |
| 3 | `M+7` | 7 a 8 V | Motores e laser |
| 4 | `M1GND` | 0 | Terra do motor |
| 5 | `DGND` | 0 | Terra digital |
| 6 | `D+5` | 5,0 V (`IC801`, 7805 com dissipador) | Lógica; vira `D+3.3V` na placa principal (`IC303`) |
| 7 | `A+5` | 5,0 V | Áudio |
| 8 | `AGND` | 0 | Terra do áudio |
| 9 | `A-5` | −5,0 V | Áudio |
| 10 | `P_MUTE` | −4,5 V | Silencia a saída ao ligar e desligar |

- O `CB807` (4 fios, visto em `20261116_082821.jpg`) leva à placa frontal o **−27 V**, o filamento (`ACFL1`,
  `ACFL2`) e o `FLGND`. **Tensão alta para os padrões do Pico: não encostar.**
- O microcontrolador tem uma entrada `POFF_detect` (pino 57), que avisa quando a força da entrada some, e uma saída
  `STBY` (pino 79), sem descrição. A fonte não usa nenhuma linha de standby.

## A placa principal (páginas 28 a 30 e 33)

| Peça | O que é |
|---|---|
| `IC305` | Microcontrolador Renesas **R5F212CASNFP** (R8C, 16 bits, 80 pernas, 3,3 V). Comanda display, teclas, controle remoto, bandeja, DAC e o chip do USB |
| `IC2` | LC786922: controle do disco, decodifica MP3/WMA e gera o áudio digital (I2S e S/PDIF) |
| `IC7` | LC87F1HC8A: USB e iPod. Fala com o `IC305` por serial (`USB_TX`, `USB_RX`) |
| `IC302` | DAC PCM1780, comandado pelo `IC305` por três fios (`DAC_/CS`, `DAC_SCL`, `DAC_SDA`) |
| `IC304` | EEPROM: guarda o modo CD/USB, PURE DIRECT, "RS-232C ON/OFF" e se há disco |
| `IC4` | TC7SH08: reforço do S/PDIF antes da saída óptica e da coaxial. O S/PDIF em 3,3 V está na entrada dele |

Sinais do `IC305` que podem servir mais tarde: `OPSW` e `CLSW` (bandeja aberta ou fechada), `C2_Flag` e `MON_1`
(erros de leitura do disco), `USB_IN` (pendrive ou iPod ligado), `DOUT_MUTE` (saída digital muda no PURE DIRECT).

### A porta de gravação da traseira (esquema, página 44; páginas 16 a 21)

Na traseira há um conector de flat de 9 vias (`CB902`), usado pela Yamaha para gravar o firmware com um adaptador
RS-232 de 3,3 V. Leva `232C_TX`, `232C_RX`, 3,3 V, terra e os sinais que põem o microcontrolador em modo de gravação
(`BOOT`, `TMODE`, `/RESET`, `TCK`).

A EEPROM guarda um ajuste "RS-232C ON/OFF", então o firmware normal pode falar algo por essa serial. **Não se
sabe.** Vale uma captura só de escuta no `232C_TX`. Os outros sinais dessa porta não se tocam: apagam o firmware.

### Modo de fábrica (página 15)

Segurar PLAY e STOP e ligar o aparelho. O display mostra `FACTORY`. A tecla DISPLAY do controle mostra a versão do
firmware (no modo CD, a do `IC305`; no modo USB, a do `IC7`). **A tecla CLEAR apaga a EEPROM.**
