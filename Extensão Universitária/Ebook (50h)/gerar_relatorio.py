# -*- coding: utf-8 -*-
"""
Gera relatorio.html no padrão da pasta "1 - Cartilha (50h)":
relatório ABNT + a peça (o e-book) reproduzida na íntegra no Anexo A.

O CSS e as folhas do Anexo A são lidos do código do e-book — nada é
reescrito à mão, para a cópia não divergir do original.
"""
import io, re, os

# O script mora ao lado do relatório. O e-book é procurado subindo as pastas até achar
# ebook.html: assim a pasta do relatório pode ser reorganizada sem quebrar o script.
PASTA = os.path.dirname(os.path.abspath(__file__))


def achar_ebook(inicio):
    atual = inicio
    while True:
        if os.path.isfile(os.path.join(atual, "ebook.html")):
            return atual
        pai = os.path.dirname(atual)
        if pai == atual:
            raise SystemExit("ebook.html não encontrado em nenhuma pasta acima de " + inicio)
        atual = pai


EBOOK = achar_ebook(PASTA)
CARTILHA = r"C:\Users\mayco\Documents\GitHub\CasalFlow\.planning\Extensões Universitárias\1 - Cartilha (50h)\relatorio.html"
SAIDA = os.path.join(PASTA, "relatorio.html")


def ler(p):
    return io.open(p, encoding="utf-8").read()


def bloco(css, inicio):
    """Devolve (ini, fim) do bloco com chaves que começa em `inicio`."""
    abre = css.index("{", inicio)
    nivel, i = 0, abre
    while True:
        if css[i] == "{":
            nivel += 1
        elif css[i] == "}":
            nivel -= 1
            if nivel == 0:
                return inicio, i + 1
        i += 1


def remover(css, padrao):
    """Remove todos os blocos que começam com `padrao`; devolve (css, removidos)."""
    removidos = []
    while True:
        m = re.search(padrao, css)
        if not m:
            return css, removidos
        ini, fim = bloco(css, m.start())
        removidos.append(css[ini:fim])
        css = css[:ini] + css[fim:]


# ─────────────────────────── CSS do relatório (padrão Cartilha) ───────────────────────────
cartilha = ler(CARTILHA)
camada_relatorio = cartilha.split("@layer relatorio, peca;")[1].split("@layer peca {")[0]
script_imagens = "<script>" + cartilha.split("<script>")[1].split("</script>")[0] + "</script>"

# Acréscimo ao padrão: quadro de conteúdo em corpo menor (ABNT admite para tabelas).
acrescimo_relatorio = """
        @layer relatorio {
            /* 11. QUADRO DE CONTEÚDO (acréscimo deste relatório)
               Três colunas com texto corrido não cabem em 12pt sem quebrar a folha;
               a ABNT admite corpo menor em tabelas e quadros. */
            .table-conteudo { font-size: 10pt; }
            .table-conteudo th, .table-conteudo td { text-align: left; vertical-align: top; padding: 5px 7px; line-height: 1.3; }
            .table-conteudo td:first-child { font-weight: bold; width: 27%; }
            .table-conteudo td:nth-child(2) { width: 25%; }
        }
"""

# ─────────────────────────── CSS do e-book (camada peca) ───────────────────────────
ordem = ["tokens", "base", "layout", "panels", "missions", "covers", "themes", "motion", "print"]
fora_do_escopo, dentro_do_escopo = [], []

for nome in ordem:
    css = ler(os.path.join(EBOOK, "assets", "css", "modules", nome + ".css"))
    if nome == "tokens":
        # :root não é descendente do anexo; dentro do @scope não casaria com nada.
        fora_do_escopo.append("/* ── tokens.css ── */\n" + css)
        continue
    css, keyframes = remover(css, r"@keyframes\s+[\w-]+\s*\{")
    css, _pages = remover(css, r"@page\s*\{")
    if keyframes:
        fora_do_escopo.append("/* ── @keyframes de motion.css (não valem dentro de @scope) ── */\n" + "\n".join(keyframes))
    dentro_do_escopo.append("/* ── " + nome + ".css ── */\n" + css)

