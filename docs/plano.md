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
- Fios do Pico soldados numa extensão do flat, nunca na placa da Yamaha.

## Objetivos

1. **Saber o estado**: tocando, pausado ou parado, faixa, tempo, disco presente, bandeja, modo CD ou USB, PURE DIRECT.
2. **Comandar pelo Wi-Fi**, com os códigos do controle remoto por fio.
3. **Compartilhar o estado** com os outros aparelhos, pelo mesmo contrato dos amps.
4. Depois: escrever no display e o que mais valer a pena da lista de ideias.

## Fases

**Fase 1: ler e comandar.** O Pico escuta as quatro vias do display, sem cortar nada, e manda os códigos do controle
remoto. Diferente dos amps, o comando já entra na fase 1: os códigos estão no manual e a ligação é um fio só.

**Fase 2: escrever no display.** O Pico no meio da via `FL_DATA` (e das outras três, se for preciso), entre duas
extensões do flat. Só vale a pena se a fase 1 mostrar o que há para ganhar (ver "Ideias").

## Ligar e desligar

O botão da frente é uma chave nos 230 V (`SW801`), e o controle remoto não tem tecla de ligar. Com o aparelho
desligado, o Pico está desligado, e nada pelo Wi-Fi o liga. Três saídas:

| Saída | O que muda | Custo |
|---|---|---|
| **A. Aceitar** | O Pico vive enquanto o aparelho está ligado. A ponte some da rede quando ele desliga, e o hub entende isso como "desligado" | Nenhum |
| **B. Tomada inteligente** | O botão fica sempre apertado, e uma tomada Wi-Fi liga e desliga o aparelho. O hub comanda a tomada | Uma tomada; nada dentro do aparelho |
| **C. Relé dentro do aparelho** | Uma fonte pequena de 5 V sempre ligada para o Pico e um relé no lugar da chave | Mexe nos 230 V, dentro de um aparelho sem terra |

**Recomendação: começar com A e passar para B** se ligar pelo Wi-Fi fizer falta. A saída C repete o que foi
recusado no MR 780 (fonte nova dentro do aparelho) e é a única com risco de choque. A decisão é do dono.

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
- O flat com uma régua ao lado, para confirmar o passo de 1,25 mm.

## Passo 2: multímetro

Com o aparelho ligado, contra o `DGND` (via 1 ou 9 do flat):

1. As 15 vias do flat, conferindo com a tabela de `docs/pesquisa.md`. Qualquer via acima de 3,4 V para tudo. Medir
   nas janelas do `CB304`, na placa principal, que deixam o contato de cada via à mostra. Guiar-se pelos nomes da
   serigrafia: os números das vias se invertem entre as duas placas.
2. A saída do receptor `U701`, em repouso (esperado: 3,3 V).
3. O `D+5` no `CB301` da placa principal, ao lado do flat: a tensão, e a temperatura do dissipador do `IC801` (na
   fonte) depois de meia hora tocando. O Pico vai pedir mais uns 50 a 100 mA dessa linha.
4. O `+B2`, no mesmo conector: alternativa para alimentar o Pico por um regulador próprio, se o `D+5` não tiver
   folga.

Medir também o passo e a largura do flat de 15 vias (esperado: 1,25 mm), para comprar a extensão (duas, para a
fase 2) e flats de reserva dos dois tipos, como no MR 780.

Anotar em `docs/medicoes.md`.

## Passo 2b: teste de interferência do Wi-Fi

O mesmo teste do MR 780 (`mr780-mod/docs/plano.md`, passo 2b): o Pico num saquinho, alimentado por power bank,
transmitindo sem parar, perto de cada placa. Aqui o que se ouve é a saída analógica, com o disco em pausa e o volume
do amp alto. Os pontos sensíveis são o DAC, os amplificadores de saída e o leitor óptico (erros de leitura em vez de
ruído: ver se o disco pula). Anotar também o RSSI com a tampa fechada.

## Passo 3: analisador lógico

Com o LogicAnalyzer do SP103 (`logicanalyzer-sp103`), nas vias `FL_/CS`, `FL_CLK`, `FL_DATA`, `FL_/RST` e `REM`.

Display:

- Ligar o aparelho, sem disco e com disco (`LOADING`, `NO DISC`, o total de faixas e de tempo).
- Play, pause, stop, próxima, anterior, avançar e voltar.
- A tecla DISPLAY (tempo da faixa, restante, total) e o DIMMER.
- REPEAT, RANDOM, PROGRAM, A/B, PURE DIRECT.
- Abrir e fechar a bandeja.
- Um CD com CD-Text e um pendrive com MP3 (nomes de arquivo e de pasta, FOLDER).

