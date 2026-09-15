# 🌆 A Evolução dos Games — E-book

> Um e-book interativo sobre **50 anos de evolução dos videogames**, com direção de arte inspirada em **GTA V** e **GTA VI**.

![Status](https://img.shields.io/badge/status-concluído-brightgreen)
![Versão](https://img.shields.io/badge/versão-1.0-blue)
![Arquitetura](https://img.shields.io/badge/arquitetura-SMACSS%20%7C%20Clean%20Code-orange)
![Licença](https://img.shields.io/badge/licença-educacional-yellow)

🔗 **[Ler o e-book online](https://maycondis.github.io/E-book-A_Evolucao_dos_Games/)**

## 📖 Sobre

Este e-book usa uma única franquia como régua para medir três décadas de tecnologia: a série **Grand Theft Auto**. De 1997, quando a cidade era vista de cima em sprites, a 2026 e o pôr do sol de Leonida, cada episódio marca um limite técnico sendo rompido — e um preço sendo pago por isso.

O conteúdo é organizado como uma sequência de **missões**, com briefing, objetivo e balanço de ganhos e riscos. Cada afirmação técnica fecha com a fonte usada, e o que ainda é promessa de fabricante (o caso de GTA VI) está explicitamente marcado como tal, separado do que já é resultado medido.

Não é só uma história de hardware: a Missão 05 trata da crise regulatória de 2005 e da decisão que, em 2011, reconheceu videogames como expressão protegida nos Estados Unidos — o momento em que o meio deixou de ser réu.

## 🎨 Direção de Arte

A identidade visual cita as duas gerações da franquia que dão nome ao tema:

- **De GTA V** vem a estrutura: capa em colagem de painéis com moldura preta, HUD de missão e o sistema de cores dos protagonistas usado como tema de capítulo.
- **Cada era tem sua cor:** verde para a vista de cima, azul para Liberty City, teal para Vice City, ocre de deserto para San Andreas, aço lavado para GTA IV, laranja para GTA V e o rosa de Leonida para GTA VI. A folha da controvérsia quebra o neon de propósito: é papel de jornal.
- **De GTA VI** vem a pele: o pôr do sol rosa → laranja → dourado de Leonida, grão de filme, palmeiras e skyline em silhueta.

Todo o cenário é desenhado em **CSS e SVG inline**: nenhuma imagem externa, nenhuma requisição extra.

## 🗺️ Missões

| # | Missão | Jogo / período | Tema |
|---|--------|----------------|------|
| 01 | Vista de Cima | GTA 1 e 2 · 1997–1999 | Mundo aberto antes do 3D |
| 02 | Liberty City | GTA III · 2001 | A terceira dimensão e o mapa sem costura |
| 03 | Neon | Vice City · 2002 | Ambientação vale tanto quanto hardware |
| 04 | Escala | San Andreas · 2004 | Três cidades dentro de 32 MB |
| 05 | A Linha de Fogo | 2005–2011 | Hot Coffee, censura e a Suprema Corte |
| 06 | O Peso do Real | GTA IV · 2008 | RAGE, Euphoria e o custo do realismo |
| 07 | Três Protagonistas | GTA V · 2013 | O fenômeno e o jogo como serviço |
| 08 | O Custo Bilionário | Procurado | Orçamento, crunch e o contraponto indie |
| 09 | Leonida | GTA VI · 2026 | O que é fato e o que é trailer |
| 10 | Horizonte | Bônus | Nuvem, VR e IA generativa |
| 11 | Dossiê | Fontes | Tudo com link para conferir |

## 🚀 Como Usar

### Ler no navegador

Acesse o [link do GitHub Pages](https://maycondis.github.io/E-book-A_Evolucao_dos_Games/) ou abra localmente:

```bash
start index.html
```

### Exportar como PDF

O e-book foi projetado com regras de `@media print` para sair fiel no papel:

1. Abra `index.html` no Chrome ou Edge.
2. Pressione `Ctrl + P` ou clique no botão flutuante **"BAIXAR PDF"**.
3. Selecione **"Salvar como PDF"**.
4. ✅ Ative **"Gráficos de fundo"** (Background graphics).
5. Defina as Margens como **"Nenhuma"** (None).
6. Cada folha sai exatamente como uma página A4.

### Conferir a paginação

O projeto tem um auditor embutido. Abra a página com `?debug` na URL:

```
index.html?debug
```

Qualquer folha cujo conteúdo ultrapasse o limite da A4 — e que seria cortada silenciosamente no PDF — aparece marcada em vermelho. O aviso também sai no console do navegador, sempre.

## 🛠️ Engenharia

- **Arquitetura SMACSS:** CSS modularizado em `tokens`, `base`, `layout`, `panels`, `missions`, `covers`, `themes`, `motion` e `print` — nomes que descrevem o domínio do projeto.
- **Temas por variável:** cada folha define um único `--mission`; faixa do painel, numeração, etiquetas e ganchos herdam essa cor. Trocar o tema de um capítulo é mudar uma linha.
- **Clean Code no JS:** funções pequenas e nomeadas, uma responsabilidade cada — exportação de PDF, rastreamento da missão visível e auditoria de paginação.
- **Semântica HTML5:** `<main>`, `<article>`, `<nav>`, `<aside>`, `<footer>`, com `aria-labelledby` em todas as folhas e `.sr-only` para o `<h1>` da capa.
- **Acessibilidade:** foco visível no teclado, `prefers-reduced-motion` respeitado e contraste conferido no tema escuro.
- **Performance:** o cenário evita `backdrop-filter` e transformações 3D em camadas fixas — ambos travavam o renderizador do Chrome ao rolar um documento de dez folhas A4. As grades em perspectiva são SVG já desenhado, não `rotateX` em tempo real.
- **Open Graph e Twitter Cards** para gerar miniatura ao compartilhar.

## 📁 Estrutura do Projeto

```
📦 E-book-A_Evolucao_dos_Games
├── 📄 index.html              # Conteúdo semântico do e-book (HTML5)
├── 📂 assets/
│   ├── 📂 css/
│   │   ├── 🎨 style.css       # Hub central de importação
│   │   ├── 🎨 scenery.css     # Cenário de fundo (Leonida ao anoitecer)
│   │   └── 📂 modules/        # Arquitetura SMACSS
│   │       ├── tokens.css     # Design tokens e paleta
│   │       ├── base.css       # Reset e tipografia
│   │       ├── layout.css     # Folhas A4 e menu de pausa
│   │       ├── panels.css     # Painel, cabeçalho e HUD de rodapé
│   │       ├── missions.css   # Briefing, ganhos x riscos, nível de procurado
│   │       ├── covers.css     # Capa em painéis e tela final
│   │       ├── themes.css     # Um tema de cor por missão
│   │       ├── motion.css     # Animações e reduced-motion
│   │       └── print.css      # Impressão A4 e auditor de paginação
│   ├── 📂 js/
│   │   └── ⚙️ script.js       # PDF, missão ativa e auditoria de folhas
│   └── 📂 img/
│       └── favicon.svg
└── 📘 README.md
```

## ✨ Features

- 🎨 **Tema por era** — onze missões, onze paletas, propagadas por uma única variável CSS.
- 🖨️ **Impressão A4 milimétrica** — catorze folhas, nenhuma estourando o limite (verificado no navegador, com as fontes carregadas).
- 🛰️ **Menu de pausa** com radar e destaque automático da missão em leitura.
- 🚨 **Nível de procurado** com as estrelas do HUD no capítulo sobre o custo da indústria.
- 🌴 **Cenário 100% CSS/SVG** — sol cortado, skyline e palmeiras sem uma única imagem externa.
- 📱 **Responsivo** — as folhas viram fluidas no celular sem quebrar a leitura.

## 👥 Autores

| Nome | R.A. |
|------|------|
| Gabriel Alves Moreira | H67HJ4 |
| Maycon Douglas Inácio Silva | H719CD3 |

## ⚠️ Nota sobre GTA VI

O jogo ainda não foi lançado. A data (**19 de novembro de 2026**) e as plataformas (**PS5 e Xbox Series X|S**, sem PC no lançamento) foram conferidas na [página oficial da Rockstar](https://www.rockstargames.com/VI) em 15/09/2026.

Já as afirmações sobre desempenho e simulação vêm de trailers e comunicados, e estão marcadas no texto como promessa — não como resultado medido. Essa separação é proposital: é o que diferencia o e-book de uma matéria de expectativa.

## 📄 Licença

Projeto de uso livre para fins educacionais. *Grand Theft Auto* é marca registrada da Rockstar Games; este é um trabalho acadêmico independente, sem qualquer vínculo com a empresa.

---

*"O que muda é a potência. O que decide continua sendo o design."* 🎮