camada_peca = """
        @layer peca {
            /* Mesmo desenho da Cartilha: o relatório estiliza elementos nus (p, li,
               h1..h6, ul, ol, table) com recuo ABNT, justificação e 12pt; o reset em
               sub-camada `base` impede esse estilo de vazar para dentro do e-book, e
               `@scope` impede o e-book de vazar para fora. `arte` vence `base` sempre. */
            @layer base, arte;

            @layer base {
                .anexo-a, .anexo-a * { -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
                .anexo-a, .anexo-a * { box-sizing: border-box; margin: 0; padding: 0; }

                .anexo p, .anexo li, .anexo h1, .anexo h2, .anexo h3, .anexo h4,
                .anexo h5, .anexo h6, .anexo ul, .anexo ol,
                .anexo table, .anexo th, .anexo td, .anexo dl, .anexo dt, .anexo dd {
                    margin: 0;
                    padding: 0;
                    text-indent: 0;
                    text-align: inherit;
                    line-height: inherit;
                    font-size: inherit;
                    color: inherit;
                    border: 0;
                    background-color: transparent;
                }
            }

            @layer arte {
                /* ═══ Anexo A: e-book "A Evolução dos Games" ═══
                   Copiado de assets/css/modules/ por script. Não editar aqui:
                   corrigir no e-book e regerar este relatório. */

%FORA%

                @scope (.anexo-a) {
%DENTRO%
                }

                /* O `body` do e-book (Inter, cor de texto clara) não existe dentro do
                   relatório; sem isto o miolo das folhas herdaria Arial e preto. */
                .page.peca-a {
                    font-family: var(--font-ui);
                    color: var(--text);
                    -webkit-font-smoothing: antialiased;
                }

                @media screen {
                    .anexo > .page { margin-bottom: 30px; }
                }
            }
        }
""".replace("%FORA%", "\n".join(fora_do_escopo)).replace("%DENTRO%", "\n".join(dentro_do_escopo))

# ─────────────────────────── Folhas do e-book (Anexo A) ───────────────────────────
indice = ler(os.path.join(EBOOK, "ebook.html"))
main = indice.split("<main>")[1].split("</main>")[0]
folhas = re.findall(r"(<article class=\"sheet.*?</article>)", main, flags=re.S)
assert len(folhas) == 14, "esperava 14 folhas, achei %d" % len(folhas)
folhas = [f.replace('<article class="sheet', '<article class="page peca-a sheet', 1) for f in folhas]
anexo = "\n\n".join(folhas)

# ─────────────────────────── Relatório ───────────────────────────
P = lambda t: '<span class="pendente">%s</span>' % t


def folha(id_, numero, corpo):
    num = '        <div class="page-number">%d</div>\n' % numero if numero else ""
    return '    <section class="page" id="%s">\n%s%s\n    </section>\n' % (id_, num, corpo)


capa = """    <section class="page" id="capa" aria-label="Capa do Trabalho">
        <header>
            <img src="assets/Logo UNIP.png" alt="Logo da Universidade Paulista" class="logo-unip" onerror="this.src='https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/UNIP_Logo.svg/1200px-UNIP_Logo.svg.png'">
            <div class="capa-header uppercase">
                UNIVERSIDADE PAULISTA<br>
                ICET - INSTITUTO DE CIÊNCIAS EXATAS E TECNOLOGIA<br>
                CURSO SUPERIOR DE TECNOLOGIA EM ANÁLISE E DESENVOLVIMENTO DE SISTEMAS<br><br><br>
                EXTENSÃO UNIVERSITÁRIA<br><br><br>
                RELATÓRIO DE ATIVIDADE DE EXTENSÃO — EBOOK<br>
                <span style="text-transform: none;">(A Evolução dos Games: a história do videogame contada pela série GTA)</span><br>
                <span style="text-transform: none;">Carga horária: 50 horas</span>
            </div>
        </header>

        <table class="table-capa" aria-label="Tabela de Autores">
            <tr><th width="70%">Nome</th><th width="30%">R.A</th></tr>
            <tr>
                <td>Gabriel Alves Moreira</td>
                <td>H67HJ4</td>
            </tr>
            <tr>
                <td>Maciel Costa da Silva</td>
                <td>R280985</td>
            </tr>
            <tr>
                <td>Maycon Douglas Inácio Silva</td>
                <td>H719CD3</td>
            </tr>
        </table>

        <footer class="capa-footer uppercase">
            São José dos Campos - SP<br>Setembro / 2026
        </footer>
    </section>
"""

