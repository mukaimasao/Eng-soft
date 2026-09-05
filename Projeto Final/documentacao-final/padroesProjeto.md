---
name: padroes-projeto-eduhub
description: Análise de quais Design Patterns (GoF) encaixam bem no sistema EduHub, componente a componente, com nível de aderência honesto.
tags: [design-patterns, es2, eduhub, arquitetura, estudo]
metadata:
  type: reference
---

# Padrões de Projeto que encaixam no EduHub

Análise do sistema **EduHub** (gestão educacional, disciplina ES2) à luz dos padrões
GoF apresentados no material da disciplina. Documento de estudo — **não** faz parte do
`.tex` da documentação. Relacionado: [[handoff]].

> **Escopo:** isto **não** é um plano de implementação. O objetivo é só apontar quais
> padrões de projeto se encaixam bem nos problemas do EduHub e explicar o porquê, para
> raciocinar sobre o sistema e para a prova. Os trechos de código são apenas esboços de
> estrutura, para mostrar *por que* o padrão encaixa, não código a ser escrito.

O material avisa, e vale como régua desta análise:

> **Não force o problema a caber no padrão.** Primeiro entenda o problema (contexto +
> forças + consequências), depois veja qual padrão responde a ele.

Por isso cada padrão está classificado por **aderência ao problema real do EduHub**:

- 🟢 **Encaixe natural** — o problema está claramente no sistema e o padrão é a resposta
  canônica para ele. Alguns já aparecem no diagrama de classes.
- 🟡 **Encaixe plausível** — dá para enxergar o padrão em um componente, mas depende de como
  a funcionalidade se comporta. Encaixa como leitura, não como obrigação.
- 🔴 **Encaixe forçado** — "parece", mas o problema real não pede o padrão. Citar aqui só
  para justificar por que **não** se aplica.

> **Nota sobre Service Layer e Repository:** eles aparecem nos diagramas de classes
> (`...Service`/`...ServiceImpl` e `...Repository`), mas são padrões de **arquitetura**
> (catálogo do Fowler), **não** padrões GoF. Por isso ficam fora desta análise, que trata
> só dos padrões do material. Servem de vocabulário quando você for justificar os demais.

---

## Mapa rápido: componente → padrão

| Componente (RFs) | Padrão | Aderência |
|---|---|---|
| Registro Acadêmico (RF-21–27) | **Strategy** (`TipoAvaliacao`) | 🟢 já no diagrama |
| Autenticação e Acesso (RF-01,02,05–10) | **Strategy** (`Metodo2FA`) | 🟢 já no diagrama |
| Adaptador de E-mail (RF-36) | **Adapter** | 🟢 |
| Mensageria e Comunicação (RF-35–41) | **Observer** | 🟢 |
| Autenticação — controle de permissão (RF-07, RF-21) | **Proxy** de proteção | 🟢 |
| Autoatendimento do Aluno (RF-28–34) | **Facade** | 🟡 |
| Relatório e Auditoria — logs (RF-42–45) | **Singleton** (logger) | 🟡 |
| Relatório e Auditoria — exportação (RF-42) | **Factory Method** / Fábrica | 🟡 |
| Autenticação — hierarquia de cargos (RF-08) | **Composite** | 🔴 |
| Qualquer listagem (alunos, notas, mensagens) | **Iterator** | 🔴 |

---

## 🟢 Encaixe natural

### Strategy — já aparece no diagrama, duas vezes

O EduHub **já expressa Strategy em dois pontos do projeto de classes**, o que torna esse o
encaixe mais fácil de defender: dá para apontar o padrão no próprio diagrama.

1. **`TipoAvaliacao`** (Registro Acadêmico): interface com `calcularNotaFinal()` e
   `exigePresencaMinima()`, com `AvaliacaoProva` e `AvaliacaoTrabalho` como concretas.
2. **`Metodo2FA`** (Autenticação): interface com `gerarCodigo()` e `validarCodigo()`, com
   `TwoFactorEmail` e `TwoFactorApp` como concretas.

**Problema que resolve:** existem vários comportamentos intercambiáveis para a mesma
operação (calcular nota de prova vs. de trabalho; validar 2FA por e-mail vs. por app). A
alternativa sem padrão seria um `if/switch` por tipo dentro do serviço.

**Forças:** flexibilidade (acrescentar um tipo novo sem tocar no existente) contra
simplicidade (mais classes). No EduHub novos tipos são esperados, então a flexibilidade
justifica o padrão.

**Ligação com princípios:** é o **OCP** na prática — aberto para extensão (nova classe
concreta), fechado para modificação (o serviço não muda). Já está redigido assim no §3.3.

```java
interface TipoAvaliacao {                 // a "estratégia"
    double calcularNotaFinal(double nota);
    boolean exigePresencaMinima();
}
class AvaliacaoProva    implements TipoAvaliacao { /* ... */ }
class AvaliacaoTrabalho implements TipoAvaliacao { /* ... */ }
// AvaliacaoSeminario entraria como mais uma concreta, sem alterar o serviço.
```

