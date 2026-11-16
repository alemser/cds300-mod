# Plano

O caminho é o mesmo do SP103 e do MR 780: primeiro olhar e medir, depois capturar, só então soldar. A diferença é que
aqui existe manual de serviço com esquema (`docs/pesquisa.md`), então o multímetro só confere o que o esquema diz.

Escrito em 2026-11-16, antes de qualquer medição.

## Segurança

- O CD-S300 é ligado direto na tomada (230 V). A parte de 230 V fica na placa marrom da fonte: entrada de força,
  fusível, a chave do botão da frente e o transformador. **Não encostar nela**, e fios só com o cabo fora da tomada.
- O VFD usa **−27 V** e o filamento em corrente alternada. Esses fios chegam à placa frontal pelo cabo de 4 fios do
  `CB807` (`FLGND`, `ACFL1`, `ACFL2`, `-27`) e ficam na parte de cima da placa frontal. O Pico só se liga ao flat de
  15 vias, que é todo de 0 a 3,3 V.
- O aparelho não tem terra (tomada de 2 pinos). Com o analisador lógico, usar o Mac **na bateria**, para não criar um
  caminho de terra pelo carregador.
- A porta de gravação da traseira (`CB902`) tem sinais que apagam o firmware do aparelho. Só escutar o `232C_TX`.
- No modo de fábrica, a tecla CLEAR apaga a EEPROM. Não mandar `CLEAR` por engano com o aparelho nesse modo.
- Fios do Pico só em soldas de furo passante que já existem (as do `CB701`, as pernas do `U701`, o `CB301`), nunca em
  ilhas de componentes SMD. Cada fio preso à placa com cola quente ou fita kapton, para não puxar a solda. Nada sai
  do lugar: para desfazer, basta dessoldar os fios.

## Objetivos

Os requisitos do dono (2026-11-16), em ordem:

1. **Saber o estado exato**: tocando, pausado ou parado, faixa, tempo, disco presente, bandeja, modo CD ou USB, PURE
   DIRECT.
2. **Controle remoto pelo Wi-Fi**, com os códigos do controle mandados por fio.
3. **Fácil de desfazer**: nada sai do lugar.

Junto com os dois: compartilhar o estado com os outros aparelhos, pelo mesmo contrato dos amps.

**Fora do escopo: escrever no display** (decidido em 2026-11-16). O display do CD-S300 é simples (12 caracteres e
os ícones) e não há mais o que mostrar nele. O Pico só lê o display; nunca escreve.

## A ligação: fios soldados em paralelo (decidido em 2026-11-16)

O Pico só escuta o display e só puxa a linha do receptor para 0, então nada precisa ser cortado nem tirado: os fios
vão por cima de soldas que já existem e terminam num conector só, onde se encaixa o Pico ou o analisador lógico (as
capturas usam os mesmos fios, sem garras).

| Fio | Onde | Para quê |
|---|---|---|
| `DGND` | `CB701`, cima 5ª (via 9) | Terra comum |
| `FL_/CS` | `CB701`, cima 8ª (via 15) | Ler o display |
| `FL_CLK` | `CB701`, cima 7ª (via 13) | Ler o display |
| `FL_DATA` | `CB701`, baixo 7ª (via 14) | Ler o display |
| `FL_/RST` | `CB701`, baixo 6ª (via 12) | Saber quando o display é reiniciado |
| `IR` | Perna `OUT` do `U701` | Mandar as teclas. O Pico só puxa para 0, contra o resistor interno do receptor, como no SP103: sem resistor em série |
| `D+5` e `DGND` | `CB301`, placa principal | Alimentar o Pico. Só quando o Pico for instalado |

Qual solda do `CB701` é qual via: a serigrafia atrás da placa frontal dá o mapa (as vias ímpares na fileira de cima,
as pares na de baixo, da esquerda para a direita), e três bips desde as janelas do `CB304` o confirmam
(`docs/guia-medicoes.html`). As posições contam as soldas da esquerda para a direita, olhando a placa frontal por
trás com o conector `W702` à esquerda: 8 soldas na fileira de cima, 7 na de baixo. Marcar com caneta antes de soldar. Desfazer: dessoldar os fios.

O que comprar: fio fino (30 AWG, tipo kynar), uma barra de pinos de 2,54 mm para o conector, solda fina e fluxo.

**Descartado: a ponte no flat.** Uma placa entre as duas pontas do flat (dois conectores de 1,25 mm sem trava, um
flat novo e um resistor de 1 kΩ na via `REM`, que sai de uma porta lógica e não pode ser puxada direto) só se
justificava para escrever no display sem tocar na placa da Yamaha. Sem escrita, ela custa mais e não ganha nada. O
passo do flat foi medido mesmo assim: 1,25 mm (`docs/medicoes.md`).