SUMARIO = [
    ("dados-cadastro", "1. Dados de Cadastro", "%P_DADOS%"),
    ("descricao-1", "2. Descrição da Atividade", "%P_DESC%"),
    ("conclusao", "3. Conclusão e Resultados Alcançados", "%P_CONC%"),
    ("comprovacao", "4. Comprovação", "%P_COMP%"),
    ("anexo-a", "Anexo A &ndash; E-book &quot;A Evolução dos Games&quot; na íntegra", "%P_ANEXO%"),
]
sumario = '    <section class="page" id="sumario">\n        <h2>Sumário</h2>\n'
for alvo, rotulo, pag in SUMARIO:
    sumario += """
        <div class="sumario-item">
            <a href="#%s">%s</a>
            <div class="sumario-dots"></div>
            <span>%s</span>
        </div>
""" % (alvo, rotulo, pag)
sumario += "    </section>\n"

paginas = []  # (id, corpo) — numeradas a partir da folha 3

paginas.append(("dados-cadastro", """        <h2>1. Dados de Cadastro</h2>

        <h3>Campus</h3>
        <p>Campus SJC Dutra - São José dos Campos (SP)</p>

        <h3>Alunos Participantes</h3>
        <table>
            <thead>
                <tr>
                    <th>Número</th>
                    <th>R.A.</th>
                    <th>Nome</th>
                    <th>Curso</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>1</td>
                    <td>H67HJ4</td>
                    <td>Gabriel Alves Moreira</td>
                    <td>Análise e Desenvolvimento de Sistemas</td>
                </tr>
                <tr>
                    <td>2</td>
                    <td>R280985</td>
                    <td>Maciel Costa da Silva</td>
                    <td>Análise e Desenvolvimento de Sistemas</td>
                </tr>
                <tr>
                    <td>3</td>
                    <td>H719CD3</td>
                    <td>Maycon Douglas Inácio Silva</td>
                    <td>Análise e Desenvolvimento de Sistemas</td>
                </tr>
            </tbody>
        </table>
        <p class="no-indent"><em>Turma: DS4A48</em></p>
        <p class="no-indent"><em>Grupo composto por 3 alunos do mesmo campus, responsáveis pela pesquisa, redação, desenvolvimento, publicação e divulgação da obra.</em></p>

        <h3>Período</h3>
        <p>Ano: 2026 | Semestre: 4º</p>

        <h3>Área Temática e Projeto</h3>
        <p>TECNOLOGIA E PRODUÇÃO &middot; Desenvolvimento de aplicativos/software/website para a comunidade.</p>

        <h3>Ação</h3>
        <p>Ebook (50 horas)</p>

        <h3>Organização Parceira e Público Beneficiário</h3>
        <table class="table-dados">
            <tr><td>Organização Parceira</td><td>""" + P("informar a escola, biblioteca, curso técnico ou coletivo atendido") + """</td></tr>
            <tr><td>Público Beneficiário</td><td>Estudantes do ensino médio e técnico, ingressantes em cursos de tecnologia e comunidade externa interessada em história e desenvolvimento de jogos</td></tr>
        </table>"""))