### Adapter — o componente "Adaptador de E-mail" É um Adapter

Encaixe mais direto do sistema: **o próprio nome do componente é o padrão**.

**Contexto:** o EduHub envia notificações (RF-36), mas depende de um **serviço de e-mail
externo** (a única integração externa do sistema, segundo o Cap 2). Esse serviço tem a API
dele — algo como `send(from, to, subject, body)` — que não é a interface que o resto do
sistema quer chamar.

**Problema:** o sistema pensa em "notificar o aluno", não em falar SMTP. As interfaces são
incompatíveis e o serviço externo é de terceiros, não pode ser alterado. É o mesmo caso dos
projetores do material (`turnOn()`/`enable()` vs. `liga()`).

**Forças:** manter o EduHub desacoplado do provedor concreto (trocar de provedor sem
espalhar mudança) contra não deixar detalhe de e-mail vazar para o código de negócio.

**Esboço de estrutura (por que encaixa):**

```java
interface Notificador { void notificar(Usuario dest, String assunto, String corpo); }

class AdaptadorEmail implements Notificador {          // adapta a interface interna...
    private final ServicoEmailExterno externo;         // ...para a API de terceiros
    public void notificar(Usuario d, String a, String c) {
        externo.send("no-reply@eduhub", d.getEmail(), a, c);   // TRADUZ a chamada
    }
}
```

**Como reconhecer:** "tenho um serviço/classe externo que não posso modificar e preciso
encaixá-lo na interface que meu sistema espera" → **Adapter**.

**Adapter × Facade (não confundir):** Adapter = *compatibilidade* (uma interface vira
outra). Facade = *simplificação* (esconder um subsistema complexo). Aqui é compatibilidade.

### Observer — Mensageria e notificações

**Contexto:** vários eventos do EduHub geram avisos para vários interessados. Ex.: um
comunicado é publicado pela administração (RF-35), uma nota é lançada, um período é travado
(RF-26). Quando isso ocorre, é preciso gravar na caixa de entrada do aluno (RF-37), disparar
e-mail (RF-36) e, no futuro, avisar uma tela mobile.

**Problema:** se quem gera o evento chamar direto `caixaEntrada.gravar()`, `email.enviar()`,
`mobile.push()`, ele fica acoplado a cada canal e cada canal novo obriga a mexer nele. É o
mesmo caso do `Temperatura → Termometro` do material.

**Forças:** desacoplar o produtor do evento dos consumidores (relação 1:N) e permitir
adicionar/remover canais.

**Esboço de estrutura:**

```java
class EventoAcademico extends Subject {       // Subject 1:N
    void publicarComunicado(Comunicado c) { this.comunicado = c; notifyObservers(); }
}
class CanalCaixaEntrada implements Observer { public void update(Subject s){ /* grava */ } }
class CanalEmail        implements Observer { public void update(Subject s){ /* usa o Adapter de e-mail */ } }
```

Repara que **Observer e Adapter se combinam** aqui: o `CanalEmail` (Observer) usaria o
Adaptador de E-mail por baixo. Bom ponto para mostrar domínio na prova.

**Observer × Strategy:** Observer = *notificar vários quando algo muda*. Strategy = *trocar
um algoritmo*. Mensageria é notificação → Observer.

**Observer × Publish/Subscribe:** se o roteamento por tag (RF-38) um dia passar por um
broker/fila, vira Pub/Sub (com intermediário). Enquanto for chamada direta Subject→Observers,
é Observer clássico.

### Proxy de proteção — controle de acesso

**Contexto:** RF-21 diz que o professor só acessa notas das turmas às quais está vinculado;
RF-07 restringe quem altera cargos. O acesso a recursos protegidos depende de permissão
(via `verificarPermissao`).

**Problema:** espalhar `if (usuario.temPermissao(...))` dentro de cada método de negócio
mistura regra de acesso com regra de domínio.

**Esboço de estrutura:** um objeto que implementa a **mesma interface** do serviço real,
checa a permissão e só então delega.

```java
class RegistroAcademicoProxy implements RegistroAcademicoService {
    private final RegistroAcademicoService real;
    private final AutenticacaoService acesso;
    public Nota registrarNota(int alunoId, int discId, double v, TipoAvaliacao t) {
        if (!acesso.verificarPermissao(professorAtual(), "LANCAR_NOTA")) throw new AcessoNegado();
        return real.registrarNota(alunoId, discId, v, t);        // delega ao real
    }
}
```

**Como reconhecer:** "quero controlar/interceptar o acesso a um objeto sem mudar o objeto"
→ **Proxy**. (Se fosse *simplificar* o acesso, Facade; se fosse *adaptar* a interface, Adapter.)

---

## 🟡 Encaixe plausível (depende de como a funcionalidade se comportar)

