# Handoff — Documentação Final ES2 (EduHub)

Contexto para retomar o trabalho numa próxima sessão. Última atualização: 28/08/2026.

## O que é

Documento final da disciplina **Engenharia de Software II** (UNESP Bauru), projeto **EduHub**
(sistema de gestão educacional). O documento final (LaTeX) foi preenchido a partir de um
modelo `.tex` fornecido pela disciplina, usando o conteúdo do documento de ES1 e, na segunda
rodada, os diagramas C4 e os slides de apresentação da equipe.

**Integrantes:** Arthur Alves Ribeiro Gordo (241024293), Caio César Souza Oliveira (241025702),
Davi Ferreira de Souza (241024676), Mário Masao Mukai (241022321).

## Arquivos-fonte (pasta pai `../`)

- `Documentação_do_Projeto_de_Software.zip` — modelo `.tex` original da disciplina (template + `refs.bib` + imagens).
- `EduHub.docx-5.pdf` — documento de ES1 (44 págs): requisitos, histórias de usuário, casos de uso,
  processo (Scrumban), qualidade/métricas. Foi a fonte de conteúdo original.
- `C4/` — diagramas produzidos pela equipe: `contexto.png`, `container.png`, `componentes.png`
  (C4 Níveis 1/2/3), `registro academico.png` e `autenticacaoeacesso.png` (diagramas de classes UML
  dos componentes Registro Acadêmico e Autenticação e Acesso).
- `slide/eduhub_empacotamento.pdf` — slides da apresentação (C4, empacotamento e **SOLID** aplicado
  ao componente Registro Acadêmico: SRP, OCP, DIP). Foi a fonte da Seção 3.3.
- `Telas Finais/` — protótipos de alta fidelidade do Figma (PNG), fluxo do CU-03, nas versões
  **desktop** (`Desktop - *.png`, 1440x1024) e **mobile** (nomes sem prefixo, 402x874). Foi a fonte
  das figuras do Cap 4 (copiadas e renomeadas para `images/tela-cu03-*`).

## Estrutura desta pasta (`documentacao-final/`)

```
main.tex                 preâmbulo + capa + \input dos capítulos (\orientacoesfalse)
                         define \comparativotela{desktop}{mobile}{legenda}{label} (par de telas lado a lado)
refs.bib                 NÃO É MAIS USADO (bibliografia removida, ver abaixo)
chapters/
  ch1.tex                Cap 1 — Introdução e Objetivos
  ch2_ch3.tex            Cap 2 Arquitetura + Cap 3 Projeto de Componentes
  ch4_ch5_ch6.tex        Cap 4 Interface + Cap 5 Testes + Cap 6 Gestão de Config + Controle de Versões
  appendix.tex           Apêndice A — Especificação Detalhada de Requisitos (45 RF, 10 RNF, 18 HU, 3 CU)
images/
  AV01A.jpg                        logo UNESP (capa)
  01_2_iso-25010-topics-EN.drawio.png  figura ISO 25010 (Cap 1)
  c4-contexto.png                  C4 Nível 1 — contexto (Fig 2.1)
  c4-container.png                 C4 Nível 2 — contêineres (Fig 2.2)
  c4-componentes.png               C4 Nível 3 — componentes do Backend (Fig 2.3)
  classes-autenticacao-acesso.png  diagrama de classes do componente Autenticação e Acesso (Fig 3.1)
  classes-registro-academico.png   diagrama de classes do componente Registro Acadêmico (Fig 3.2)
  diagrama-classes.png             (ex-diagrama total do EduHub) — NÃO É MAIS USADO
  diagrama-cu01.png / diagrama-cu02.png  diagramas de caso de uso (Apêndice)
  tela-cu03-01..08-*.png           telas do fluxo CU-03 no Cap 4 (8 pares desktop + mobile):
                                   01 login, 02 home professor, 03 notas aberto, 04 frequência,
                                   05 home coordenação, 06 período aberto, 07 período bloqueado,
                                   08 notas bloqueado. Cada uma tem par `-mobile.png`.
padroesProjeto.md        análise de Design Patterns (GoF) que encaixam no EduHub — só estudo, NÃO entra no .tex
EduHub_Documentacao_Projeto_v1.0.pdf  PDF v1.0 antigo (38 págs) — desatualizado
main.pdf                 build atual (45 págs)
```

## Como compilar

**Mudou:** agora há TeX Live disponível nesta máquina (`latexmk` e `pdflatex` em `/usr/bin`). O
caminho mais simples passou a ser:

- **`latexmk -pdf -interaction=nonstopmode main.tex`** — compila direto, resolve as passagens de
  referência sozinho. Foi o usado nas últimas sessões.