O que as capturas precisam responder:

- O protocolo do vidro: velocidade, ordem dos bits, comandos.
- **O microcontrolador manda letras ou pontos?** Decide como é o leitor de telas.
- Como os ícones (grades 13 e 14) são acesos: é deles que saem play, pause e os modos.
- De quanto em quanto tempo o display é reescrito (o tempo corre de segundo em segundo).

Controle remoto: uma tecla basta para confirmar o formato (NEC?) e o código de cliente `79`. O resto vem da tabela do
manual.

Uma captura à parte, só de escuta, no `232C_TX` da porta da traseira: ver se o aparelho fala algo sozinho.

Documentar em `docs/descobertas-protocolo.md`, com as capturas em `captures/`.

## Passo 4: o programa

1. **A base da ponte**: Wi-Fi sem cabo pela rede `AmpLink-CDS300-XXXX`, descoberta e atualização pelo Wi-Fi, com o
   `/state` todo `null`. **Escrita em 2026-11-16**, testada só no computador.
2. O `/device` do CD-S300. **Escrito em 2026-11-16**, com `kind` e `keys`, que são a proposta do `api` 2.
3. O envio dos códigos do controle remoto, e o `/control`. **Escrito em 2026-11-16**: as 30 teclas da tabela do
   manual, em NEC 79/86, conferidas bit a bit com o modelo do `groove-rig`. O PIO que move a linha é o do SP103.
   Falta: rodar num Pico, ligar o fio na saída do receptor e ver o aparelho obedecer. Os tempos são os do padrão
   NEC, não medidos neste aparelho.
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

**O nome.** A rede de configuração `AmpLink-…` e a pergunta `AMPLINK?` continuam, mesmo com um CD player. Trocar
custa mexer na app e nas duas pontes que já existem, sem ganho de função. A decisão é do dono.

## Ideias

Além do básico (estado e comandos). A coluna "Depende de" diz o que precisa existir antes.

| Ideia | O que é | Depende de |
|---|---|---|
| Ligar o amp junto | Play no CD liga o amp e escolhe a entrada CD; outra entrada no amp ou standby pausa o CD | Fase 1 e o ponto central |
| Reconhecer o disco | Ao carregar, o aparelho mostra o número de faixas e o tempo total. O par serve de chave na coleção (`groove-catalog`): o disco é nomeado uma vez e reconhecido sempre | Fase 1 |
| Título no display | O nome da faixa, vindo do catálogo, rolando nos 12 caracteres, para discos sem CD-Text | Fase 2 e a ideia anterior |
| "Tocando agora" e histórico | O `groove-display` mostra o disco e a faixa; o groove guarda o que foi tocado | Fase 1 |
| Texto do disco e do pendrive | CD-Text e nomes de arquivo e de pasta, remontados da rolagem do display | Fase 1 |
| Faixa direta, programa, A-B | Pela app, com as teclas numéricas do controle, sem o controle na mão | Fase 1 |
| Timer de desligar e despertador | Parar depois de N minutos; tocar numa hora marcada | Fase 1 (o despertador depende de "Ligar e desligar") |
| Horas de uso | Tempo total tocando, guardado no Pico: a idade do laser | Fase 1 |
| Saúde do disco | Contar os erros de leitura (`C2_Flag`, pino 31 do `IC305`): disco riscado ou laser fraco | Um fio a mais na placa principal |
| Bandeja | Saber se está aberta (`OPSW`, `CLSW`) sem depender do display | Dois fios a mais, só se o display não bastar |
| Fonte do VU dos amps | O Pico lê o S/PDIF (3,3 V, na entrada do `IC4`) e publica o nível do áudio. O CD player vira a fonte do VU do SP103 e do MR 780, no lugar do relay | A estudar: não foi verificado se o Pico dá conta de ler S/PDIF junto com o resto |
| Volume na saída | O DAC PCM1780 tem atenuador digital, comandado por três fios. O Pico poderia ajustar o nível | A estudar: disputa os três fios com o microcontrolador e mexe no caminho do som |
| Relógio com o aparelho parado | O display mostra a hora em vez de `NO DISC` | Fase 2 |

## Perguntas em aberto

- Ligar e desligar: A, B ou C?
- O nome `AmpLink` fica?
- A base comum do firmware vai para o `amp-link` agora ou depois deste aparelho?
- O que mostrar no display na fase 2, se ela for feita.
