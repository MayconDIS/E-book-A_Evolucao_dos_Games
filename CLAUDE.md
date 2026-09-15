# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## O que é

E-book estático de página única sobre a evolução dos videogames, contada pela série Grand Theft Auto. HTML + CSS + um arquivo JS, sem build, sem dependências, sem framework. Publicado via GitHub Pages em `https://maycondis.github.io/E-book-A_Evolucao_dos_Games/`.

Idioma do conteúdo, dos comentários no código e das mensagens de commit: **português do Brasil**.

## Rodar e verificar

Não há build, lint nem suíte de testes. O ciclo é: editar → servir → medir no navegador.

```bash
# servidor local (file:// não serve: o JS usa fetch e as fontes vêm de CDN)
python -m http.server 8000 --bind 127.0.0.1
```

### Auditor de paginação embutido

Abrir com `?debug` na URL (`http://127.0.0.1:8000/index.html?debug`) marca em vermelho qualquer folha cujo conteúdo ultrapasse a A4 — conteúdo que sairia **cortado sem aviso** no PDF, porque `.sheet` tem `overflow: hidden`. O aviso também vai ao console sempre, com ou sem `?debug`.

### Verificação obrigatória após mexer em conteúdo ou CSS

Duas medições, sempre no navegador e sempre **depois de `await document.fonts.ready`** (a altura do texto só é confiável com Anton e Inter carregadas):

1. **Paginação** — nenhuma `.panel` pode ter `scrollHeight > clientHeight`.
2. **Contraste** — para cada elemento com texto, calcular o índice WCAG contra o fundo real (subindo a árvore até achar um ancestral com `background-color` opaco). Mínimo 4.5:1, ou 3:1 para texto grande (≥24px, ou ≥18.66px em peso ≥700). O estado atual é 321 elementos medidos, zero falhas, margem mais apertada 4.78:1.

**Cuidado com cache ao medir:** os módulos CSS entram por `@import` dentro de `style.css`. Recarregar a página ou colocar query na tag `<link>` **não** invalida os arquivos importados — o Chrome serve da memória e a medição reflete código antigo. Para medir de verdade, buscar cada módulo com `fetch(url, {cache: 'no-store'})` e injetar num `<style>`.

## Arquitetura

### Contrato de folha

Cada página do e-book é um `<article class="sheet theme-X">` de exatamente 21cm × 29.7cm contendo **um** `<div class="panel">`. O `.sheet` é a folha (cor de moldura); o `.panel` é a moldura preta de quadrinho onde o conteúdo vive. O `.panel` é flex-column e o `<footer class="hud-footer">` usa `margin-top: auto` — por isso o rodapé encosta na borda interna inferior e a "sobra" medida ali é normalmente 0. Isso é o esperado, não um sintoma de estouro.

A capa foge do contrato: usa `.cover-grid` com células de colagem em vez de `.panel`.

### Um tema por folha, uma variável

`themes.css` define `--mission` por tema. Faixa de cor do painel (`.panel::before`), numeração, `.eyebrow`, `.briefing-label`, `.hud-page` e o gancho `.cliffhanger` herdam dessa variável. **Trocar a cor de um capítulo é mudar uma linha.** Não espalhar cores literais pelos componentes.

Fundos: cada tema tem um `.theme-X .panel` com brilho radial na cor da missão sobre degradê linear escuro. `background-color` é declarado **separado** de `background-image` de propósito — é a cor sólida que sustenta o contraste se a imagem não pintar, e é ela que a auditoria de contraste lê.

### Ordem dos módulos CSS importa

`style.css` importa nesta ordem: `tokens → base → layout → panels → missions → covers → themes → motion → print`. Regras de mesma especificidade em arquivos posteriores vencem. Os fundos em degradê ficam no fim de `themes.css` justamente para vencer as declarações anteriores.

Consequência prática: **onde uma regra mora muda se ela funciona.** Os estilos das folhas de papel (`.dossier-sheet`, `.press-sheet`) estão espalhados entre `missions.css` e `themes.css`; ao sobrescrever uma delas, confirmar em qual arquivo a regra original vive antes de editar.

### Tokens: não reusar nome

`tokens.css` separa **cor de superfície** de **cor de acento**, e acentos de preenchimento de acentos de texto:

- `--steel` é a superfície escura dos painéis. Não é a cor da era GTA IV — essa é `--hd-washed`.
- `--alert` e `--violet` são saturados, para barras e marcadores. Em texto pequeno sobre fundo escuro eles não alcançam 4.5:1: usar `--alert-ink` e `--violet-ink`.

Já aconteceu de um token ser definido duas vezes no mesmo `:root` (`--steel`), a segunda definição vencer e o fundo de quase toda folha virar claro com texto claro em cima. Antes de criar um token, conferir se o nome já existe.

### JavaScript

`assets/js/script.js`, funções pequenas e nomeadas, sem dependências. Três responsabilidades: botão de exportar PDF (`window.print()`), destaque da missão visível no menu de pausa via `IntersectionObserver` sobre `.sheet h2[id]`, e a auditoria de paginação descrita acima.

### Impressão

`print.css` reproduz a A4 exata, esconde menu de pausa, botão e cenário, e reduz tipografia para dar folga. Todo bloco colorido precisa estar na lista de `print-color-adjust: exact`, senão o navegador descarta o fundo no PDF. Ao criar um componente colorido novo, incluí-lo nessa lista.

## Armadilhas de renderização já enfrentadas

Este documento é longo (catorze folhas A4 empilhadas). Duas construções travaram o renderizador do Chrome ao rolar — tela em branco e depois timeout:

- `backdrop-filter` em elemento fixo (era o menu de pausa)
- `perspective()` + `rotateX()` numa camada grande e fixa (era a grade do cenário)

Ambas foram substituídas por SVG já desenhado em perspectiva, embutido como data URI. **Não reintroduzir nenhuma das duas.** O grão de filme é uma única camada fixa do tamanho da janela em `body::after` — aplicá-lo por folha criava catorze camadas do tamanho de uma A4 e degradava a rolagem.

Outra: `line-height` abaixo de 1 em texto com `background-clip: text` faz til e cedilha caírem fora da caixa pintada pelo gradiente e **sumirem** — o título saía "A EVOLUCAO". Manter `line-height ≥ 1.04` em tipografia de display.

## Imagens

Tudo é CSS ou SVG inline: cenário, palmeiras, skyline, grades. A única exceção é `assets/img/capa.png` (1200×630), a imagem de Open Graph, gerada por script Pillow fora do repositório. O script mede o texto antes de desenhar a caixa e aborta se o texto invadir o bloco de autores.

## Conteúdo

Onze missões em ordem cronológica, de GTA 1 (1997) a GTA VI (2026), mais índice, dossiê de fontes e tela final. Cada missão fecha com `.hud-source` citando a fonte.

Regra editorial a preservar: **o que é resultado medido e o que é promessa de fabricante ficam separados no texto.** A folha de GTA VI afirma data e plataformas (conferidas na página oficial da Rockstar) mas marca desempenho e simulação como promessa de trailer. Ao atualizar dados de mercado ou da série, conferir na fonte primária e ajustar a data de verificação citada no rodapé da folha.

## Autoria

Trabalho acadêmico de Gabriel Alves Moreira (R.A. H67HJ4) e Maycon Douglas Inácio Silva (R.A. H719CD3). Os nomes e R.A. aparecem na capa, nas meta tags, no rodapé da folha final e no README — ao alterar um, alterar todos.