paginas.append(("descricao-1", """        <h2>2. Descrição da Atividade</h2>
        <h3>2.1 Descrição Geral da Atividade</h3>
        <p>A presente atividade de extensão universitária consistiu na pesquisa, redação e
        desenvolvimento editorial do e-book <strong>&quot;A Evolução dos Games: a história do
        videogame contada pela série GTA&quot;</strong>, obra digital de 14 folhas em formato A4,
        organizada em 11 capítulos e cerca de 2.700 palavras, publicada gratuitamente na
        internet para uso educacional.</p>

        <p>O problema que a obra endereça é o acesso a conhecimento técnico organizado. A
        história da computação aplicada ao entretenimento costuma chegar ao público em duas
        formas igualmente limitadas: a matéria de expectativa, que trata anúncio comercial como
        fato consumado, e o material técnico fechado em vocabulário inacessível a quem ainda não
        é da área. O e-book adota uma terceira via: usar uma única franquia conhecida do público
        como régua para medir três décadas de evolução técnica, explicando cada salto de
        engenharia pelo problema concreto que ele resolveu.</p>

        <h4>Estrutura do conteúdo</h4>
        <p>A obra percorre o período de 1997 a 2026 em ordem cronológica. Cada capítulo está
        ancorado em um marco técnico verificável e trata um conceito de computação específico,
        conforme apresentado no Quadro 1.</p>"""))

quadro = [
    ("01 — Vista de Cima", "GTA 1 e 2 · 1997–1999", "Restrição de memória como condicionante de design; mundo aberto sem 3D"),
    ("02 — Liberty City", "GTA III · 2001", "Renderização em terceira pessoa; mapa contínuo sem carregamento"),
    ("03 — Neon", "Vice City · 2002", "Direção de arte e licenciamento sobre a mesma base técnica"),
    ("04 — Escala", "San Andreas · 2004", "Mundo aberto extenso em hardware de 32 MB de memória"),
    ("05 — A Linha de Fogo", "2005–2011", "Classificação etária, autorregulação e jurisprudência"),
    ("06 — O Peso do Real", "GTA IV · 2008", "Física procedural em tempo real versus animação pré-gravada"),
    ("07 — Três Protagonistas", "GTA V · 2013", "Troca de personagem; software como serviço"),
    ("08 — O Custo Bilionário", "Indústria", "Ciclos de desenvolvimento, orçamento, crunch e monetização"),
    ("09 — Leonida", "GTA VI · 2026", "Iluminação global, simulação de multidões e sistemas emergentes"),
    ("10 — Horizonte", "Prospectivo", "Computação em nuvem, latência, realidade virtual e IA generativa"),
    ("11 — Dossiê", "Referências", "Nove fontes primárias com link para verificação"),
]
linhas = "\n".join(
    "                <tr><td>%s</td><td>%s</td><td>%s</td></tr>" % l for l in quadro)

paginas.append(("descricao-2", """        <h2>2. Descrição da Atividade (continuação)</h2>
        <p class="figure-title">Quadro 1 – Capítulos do e-book e conceitos de computação tratados</p>
        <table class="table-conteudo">
            <thead>
                <tr><th>Capítulo</th><th>Recorte</th><th>Conceito tratado</th></tr>
            </thead>
            <tbody>
%s
            </tbody>
        </table>
        <p class="caption">Fonte: Elaborado pelos autores (2026).</p>""" % linhas))

paginas.append(("descricao-3", """        <h2>2. Descrição da Atividade (continuação)</h2>
        <p>Dois capítulos merecem destaque pelo alcance formativo:</p>
        <ul>
            <li><strong>Capítulo 05 — A Linha de Fogo:</strong> trata da crise regulatória de
            2005, originada por conteúdo residual encontrado dentro dos arquivos do jogo, e da
            decisão da Suprema Corte dos Estados Unidos em 2011 no caso <em>Brown v. Entertainment
            Merchants Association</em>, que reconheceu videogames como expressão protegida
            constitucionalmente. É o capítulo que conecta o curso de tecnologia a temas de ética,
            regulação e responsabilidade profissional: o que fica esquecido dentro de um
            repositório de código pode ter consequência jurídica e comercial.</li>
            <li><strong>Capítulo 08 — O Custo Bilionário:</strong> apresenta ao estudante de
            tecnologia a realidade econômica da engenharia de software de grande porte — ciclos
            de sete a dez anos, jornadas extremas na reta final e a relação entre orçamento e
            modelo de receita —, com o contraponto do desenvolvimento independente.</li>
        </ul>

        <h4>Rigor editorial adotado</h4>
        <p>A obra estabelece uma regra explícita e visível ao leitor: o que é resultado medido e
        o que é promessa de fabricante aparecem separados no texto. O capítulo sobre o título
        ainda não lançado afirma data e plataformas — conferidas na página oficial da empresa
        desenvolvedora, com a data da verificação registrada no rodapé da própria folha —, mas
        classifica explicitamente as declarações de desempenho e simulação como promessa de
        material promocional. Cada capítulo encerra com a fonte utilizada, e o capítulo final
        reúne as nove referências com link direto, permitindo ao leitor auditar qualquer
        afirmação.</p>"""))