Alternativas (caso o TeX Live suma):

- **tectonic 0.15.0** (última versão compatível com glibc 2.35): baixar de
  `https://github.com/tectonic-typesetting/tectonic/releases/download/tectonic%400.15.0/tectonic-0.15.0-x86_64-unknown-linux-gnu.tar.gz`,
  extrair e rodar `./tectonic -X compile main.tex`. (tectonic ≥0.16 não roda por glibc 2.35.)
- **Overleaf:** subir a pasta inteira, definir `main.tex` como principal, compilar (pdfLaTeX).

Validação visual: `pdftoppm -png -r 100 -f <ini> -l <fim> main.pdf out` e abrir os PNGs.

## Estado atual

- Documento compila **sem erros nem referências indefinidas**. PDF atual = **50 páginas**.
- Restam 6 overfull `\hbox` >15pt, todos **pré-existentes** (§3.3 e apêndice, por identificadores
  `\texttt` longos que não hifenizam). Nenhum introduzido nas edições recentes.
- Conteúdo dos Caps 1–6 revisado e coerente entre si.
- **§3.2** detalha dois diagramas de classes, na ordem: Autenticação e Acesso (**Fig 3.1**,
  `classes-autenticacao-acesso.png`) e Registro Acadêmico (**Fig 3.2**, `classes-registro-academico.png`).
  Em cada componente a ordem é **regras → figura → explicação do diagrama** (diagrama antes do texto).
- **Cap 4 §4.3 preenchido com as telas do CU-03:** 8 etapas, cada uma com a versão **desktop à
  esquerda e mobile à direita** (via `\comparativotela`), da autenticação ao efeito da trava.
- **Cadeia Gestão de Configuração ↔ Testes agora amarrada:** §6.1 (repositório + branches) →
  §6.4 (CI/CD por ambiente) → §5.5 (testes rodando nessa esteira), ligadas por `\ref` cruzado.

## Convenções de estilo já aplicadas (manter em edições futuras)

Aplicadas em Cap 1 §1.3, Cap 2 inteiro, Cap 3 §3.1–3.4, **Cap 5 e Cap 6 (travessões removidos)**:

- **Sem travessões** (`---`/`--` como aparte) no meio de frases — usar vírgula, dois-pontos,
  parênteses ou dividir a frase. (Os `--` de legenda/`\caption` são separadores de título e ficam.)
- **Sem `;`** no meio de frase em prosa — usar vírgula/ponto, ou virar `itemize`.
- **Negrito só em rótulo de tópico/item de lista ou cabeçalho de tabela**, nunca para ênfase no meio da frase.
- Primeiro parágrafo após título com recuo (pacote `indentfirst`).
- **Nada de "hedge"** do tipo "a ferramenta ainda será definida pela equipe" para coisas que já
  foram decididas (repositório = GitHub, CI/CD = GitHub Actions, branches = Git Flow).
- **A especificação de requisitos (ES1) é trabalho da PRÓPRIA EQUIPE, não fonte externa.** Não usar
  "da fonte", "conforme a fonte", "o Documento de Especificação de Requisitos define/estabelece...".
  Requisitos detalhados (RF/RNF/HU/CU) estão no **Apêndice A** (`\ref{apx:requisitos}`): citar por ID
  ou apontando pro apêndice. Personas/sprints/métricas **não** estão no apêndice: reescrever como
  "definido pela equipe na etapa de requisitos". (O "fonte" do Cap 1 é "fonte de dados do sistema",
  outro sentido, fica.) Varredura: `grep -riE "d[ae] fonte" chapters/` deve dar zero.

## Pacotes adicionados ao `main.tex` (não remover sem entender o efeito)

- `indentfirst` — recuo no primeiro parágrafo de cada seção.
- `placeins` com opção `[section]` — barra floats na fronteira de cada `\section`. Só barra em
  `\section`, não em `\subsection` (por isso o apêndice usa `[H]`, ver abaixo).
- `float` — habilita o especificador `[H]` (posição fixa). Usado na Tabela de módulos (§2.3),
  na Figura de classes de Autenticação (§3.2) e em **todas as tabelas de RF/RNF do apêndice**.
- `listings` — blocos de código Java do §3.4 (padrões de projeto). Config em `\lstset`. **Comentários
  de código sem acentos** para evitar conflito de UTF-8 com o `listings`.
- `tabularx` / `xltabular` — tabelas com coluna elástica `X`; `xltabular` quebra entre páginas (apêndice).

## Decisões e detalhes técnicos (para não repetir trabalho)

