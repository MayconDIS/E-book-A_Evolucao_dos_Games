# 🌆 A Evolução dos Games — E-book

> Um e-book interativo sobre **50 anos de evolução dos videogames**, com direção de arte inspirada em **GTA V** e **GTA VI**.

![Status](https://img.shields.io/badge/status-concluído-brightgreen)
![Versão](https://img.shields.io/badge/versão-1.0-blue)
![Arquitetura](https://img.shields.io/badge/arquitetura-SMACSS%20%7C%20Clean%20Code-orange)
![Licença](https://img.shields.io/badge/licença-educacional-yellow)

🔗 **[Ler o e-book online](https://maycondis.github.io/E-book-A_Evolucao_dos_Games/)**

## 📖 Sobre

Do **Atari 2600 com 128 bytes de RAM** ao mundo vivo de **Leonida**, este e-book conta como a restrição técnica sempre foi a maior professora de game design — e por que ela nunca desaparece de verdade, só muda de forma.

O conteúdo é organizado como uma sequência de **missões**, com briefing, objetivo e balanço de ganhos e riscos. Cada afirmação técnica fecha com a fonte usada, e o que ainda é promessa de fabricante (o caso de GTA VI) está explicitamente marcado como tal, separado do que já é resultado medido.

## 🎨 Direção de Arte

A identidade visual cita as duas gerações da franquia que dão nome ao tema:

- **De GTA V** vem a estrutura: capa em colagem de painéis com moldura preta, HUD de missão e o sistema de cores dos protagonistas — verde Franklin, azul Michael e laranja Trevor — usado como tema de capítulo.
- **De GTA VI** vem a pele: o pôr do sol rosa → laranja → dourado de Leonida, grão de filme, palmeiras e skyline em silhueta.

Todo o cenário é desenhado em **CSS e SVG inline**: nenhuma imagem externa, nenhuma requisição extra.

## 🗺️ Missões

| # | Missão | Tema |
|---|--------|------|
| 01 | Restrição | Como 128 bytes de RAM viraram escola de design |
| 02 | A Terceira Dimensão | Quando o jogo deixou de ser fase e virou lugar |
| 03 | Leonida | GTA VI: o que a Rockstar confirmou e o que é leitura de trailer |
| 04 | O Custo Bilionário | Nível de procurado: orçamento, crunch e monetização |
| 05 | Fora do Radar | A contracultura indie e a hipersaturação |
| 06 | Horizonte | Nuvem, VR e IA generativa — com os gargalos de cada uma |
| 07 | Dossiê | Todas as fontes, com link |

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

- 🎨 **Tema por missão** — a cor do capítulo se propaga por uma única variável CSS.
- 🖨️ **Impressão A4 milimétrica** — dez folhas, nenhuma estourando o limite (verificado no navegador, com as fontes carregadas).
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

O jogo ainda não foi lançado. Tudo o que o e-book afirma sobre desempenho e simulação vem de trailers e comunicados oficiais da Rockstar, e está marcado no texto como promessa, não como resultado medido. A data de lançamento já mudou duas vezes — **reconfira no [Rockstar Newswire](https://www.rockstargames.com/newswire) antes de citar**.

## 📄 Licença

Projeto de uso livre para fins educacionais. *Grand Theft Auto* é marca registrada da Rockstar Games; este é um trabalho acadêmico independente, sem qualquer vínculo com a empresa.

---

*"O que muda é a potência. O que decide continua sendo o design."* 🎮