paginas.append(("descricao-4", """        <h2>2. Descrição da Atividade (continuação)</h2>
        <h4>Desenvolvimento técnico</h4>
        <p>A peça foi construída como aplicação web estática, sem framework e sem bibliotecas de
        terceiros; o único recurso externo carregado em tempo de execução são as duas famílias
        tipográficas, servidas pelo Google Fonts.</p>
        <ul>
            <li><strong>HTML5 semântico:</strong> 675 linhas, com hierarquia de títulos sem saltos
            e rótulos de acessibilidade em todas as folhas.</li>
            <li><strong>CSS modular em arquitetura SMACSS:</strong> 1.407 linhas em 11 arquivos,
            sendo nove módulos separados por responsabilidade, o arquivo central de importação e
            o do cenário ilustrado.</li>
            <li><strong>JavaScript sem bibliotecas:</strong> 105 linhas em funções de
            responsabilidade única — exportação para PDF, destaque do capítulo em leitura e
            auditoria automática de paginação.</li>
            <li><strong>Peso total de 98,3 KB</strong> em HTML, CSS e JavaScript. Toda a ilustração
            é desenhada em CSS e SVG embutido, sem nenhuma imagem externa, para que a obra abra
            rápido em conexão lenta e em aparelho modesto.</li>
        </ul>

        <h4>Acessibilidade e impressão</h4>
        <p>A obra foi submetida a auditoria automatizada de contraste segundo o critério WCAG
        2.1 nível AA, executada no navegador com as fontes já carregadas: 321 elementos de texto
        foram medidos contra o fundo efetivo de cada um, sem nenhuma falha, com margem mínima de
        4,78:1 sobre o mínimo exigido de 4,5:1. Somam-se foco visível para navegação por
        teclado e respeito à preferência de movimento reduzido do sistema operacional.</p>
        <p>Para distribuição impressa, a obra reproduz o formato A4 exato, com verificação
        embutida: um auditor de paginação alerta sempre que o conteúdo de uma folha ultrapassa o
        limite da página e seria cortado na exportação para PDF, garantindo que a versão
        impressa seja fiel à digital.</p>

        <h4>Divulgação</h4>
        <p>Além da publicação em acesso aberto, a obra foi divulgada pelos autores no LinkedIn,
        rede profissional em que se concentra o público de estudantes e profissionais de
        tecnologia, com link direto para a leitura gratuita. A publicação usa a imagem de
        compartilhamento própria do e-book, dimensionada no padrão exigido pela rede
        (1200 × 630 pixels). """ + P("Informar a data da publicação.") + """</p>"""))