- **Bibliografia REMOVIDA.** As duas citações (`arc42`, `roos2023`) sustentavam uma frase metodológica
  do Cap 2 que foi retirada. `\bibliography` removido do `main.tex`; `refs.bib` continua no disco sem uso.
- **C4 e "sistema externo".** Único sistema externo = **Serviço de E-mail** (notificações, RF-36),
  isolado no componente Adaptador de E-mail. Sem legados nem gateways de pagamento. Cap 2 e §2.4 refletem isso.
- **§3.1** — tabela de componentes alinhada aos **8 componentes** reais do C4.
- **§3.2** (`\label{sec:detalhamento}`) — detalha **dois componentes**, Autenticação e Acesso (Fig 3.1,
  fixada com `[H]`) e Registro Acadêmico (Fig 3.2). NÃO juntar componentes num bloco fictício. O
  diagrama de classes TOTAL (`diagrama-classes.png`) foi removido.
- **§3.3** — SOLID (SRP, OCP, DIP) em dois componentes. **Ordem = Autenticação e Acesso primeiro,
  depois Registro Acadêmico** (batendo com a ordem da §3.2). Fecho cita LSP e ISP como os restantes.
- **§3.4** — "Padrões de projeto": Strategy/Adapter/Observer/Proxy (problema + código `listings`).
  Primeiro parágrafo começa direto no projeto de classes (a frase sobre "o SRS não prescreve padrões"
  foi removida). Base de análise: `padroesProjeto.md`.
- **§4.3** — escopo de protótipos **reduzido ao fluxo do CU-03** (Finalizar e Bloquear Período de
  Lançamento), o mais crítico (Registro Acadêmico + trava RF-26). Tabela 4.1 tem **4 telas** (T-01
  login, T-02 lançamento de notas, T-03 frequência, T-04 gestão/travamento de períodos). As telas
  **já foram inseridas** (Figma, alta fidelidade): §4.3.1 explica o fluxo escolhido e as subseções
  §4.3.2–§4.3.6 mostram o passo a passo, cada figura com **desktop + mobile lado a lado**. Perfil de
  T-04 = **Coordenação** (bate com o CU-03 do apêndice: "Administrativo ou Coordenador"). Demais CUs
  ficam para próximas iterações. Só as telas desktop+mobile do CU-03 entraram; não usar as demais.
- **Regra de fechamento de período = Modelo B (decidido pelo Masao, 28/08).** A Coordenação bloqueia
  o período **a qualquer momento**; se houver disciplinas com notas/frequência pendentes, o sistema
  apenas **sinaliza como aviso**, não impede o bloqueio. Correção depois do bloqueio: o **professor
  solicita o desbloqueio** à Coordenação, que reabre via "Desbloquear Período", corrige e bloqueia de
  novo. Isso **substituiu** a regra antiga ("só bloqueia com tudo 100% concluído"). Aplicado em 3
  lugares, manter coerentes: **Apêndice CU-03** (fluxo principal + alt. 7.a de desbloqueio + pós-cond.),
  **§3.2** (item de RF-26 do Registro Acadêmico) e **§4.3** (enumerate do fluxo + parágrafo da T-04).
  Não há tela de "pedido de desbloqueio" prototipada; descrito só em texto (quem executa o desbloqueio
  é a Coordenação, a pedido do professor).
- **§5.5** — automação de teste amarrada ao **GitHub Actions** (esteira de CI, `\ref{sec:build-cicd}`),
  acionada a cada commit/PR. Framework de teste específico fica dependente da linguagem escolhida
  (exemplos do §3.4 estão em Java; linguagem não foi cravada de propósito).
- **§6.1** (`\label{sec:config-repo}`) — **Taiga** para gestão do Scrumban e **GitHub** como
  repositório central (Git como controle de versão). Inclui **modelo de branches (Git Flow simplificado)**:
  `main` (produção), `develop` (base da homologação), `feature/*` via PR revisado, promoção `develop`→`main`.
- **§6.4** (`\label{sec:build-cicd}`) — **CI/CD via GitHub Actions**: CI a cada commit/PR (build +
  testes unidade/integração do Cap 5 + análise estática, com portão no merge à `develop`); CD por
  ambiente (`develop`→homologação, `main`→produção). Referencia o modelo de branches do §6.1.
- **Apêndice** — corrigidos dois problemas de layout: (1) coluna "Prioridade"/"Estimativa" alargada
  (era `p{0.10}`, header colava no vizinho) para `p{0.14\textwidth}`; (2) tabelas de RF/RNF fixadas
  com **`[H]`** (antes `[ht]` flutuavam para longe do subtítulo). `xltabular` e figuras de CU intactas.