## Ligar e desligar

O botão da frente é uma chave nos 230 V (`SW801`), e o controle remoto não tem tecla de ligar. Com o aparelho
desligado, o Pico está desligado, e nada pelo Wi-Fi o liga. Três saídas:

| Saída | O que muda | Custo |
|---|---|---|
| **A. Aceitar** | O Pico vive enquanto o aparelho está ligado. Ele some da rede quando o aparelho desliga, e o hub entende isso como "desligado" | Nenhum |
| **B. Tomada inteligente** | O botão fica sempre apertado, e uma tomada Wi-Fi liga e desliga o aparelho. O hub comanda a tomada | Uma tomada; nada dentro do aparelho |
| **C. Relé dentro do aparelho** | Uma fonte pequena de 5 V sempre ligada para o Pico e um relé no lugar da chave | Mexe nos 230 V, dentro de um aparelho sem terra |

**Decidido em 2026-11-16: começar com A e passar para B** se ligar pelo Wi-Fi fizer falta. A saída C repete o que foi
recusado no MR 780 (fonte nova dentro do aparelho) e é a única com risco de choque.

Para a saída B, conferir antes: o aparelho ligado pela tomada volta no modo em que estava (a EEPROM guarda o modo
CD/USB e o PURE DIRECT) e lê o disco sozinho?

## Passo 1: fotos e manual

**Feito em 2026-11-16**: dezesseis fotos e o manual de serviço. As fotos de perto já mostraram o flat nas duas
pontas, os nomes das vias nas duas placas e o conector da fonte (`docs/pesquisa.md`).

Com a frente do gabinete tirada, as fotos mostraram também as pernas do receptor `U701` e os resistores do display:
os pontos onde o fio do IR e o analisador lógico se ligam.

Fotos que ainda ajudam:

- A traseira inteira, para achar a porta de gravação `CB902`.
- A placa principal na região do `IC305` e do `IC4` (S/PDIF).

## Passo 2: multímetro

Com o aparelho ligado, contra o `DGND` (via 1 ou 9 do flat):

1. O mapa das soldas do `CB701` (três bips) e a perna `OUT` do `U701` (a que bipa com o `IC702`), com o aparelho
   fora da tomada.
2. As vias que o Pico usa (`D+3.3V`, `FL_/CS`, `FL_/RST`, `REM`) e a saída do `U701` em repouso. Qualquer valor
   acima de 3,4 V para tudo.
3. O `D+5` no `CB301` da placa principal, ao lado do flat: a tensão. A temperatura do dissipador do `IC801` (na
   fonte) fica para o primeiro teste com o Pico ligado no `D+5`, depois de meia hora tocando: é com a carga do Pico
   (mais uns 50 a 100 mA) que ela diz algo. Tocar só com o aparelho fora da tomada.
4. O `+B2`, no mesmo conector: alternativa para alimentar o Pico por um regulador próprio, se o `D+5` não tiver
   folga.