paginas.append(("participacao", """        <h2>2.2 Descrição da Participação de Cada Aluno</h2>
        <p class="no-indent">""" + P("Conferir e ajustar à divisão real de tarefas antes de submeter.") + """</p>

        <h4>Gabriel Alves Moreira (R.A. H67HJ4)</h4>
        <p>Atuou na <strong>pesquisa histórica, curadoria de fontes primárias e redação
        didática</strong>, aplicando conhecimentos das disciplinas de <em>Metodologia
        Científica</em>, <em>Comunicação e Expressão</em> e <em>Ética e Legislação
        Profissional</em>. Foi responsável por levantar e verificar as nove referências que
        sustentam a obra, estabelecer a regra editorial que separa dado medido de promessa
        comercial, redigir o capítulo sobre classificação etária e jurisprudência e adequar a
        linguagem técnica a um público que ainda não cursa tecnologia, preservando a precisão dos
        conceitos.</p>

        <h4>Maciel Costa da Silva (R.A. R280985)</h4>
        <p>Atuou na <strong>revisão editorial, adequação às diretrizes de extensão e planejamento
        da divulgação</strong>, aplicando conhecimentos das disciplinas de <em>Comunicação e
        Expressão</em>, <em>Metodologia Científica</em> e <em>Interface Homem-Computador</em>. Foi
        responsável por revisar a clareza dos capítulos para o público não técnico, verificar a
        consonância da obra com os critérios de impacto comunitário da UNIP e estruturar a
        divulgação no LinkedIn, incluindo o texto da publicação e o acompanhamento das
        estatísticas de alcance registradas neste relatório.</p>

        <h4>Maycon Douglas Inácio Silva (R.A. H719CD3)</h4>
        <p>Atuou no <strong>desenvolvimento front-end, arquitetura de estilos, acessibilidade e
        publicação</strong>, aplicando conhecimentos das disciplinas de <em>Programação Web</em>,
        <em>Interface Homem-Computador</em> e <em>Engenharia de Software</em>. Foi responsável por
        estruturar o CSS em arquitetura modular, implementar o sistema de temas em que a cor de
        cada capítulo se propaga por uma única variável, codificar o suporte nativo a impressão
        A4 e o auditor automático de paginação — reproduzidos na íntegra no Anexo A deste
        relatório —, conduzir a auditoria de contraste WCAG AA e publicar a obra em servidor de
        acesso público com versionamento aberto.</p>"""))

paginas.append(("conclusao", """        <h2>3. Conclusão e Resultados Alcançados</h2>
        <p>A atividade entregou à comunidade uma obra de referência sobre história da computação
        aplicada ao entretenimento, gratuita, sem anúncios, sem rastreadores e sem exigência de
        cadastro, acessível por navegador em qualquer aparelho e disponível também para impressão
        em A4 para distribuição física.</p>

        <p>A atividade atendeu diretamente """ + P("informar o número de pessoas atendidas presencialmente e onde") + """.
        A divulgação no LinkedIn ampliou o alcance da obra para além desse público, registrando
        """ + P("impressões e reações da publicação, conforme as estatísticas do LinkedIn na data de fechamento do relatório") + """.</p>

        <p class="no-indent">Resultados objetivos e verificáveis:</p>
        <ul>
            <li><strong>11 capítulos e 14 folhas A4</strong> publicados e acessíveis por endereço permanente.</li>
            <li><strong>Nove fontes primárias</strong> com link direto, permitindo ao leitor auditar cada afirmação.</li>
            <li><strong>Conformidade de contraste WCAG 2.1 AA</strong> verificada por medição automatizada em 321 elementos de texto, sem falhas.</li>
            <li><strong>98,3 KB de peso total</strong>, sem imagens externas, para conexões lentas e aparelhos de baixo desempenho.</li>
            <li><strong>Código-fonte aberto</strong>, permitindo que a obra seja reaproveitada, corrigida ou traduzida por terceiros.</li>
        </ul>

        <p class="no-indent">A atividade está alinhada aos seguintes <strong>Objetivos de
        Desenvolvimento Sustentável (ODS) da ONU</strong>:</p>
        <ul>
            <li><strong>ODS 4 (Educação de Qualidade):</strong> material didático gratuito sobre evolução tecnológica, com fontes verificáveis e linguagem acessível.</li>
            <li><strong>ODS 9 (Indústria, Inovação e Infraestrutura):</strong> documentação de três décadas de inovação em engenharia de software.</li>
            <li><strong>ODS 10 (Redução das Desigualdades):</strong> acesso irrestrito, sem custo nem cadastro, com acessibilidade e peso reduzido.</li>
        </ul>"""))