### Facade — Autoatendimento do Aluno

**Contexto:** o Autoatendimento (RF-28–34) monta boletim, frequência detalhada, grade e
calendário, lendo de vários componentes: Registro Acadêmico (notas, faltas), Estrutura
Escolar (turmas, horários) e Gestão de Usuários (perfil).

**Encaixe:** se essa orquestração de vários módulos ficar complexa, uma **Facade**
(`AutoatendimentoService` com `montarBoletim(alunoId)`) faz sentido para dar ao cliente um
ponto de entrada simples e esconder os subsistemas. Se o boletim lê de poucos lugares, a
leitura de Facade é fraca — o padrão só se paga com complexidade real por trás.

### Singleton — logger de auditoria

**Contexto:** Relatório e Auditoria registra logs de alteração (RF-44/RF-45). Um **único**
ponto de escrita de log, acessível de qualquer componente, é o exemplo `Logger` do material.

**Ressalva do próprio material:** Singleton controla *quantidade de instâncias*, não é
"classe estática", e cria estado global que atrapalha teste isolado. Em sistema web com
injeção de dependência, esse "único" costuma ser resolvido pelo container (escopo singleton),
não escrito à mão. Encaixa conceitualmente, mas é o padrão a citar com mais cautela.

### Factory Method / Fábrica — exportação de relatórios

**Contexto:** Relatório e Auditoria exporta relatórios (RF-42), plausivelmente em formatos
diferentes (PDF, CSV, XLSX).

**Encaixe:** centralizar a criação do exportador evita `new ExportadorPDF()` espalhado. Se
o formato varia num único ponto de decisão, uma **Fábrica estática** já basta; só vira
**Factory Method** se a escolha do produto precisar variar por subclasse/polimorfismo.
Enquanto for um `switch(formato)` num lugar só, a fábrica simples é a leitura mais fiel.

---

## 🔴 Encaixe forçado (não se aplica de verdade)

- **Composite — hierarquia de cargos (RF-08):** `Cargo` tem `nivelHierarquia`, o que *parece*
  árvore. Mas o requisito é só um `int` de nível, não uma árvore de cargos-dentro-de-cargos
  tratados de forma uniforme. Composite só se aplicaria se um cargo *contivesse* outros
  cargos e você quisesse tratar um cargo e um grupo com a mesma interface. Não é o caso.
- **Iterator — listagens:** percorrer listas de alunos/notas/mensagens já é resolvido pela
  linguagem (`Iterable`/`for-each`). Iterator próprio só faria sentido para esconder uma
  estrutura interna exótica, o que o EduHub não tem.

---

## Como usar isto na prova

O material cobra **padrão + justificativa baseada no problema**, não o nome solto. Roteiro:

1. **Categoria** — o problema é de *criação*, *estrutura* ou *comportamento*?
   - criação → Singleton / Factory / Factory Method
   - estrutura → Adapter / Composite / Proxy (/ Facade)
   - comportamento → Observer / Strategy / Iterator
2. **Forças** — o que o problema exige (flexibilidade? desacoplamento? acesso controlado?).
3. **Padrão** que responde a essas forças com consequências aceitáveis.
4. **Por que não o parecido** (ex.: "é Observer e não Factory porque o problema é
   *notificação*, não *criação*").

### Exemplos prontos com o EduHub

- *"Enviar notificação por um serviço de e-mail de terceiros que não posso alterar."*
  → **Adapter** (o Adaptador de E-mail). Não é Facade: o objetivo é compatibilidade, não
  esconder complexidade.
- *"Quando um comunicado é publicado, caixa de entrada, e-mail e app precisam saber."*
  → **Observer** (1:N, desacoplado). Não é Strategy: não estou trocando algoritmo.
- *"Vários tipos de avaliação com cálculo de nota diferente, sem `if` gigante."*
  → **Strategy** (`TipoAvaliacao`). Já está no diagrama.
- *"O professor só pode lançar nota nas turmas dele."*
  → **Proxy** de proteção. Não é Adapter: a interface é a mesma, o que muda é o controle de acesso.

---

## Resumo de uma linha

- **Strategy** → já no EduHub, 2×: tipos de avaliação e métodos de 2FA. (OCP)
- **Adapter** → o componente Adaptador de E-mail, traduzindo para o serviço externo. (RF-36)
- **Observer** → mensageria/notificações 1:N quando um evento acadêmico ocorre. (RF-35–41)
- **Proxy** → controle de acesso por permissão antes de delegar ao serviço real. (RF-07, RF-21)
- **Facade** → Autoatendimento do Aluno, se a orquestração de módulos crescer. (RF-28–34)
- **Singleton** → logger de auditoria único, com ressalvas. (RF-44)
- **Factory Method / Fábrica** → exportação de relatório em formatos variados. (RF-42)
- **Composite / Iterator** → não se aplicam ao EduHub como está.