A página guiada (`docs/guia-medicoes.html`, https://claude.ai/artifact/1Gud8oKmZ5HQ2eygCHr3Kf) mostra cada ponto
sobre as fotos do aparelho e copia o resultado para o chat. Anotar em `docs/medicoes.md`.

## Passo 2b: teste de interferência do Wi-Fi

O mesmo teste do MR 780 (`mr780-mod/docs/plano.md`, passo 2b): o Pico num saquinho, alimentado por power bank,
transmitindo sem parar, perto de cada placa. Aqui o que se ouve é a saída analógica, com o disco em pausa e o volume
do amp alto. Os pontos sensíveis são o DAC, os amplificadores de saída e o leitor óptico (erros de leitura em vez de
ruído: ver se o disco pula). Anotar também o RSSI com a tampa fechada.

## Passo 3: analisador lógico

Com o LogicAnalyzer do SP103 (`logicanalyzer-sp103`), encaixado no conector dos fios já soldados: `FL_/CS`,
`FL_CLK`, `FL_DATA`, `FL_/RST` e o `IR`.

Display:

- Ligar o aparelho, sem disco e com disco (`LOADING`, `NO DISC`, o total de faixas e de tempo).
- Play, pause, stop, próxima, anterior, avançar e voltar.
- A tecla DISPLAY (tempo da faixa, restante, total) e o DIMMER.
- REPEAT, RANDOM, PROGRAM, A/B, PURE DIRECT.
- Abrir e fechar a bandeja.
- Depois, se a ideia do texto do disco for feita: um CD com CD-Text e um pendrive com MP3.

O que as capturas precisam responder:

- O protocolo do vidro: velocidade, ordem dos bits, comandos.
- **O microcontrolador manda letras ou pontos?** Decide como é o leitor de telas (com pontos, ele precisa de uma
  tabela da fonte do vidro para reconhecer as letras).
- Como os ícones (grades 13 e 14) são acesos: é deles que saem play, pause e os modos.
- De quanto em quanto tempo o display é reescrito (o tempo corre de segundo em segundo).

Controle remoto: uma tecla basta para confirmar o formato (NEC?) e o código de cliente `79`. O resto vem da tabela do
manual.

Uma captura à parte, só de escuta, no `232C_TX` da porta da traseira: ver se o aparelho fala algo sozinho.

Documentar em `docs/descobertas-protocolo.md` (a ligação, a lista de capturas e as perguntas já estão lá), com as
capturas em `captures/`. O `tools/fl_decode.py` lê cada `.lac`: corta o display em quadros, mede o relógio e os
intervalos, mostra os bytes nas duas ordens de bits e decodifica o NEC do controle. Ele não supõe nada do protocolo
do vidro; o leitor de telas sai do que ele mostrar.

## Passo 4: o programa

1. **A base da ponte**: Wi-Fi sem cabo pela rede `AmpLink-CDS300-XXXX`, descoberta e atualização pelo Wi-Fi, com o
   `/state` todo `null`. **Escrita em 2026-11-16**, testada só no computador.
2. O `/device` do CD-S300. **Escrito em 2026-11-16**, com `kind` e `keys`, que são a proposta do `api` 2.
3. O envio dos códigos do controle remoto, e o `/control`. **Escrito em 2026-11-16**: as 30 teclas da tabela do
   manual, em NEC 79/86, conferidas bit a bit com o modelo do `groove-rig`. O PIO que move a linha é o do SP103.
   **Funcionando no aparelho em 2026-11-16**: o Pico alimentado pelo `D+5`, na rede de casa (`CDS300-D85E`), e o
   `POST /control?target=key&name=play` pôs o disco a tocar. O fio do controle está no GP6 (não no GP15 do SP103),
   para o mesmo chicote servir ao analisador. Os tempos são os do padrão NEC, não medidos neste aparelho.
4. O sniffer do display (PIO) e o leitor das telas, testados no Mac com as capturas reais.

Os arquivos de Wi-Fi, servidor e atualização saíram do `mr780-mod` e agora ficam num lugar só: a **base comum**, no
repositório `amp-link`, pasta `firmware-base/`. Cada projeto recebe uma cópia igual, feita pelo `copiar.py` de lá. O
`mr780-mod` e este projeto usam a base; o `sp103-display-proxy` ainda não (o `web.py` e o `main.py` dele têm partes
próprias).

As lições do SP103 continuam valendo: sem página web no Pico, sem respostas grandes, uma conexão `/events` por
cliente, e copiar cada parte só quando for usada.

## O protocolo comum

O contrato do `amp-link` (`amp-link/docs/contrato.md`, `api` 1) já tem quase tudo: descoberta por broadcast UDP, o
`/device` que diz o que a ponte sabe fazer, o `/state`, o `/events` e o `/control`. Falta deixar de supor que todo
aparelho é um amplificador. Proposta, a escrever no `amp-link` como `api` 2 **depois das capturas**, quando os campos
do CD player forem conhecidos:

| Parte | Hoje | Proposta |
|---|---|---|
| Descoberta | Responde `name`, `model`, `ip` | Mais `kind` (`amplifier`, `cd_player`) e `api`, para o cliente saber o que achou sem perguntar a cada um |
| `/device` | `volume_db`, `tone_db` e `inputs` sempre presentes | Só o que o aparelho tem. As `features` dizem quais grupos existem |
| Grupos de estado | Os do amp: volume, entrada, tom | Novos: `transport` (tocando, pausado, parado, bandeja), `media` (faixa, tempo, texto), `disc` (faixas, tempo total) |
| Comandos | `POST /control?target=key&name=…` | O mesmo. O `/device` passa a listar as teclas que o aparelho aceita |
| `/names` | Estrutura do SP103 | Vira `/config` (já estava "em aberto" no contrato) |
| `screen`, `/bus.*` | Do SP103 | Por aparelho (também já "em aberto") |

**Estado compartilhado.** As pontes não conversam entre si: um Pico aguenta poucas conexões. Um ponto central (o
`groove-rig`, no oceano) assina o `/events` de cada aparelho e aplica as regras entre eles. A app Amp Link mostra
cada aparelho pelo `/device` dele.

**O nome: DeviceLink** (decidido em 2026-11-16). Com um CD player, "AmpLink" deixa de descrever o que o contrato é.
A troca passa pela base comum, pelas duas pontes que já existem (uma delas dentro do SP103, em uso) e pela app, então
vai em etapas, sem nenhum momento em que a app e uma ponte deixem de se achar:

1. **Base comum (`amp-link/firmware-base`)**: a descoberta responde às duas perguntas, `AMPLINK?` e `DEVICELINK?`; a
   rede de configuração passa a `DeviceLink-<MODELO>-XXXX`. O `enviar.py` pergunta `DEVICELINK?` e, sem resposta,
   `AMPLINK?`. Copiar para este projeto e para o `mr780-mod`.
2. **App**: procura as redes `DeviceLink-…` e `AmpLink-…`, pergunta as duas coisas, e o nome que aparece na tela
   muda. O pacote Android (`com.alemser.amplink`) fica: trocá-lo faz o telefone ver uma app nova, sem as pontes
   salvas.
3. **SP103**: entra na troca quando passar a usar a base comum (o `wifi.py` dele ainda é próprio).
4. **Depois que todas as pontes responderem `DEVICELINK?`**: a app e a base deixam de perguntar e de responder
   `AMPLINK?`.
5. O repositório `amp-link` e o contrato (`docs/contrato.md`) trocam de nome junto com o `api` 2.

Até a etapa 1, este projeto segue com `AmpLink-CDS300-XXXX`.

## Ideias

Além do básico (estado e comandos). A coluna "Depende de" diz o que precisa existir além disso. As ideias que
escreviam no display (o título da faixa, um relógio com o aparelho parado) saíram junto com a escrita no display.

| Ideia | O que é | Depende de |
|---|---|---|
| Ligar o amp junto | Play no CD liga o amp e escolhe a entrada CD; outra entrada no amp ou standby pausa o CD | O ponto central |
| Reconhecer o disco | Ao carregar, o aparelho mostra o número de faixas e o tempo total. O par serve de chave na coleção (`groove-catalog`): o disco é nomeado uma vez e reconhecido sempre | — |
| "Tocando agora" e histórico | O `groove-display` mostra o disco e a faixa; o groove guarda o que foi tocado | — |
| Texto do disco e do pendrive | CD-Text e nomes de arquivo e de pasta, remontados da rolagem do display | — |
| Faixa direta, programa, A-B | Pela app, com as teclas numéricas do controle, sem o controle na mão | — |
| Timer de desligar e despertador | Parar depois de N minutos; tocar numa hora marcada | — (o despertador depende de "Ligar e desligar") |
| Horas de uso | Tempo total tocando, guardado no Pico: a idade do laser | — |
| Saúde do disco | Contar os erros de leitura (`C2_Flag`, pino 31 do `IC305`): disco riscado ou laser fraco | Um fio a mais na placa principal |
| Bandeja | Saber se está aberta (`OPSW`, `CLSW`) sem depender do display | Dois fios a mais, só se o display não bastar |
| Fonte do VU dos amps | O Pico lê o S/PDIF (3,3 V, na entrada do `IC4`) e publica o nível do áudio. O CD player vira a fonte do VU do SP103 e do MR 780, no lugar do relay | A estudar: não foi verificado se o Pico dá conta de ler S/PDIF junto com o resto |
| Volume na saída | O DAC PCM1780 tem atenuador digital, comandado por três fios. O Pico poderia ajustar o nível | A estudar: disputa os três fios com o microcontrolador e mexe no caminho do som |

## Perguntas em aberto

- A base comum do firmware vai para o `amp-link` agora ou depois deste aparelho?

## Registro dos fios

Cada fio soldado no aparelho, onde e quando. Para desfazer, dessoldar na ordem inversa.

| Data | Fio | Onde | Observação |
|---|---|---|---|
| 2026-11-16 | Preto | `CB701`, cima 5ª (`DGND`) | Conferido com o bip: sem curto |
| 2026-11-16 | Cinza | `CB701`, cima 8ª (`FL_/CS`) | Metade da malha não pegou solda: fios soltos cortados, fio preso com fita, bip até a janela 1 do `CB304` ok. Redone before closing the case (2026-11-16) |
| 2026-11-16 | Laranja | `CB701`, cima 7ª (`FL_CLK`) | Idem |
| 2026-11-16 | Verde-azulado | `CB701`, baixo 7ª (`FL_DATA`) | Idem |
| 2026-11-16 | Amarelo | `CB701`, baixo 6ª (`FL_/RST`) | Idem |
| 2026-11-16 | Roxo | `U701`, perna C (saída) | Idem |