paginas.append(("conclusao-2", """        <h2>3. Conclusão e Resultados Alcançados (continuação)</h2>

        <h3>3.1 Local onde a atividade foi realizada</h3>
        <p>A obra foi desenvolvida pelos alunos e publicada em servidor de acesso público, com
        leitura disponível em qualquer dispositivo com navegador, e divulgada no LinkedIn.
        """ + P("Informar o local e a data da apresentação ou distribuição presencial — as Orientações da UNIP (p. 6) exigem que a atividade seja realizada presencialmente.") + """</p>

        <h3>3.2 Considerações Finais</h3>
        <ul>
            <li><strong>Dificuldades enfrentadas:</strong> a principal foi editorial, não técnica —
            separar, no material disponível sobre um título ainda não lançado, o que é dado
            confirmado pela empresa do que é leitura de vídeo promocional. A solução foi registrar a
            data da verificação na própria folha e marcar as promessas como tais no corpo do
            texto.</li>
            <li><strong>Sugestões:</strong> a obra está estruturada para crescer — acrescentar um
            capítulo exige apenas uma folha nova e um tema de cor. Recomenda-se revisar anualmente
            as afirmações sobre títulos não lançados e reconferir os links do capítulo de
            referências.</li>
            <li><strong>Observações:</strong> a decisão de não usar nenhuma imagem externa,
            desenhando toda a ilustração em CSS e SVG, não foi estética: foi o que permitiu manter a
            obra inteira abaixo de 100 KB, o que importa diretamente para o público que se pretende
            alcançar.</li>
        </ul>"""))

paginas.append(("comprovacao", """        <h2>4. Comprovação</h2>
        <p>A comprovação da atividade fundamenta-se na própria peça produzida, reproduzida na
        íntegra no <strong>Anexo A</strong> a partir da folha %P_ANEXO%, na obra publicada em
        acesso aberto, na publicação de divulgação no LinkedIn e nas capturas apresentadas a
        seguir.</p>
        <p class="no-indent">O anexo reproduz a peça como ela é distribuída — mesma diagramação,
        mesmo formato de impressão. Por isso as folhas do anexo não recebem o número de página do
        relatório, que cairia sobre a arte; o sumário anuncia onde o anexo começa. Imprimir apenas
        o intervalo do anexo devolve a peça pronta para uso. O e-book mantém, no pé de cada folha,
        a numeração interna da própria peça.</p>

        <h3>Comprovação 1 — Capa e índice do e-book</h3>
        <p class="figure-title">Figura 1 – Capa e Seleção de Missões (índice) do e-book &quot;A Evolução dos Games&quot;</p>
        <div class="image-container">
            <img src="assets/1.png" alt="Capa e índice do e-book A Evolução dos Games" class="dynamic-img"
                 title="Clique para trocar a imagem (JPG, PNG, WEBP)">
            <p class="caption">Fonte: Acervo dos autores (2026) — reprodução da peça produzida na atividade.</p>
        </div>"""))

paginas.append(("comprovacao-2", """        <h2>4. Comprovação (continuação)</h2>

        <h3>Comprovação 2 — Visão geral das 14 folhas</h3>
        <p class="figure-title">Figura 2 – As 14 folhas do e-book, cada capítulo com seu tema de cor</p>
        <div class="image-container">
            <img src="assets/2.png" alt="Miniaturas das 14 folhas do e-book" class="dynamic-img"
                 title="Clique para trocar a imagem (JPG, PNG, WEBP)">
            <p class="caption">Fonte: Acervo dos autores (2026) — reprodução da peça produzida na atividade.</p>
        </div>"""))

paginas.append(("comprovacao-3", """        <h2>4. Comprovação (continuação)</h2>

        <h3>Comprovação 3 — Publicação de divulgação no LinkedIn</h3>
        <p class="figure-title">Figura 3 – Publicação do e-book &quot;A Evolução dos Games&quot; no LinkedIn</p>
        <div class="image-container">
            <img src="assets/3.png" alt="Captura da publicação de divulgação do e-book no LinkedIn" class="dynamic-img"
                 title="Clique para anexar a captura da publicação (JPG, PNG, WEBP)">
            <p class="caption">Fonte: Acervo dos autores (2026) — captura da publicação no LinkedIn.</p>
        </div>
        <p class="no-indent">""" + P("Anexar a captura da publicação: clicar na imagem acima e escolher o arquivo, ou salvá-lo como assets/3.png.") + """</p>

        <h3>Demais evidências</h3>
        <ul>
            <li><strong>Obra publicada:</strong> maycondis.github.io/E-book-A_Evolucao_dos_Games/ebook.html</li>
            <li><strong>Código-fonte com histórico de versões:</strong> github.com/MayconDIS/E-book-A_Evolucao_dos_Games</li>
            <li><strong>Publicação no LinkedIn:</strong> """ + P("colar o link da publicação") + """</li>
            <li><strong>Registro da ação presencial:</strong> """ + P("anexar lista de presença e registro fotográfico") + """</li>
            <li><strong>Carta de Apresentação institucional:</strong> """ + P("anexar, se a atividade foi realizada junto a organização parceira") + """</li>
        </ul>"""))