- `xltabular` (apêndice) e a proibição de `\url` aninhado no `refs.bib` continuam válidos, caso a bibliografia volte.
- Referências cruzadas de capítulo hardcoded ("Capítulo 4", etc.) conferidas e ainda batem com a ordem de `\input`.

## Concluído nesta sessão (28/08)

- **Cap 4 §4.3 — telas do CU-03 inseridas.** Copiei as 8 telas desktop + 8 mobile de `Telas Finais/`
  para `images/tela-cu03-*`. Reescrevi a §4.3: §4.3.1 explica o fluxo escolhido, §4.3.2–§4.3.6 fazem
  o walkthrough (login → notas aberto → frequência → gestão de período → bloqueio → efeito da trava).
- **Comparativo desktop|mobile.** Cada figura mostra as duas versões lado a lado, via o novo comando
  `\comparativotela` (definido no `main.tex`, larguras 0.70 / 0.24 `\textwidth` calibradas p/ altura igual).
- **Intro do Cap 4 reescrita** (1º parágrafo): a especificação de requisitos passa a ser tratada como
  trabalho anterior **da própria equipe**, não fonte externa.
- **§3.2 reordenada:** diagrama de classes agora vem **antes** da explicação, nos dois componentes.
- **§3.3:** removida a pergunta retórica que estava no meio da prosa (virou afirmação).
- **Citações à "fonte" eliminadas** em todo o documento (ver convenção nova acima). RF/RNF/HU/CU →
  Apêndice A; personas/sprints/métricas → "definido pela equipe".
- **Regra de bloqueio → Modelo B** (ver decisão acima): reescrita no **Apêndice CU-03**, na **§3.2**
  e na **§4.3**.
- Trabalho feito por 3 subagentes (um por arquivo: `ch2_ch3.tex`, `ch4_ch5_ch6.tex`, `appendix.tex`)
  e validado centralmente. Compila limpo, 50 págs, zero refs indefinidas.

## Concluído nesta sessão (27/08)

- **§3.3** — invertida a ordem SOLID para Autenticação → Registro (alinha com §3.2).
- **§3.4** — reelaborado o primeiro parágrafo (removida a frase sobre o SRS não prescrever padrões).
- **§6.1** — GitHub como repositório + modelo de branches (Git Flow) + label `sec:config-repo`.
  Removidos os hedges "não especifica ferramenta" e "independentemente da ferramenta escolhida".
- **§6.4** — detalhado CI/CD por ambiente no GitHub Actions + label `sec:build-cicd`. Removida a
  frase confusa "a fonte não descreve um processo formal de build ou integração contínua".
- **§5.5** — automação de teste amarrada ao GitHub Actions (referência cruzada para §6.4).
- **Tabela 6.1** (rastreabilidade) — 2ª coluna virou `X` (bem mais larga), "Sprint" fixada estreita.
- **Cap 5 e Cap 6** — removidos todos os travessões de aparte em prosa.
- **Apêndice** — corrigida sobreposição de colunas (Prioridade/Estimativa) e reposicionadas as
  tabelas com `[H]` (inclui a Tabela A.12, `xltabular` de 5 colunas).
- **§4.3** — protótipos reduzidos ao fluxo do CU-03 (17 telas → 4). PDF caiu de 46 para 45 páginas.

## Pendências / próximos passos

1. **Versionar o documento para v1.1.** A tabela "Controle de Versões do Documento" (fim do
   `ch4_ch5_ch6.tex`) ainda diz **v1.0 (25/08)**, mas houve muitas mudanças de conteúdo desde então
   (§3.3, §3.4, §5.5, §6.1, §6.4, apêndice, travessões, **telas do CU-03 no Cap 4**, **reordenação da
   §3.2**, **citações reenquadradas**, **regra de bloqueio → Modelo B**). Adicionar linha v1.1 resumindo.
2. ~~Protótipos de tela (Figma)~~ — **FEITO** (28/08): 4 telas do CU-03, desktop + mobile, no Cap 4.
3. **Diagrama de classes de `Gestão de Usuários`** (opcional) — terceiro componente detalhado no §3.2,
   mesmo padrão das Figs 3.1/3.2.
4. **Cosméticos menores:**
   - §1.1.3 diz "não requer interfaces operacionais **em tempo real** com sistemas externos" — o
     qualificador "em tempo real" torna aceitável (e-mail é assíncrono), mas é o ponto de maior
     tensão residual com o Cap 2. Reavaliar se quiser precisão total.
   - Aspas retas `"..."` pré-existentes em algumas seções renderizam tortas (trocar por ``...'').
   - Pequenos overfull `\hbox` (<15pt) no apêndice e no §3.3.