# Numeração: capa e sumário não levam número; o corpo começa na folha 3.
PRIMEIRA = 3
numero = {pid: PRIMEIRA + i for i, (pid, _) in enumerate(paginas)}
folha_anexo = PRIMEIRA + len(paginas)
subst = {
    "%P_DADOS%": numero["dados-cadastro"],
    "%P_DESC%": numero["descricao-1"],
    "%P_CONC%": numero["conclusao"],
    "%P_COMP%": numero["comprovacao"],
    "%P_ANEXO%": folha_anexo,
}

corpo = capa + "\n" + sumario + "\n" + "\n".join(folha(pid, numero[pid], c) for pid, c in paginas)

cabecalho = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório de Extensão Universitária — Ebook (50h)</title>
    <!--
      ────────────────────────────────────────────────────────────────────────
      RELATÓRIO DE ATIVIDADE DE EXTENSÃO UNIVERSITÁRIA (50 horas)
      UNIP · ICET · CST em Análise e Desenvolvimento de Sistemas
      Ação: Ebook

      Formato ABNT: A4, margens 3cm superior/esquerda e 2cm inferior/direita,
      Arial 12pt, parágrafo justificado com recuo de 1,5cm.
      Para gerar o PDF: abrir no Chrome, anexar as imagens da seção 4 clicando
      sobre elas (se quiser trocá-las) e imprimir (Ctrl+P) na MESMA sessão, com
      "Gráficos de segundo plano" marcado.

      O ANEXO A (folhas %P_ANEXO% a %P_ANEXO_FIM%) é o e-book. Para tirar a peça para
      distribuir: Ctrl+P, intervalo de páginas %P_ANEXO%-%P_ANEXO_FIM%, papel A4 e
      "Gráficos de segundo plano" marcado.

      O Anexo A é CÓPIA de ebook.html e assets/css/modules/, gerada por script.
      Se o e-book mudar, regerar este relatório — não editar o anexo à mão.

      PENDÊNCIAS: todo trecho com fundo amarelo tracejado (.pendente) depende de
      informação que só os alunos têm. Resolver todos antes de submeter.
      ────────────────────────────────────────────────────────────────────────
    -->
    <style>
        @layer relatorio, peca;
""" + camada_relatorio + acrescimo_relatorio + camada_peca + """    </style>
    <!-- Tipografia da peça (Anexo A). -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Anton&family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
</head>
<body>

"""

rodape = """

    <!-- ═════════════ ANEXO A — O E-BOOK NA ÍNTEGRA ═════════════
         Folhas %P_ANEXO% a %P_ANEXO_FIM%. Reproduzem a peça como ela é distribuída, e por
         isso NÃO levam o número de página do relatório: ele cairia sobre a arte.
         O sumário anuncia onde o anexo começa. -->
    <div class="anexo anexo-a" id="anexo-a">
""" + anexo + """
    </div>

    """ + script_imagens + """
</body>
</html>
"""

html = cabecalho + corpo + rodape
subst["%P_ANEXO_FIM%"] = folha_anexo + len(folhas) - 1
for k, v in subst.items():
    html = html.replace(k, str(v))

io.open(SAIDA, "w", encoding="utf-8").write(html)
print("relatorio.html gerado:", SAIDA)
print("folhas do relatório: capa, sumário, %d a %d" % (PRIMEIRA, folha_anexo - 1))
print("anexo A: folhas %d a %d (%d folhas)" % (folha_anexo, subst["%P_ANEXO_FIM%"], len(folhas)))
print("pendências marcadas:", html.count('class="pendente"'))
print("tamanho:", round(len(html.encode('utf-8')) / 1024, 1), "KB")
