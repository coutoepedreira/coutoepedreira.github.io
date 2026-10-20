# coutoepedreira.com.br

Site editorial de Couto & Pedreira Advocacia Consultiva: Direito, patrimônio, créditos judiciais e economia.

Versão 5.6, 20 de outubro de 2026. HTML e CSS puros, sem scripts, sem dependências e sem recursos de fora. Publicado pelo GitHub Pages.

---

## O que tem em cada pasta

```
/
├── index.html          Início: capa da edição, Biblioteca, Manifesto, Autores, Escritório
├── biblioteca.html     Índice de textos e os seis formatos
├── edicoes.html        Lista de edições (a mais nova primeiro)
├── edicoes/
│   ├── quando-o-precatorio-entra-no-balanco.html   Edição 01, página única
│   └── 01.html         Endereço antigo da Edição 01: leva ao novo (não apague)
├── manifesto.html
├── metodologia.html
├── termos.html
├── privacidade.html
├── 404.html            Página de erro (usa caminhos absolutos, de propósito)
├── textos/
│   ├── modelo.html     MODELO de texto. Copie este arquivo para publicar.
│   ├── o-preco-do-registro.html   Análise: a Resolução BCB nº 346/2023 e o “registro público”
│   ├── ganhar-nao-e-receber.html  Guia: precatório e RPV, da sentença ao pagamento
│   └── o-direito-a-partilha-nao-termina-na-sentenca.html   Interpretação: partilha e perspectiva de gênero
├── css/style.css       Toda a aparência do site. Comentado, com índice no topo.
├── fonts/              Newsreader e Montserrat, servidas pelo próprio site (+ licenças)
├── assets/             Imagens, ícones e a imagem de compartilhamento
├── sitemap.xml         Mapa do site para buscadores
├── robots.txt
├── favicon.ico
├── CNAME               Domínio (não mexa)
├── .nojekyll           Diz ao GitHub para servir os arquivos como estão (não mexa)
├── .well-known/
│   └── security.txt    Contato para quem encontrar uma falha de segurança (renovar todo ano)
├── .github/            Verificação automática do site (veja SEGURANCA.md)
└── SEGURANCA.md        O que protege o site e os ajustes de conta recomendados
```

---

## Como publicar um texto novo

Tudo pode ser feito pelo navegador, no próprio GitHub.

1. **Crie o arquivo.** Abra `textos/modelo.html`, clique em *Raw*, copie tudo. Volte à pasta `textos`, clique em *Add file → Create new file* e dê um nome curto, sem acento e sem espaço: `textos/precatorio-no-balanco.html`. Cole o conteúdo.
2. **Troque o cabeçalho da página** (dentro de `<head>`): `<title>`, `description`, `canonical`, `og:url`, `article:published_time` e os autores. Troque `noindex` por `index` na linha `robots`, senão o Google não mostra o texto.
3. **Troque a abertura:** o formato no trilho (`Nota`, `Análise`...), o título (`<h1>`), a linha fina e a assinatura.
4. **Troque a ficha:** data de publicação e tempo de leitura. Tempo de leitura = número de palavras do texto ÷ 200, arredondado para cima.
5. **Escreva o corpo.** Os blocos disponíveis estão todos no modelo, cada um com um comentário explicando o uso:
   - `tese`: a frase que resume o texto. Vem primeiro.
   - `<p>`: parágrafo comum.
   - `<h2>`: intertítulo. De preferência, uma pergunta.
   - `glosa`: nota de margem. Fica **antes** do parágrafo que comenta.
   - `citacao`: trecho de lei, decisão ou doutrina, com a fonte no `<footer>`.
   - `olho`: uma frase do próprio texto em destaque. No máximo dois por texto.
   - `referencias`: lista ABNT.
   - `como-citar`: a referência do próprio texto, para quem for citá-lo.
6. **Acrescente o texto no índice** da `biblioteca.html`: copie o bloco comentado `MODELO DE ENTRADA`, cole logo abaixo da linha `indice-cabeca` e preencha. Apague a linha "Ainda não há textos publicados" quando entrar o primeiro.
7. **Troque a capa da página inicial.** A capa mostra sempre o texto mais recente, seja ele qual for. No `index.html`, o bloco `<section class="pagina capa">` (com o comentário `CAPA` acima) leva formato, título, linha fina, assinatura, tempo de leitura, endereço e imagem. Para um texto sem foto, use a figura `capa-grafica` (como na análise *O preço do registro*) ou uma imagem quadrada de 1600 × 1600 px.
8. **Acrescente o endereço no `sitemap.xml`.**
9. *Commit changes.* Em um ou dois minutos o texto está no ar.

### Peças dos textos longos (Guia e Interpretação)

O guia *Ganhar não é receber* e a interpretação *O direito à partilha não termina na sentença* trouxeram peças novas, todas no `css/style.css`, seção **18.2**:

- `exemplo`: a caixa com o caso inventado que explica a regra. Leva um `rotulo` (“Exemplo · …”) e um ou mais parágrafos.
- `citacao-longa`: citação de mais de três linhas, recuada, com a referência ABNT completa no `<footer>`.
- `tabela-texto`: tabela de texto, com quebra de linha e alinhamento à esquerda. Acrescente `numerica` quando a tabela for de números (alinha à direita e não quebra).
- `nota-final`: a observação em itálico antes das referências (“Texto informativo…”).
- Figuras de abertura sem foto: `abertura-passos` (quatro passos numerados, usada no guia) e `abertura-cifra` (um número grande e uma frase, pronta para um próximo texto).
- Abertura com foto em pé à direita do título: `abertura--retrato`, a mesma peça da Biblioteca. Usada no guia (`assets/guia-ganhar-abertura.jpg`, com os quatro passos logo abaixo) e na interpretação (`assets/interpretacao-partilha-abertura.jpg`), ambas em 3:4, 1080 × 1440 px.
- Capas da página inicial sem foto: `capa-cifras` (três números no quadro escuro) e `capa-meio` (um número só).

### A cifra sobre a foto (aberturas dos textos)

Toda foto de abertura de texto leva a **aba** com o formato (como nas chamadas do Instagram) e a **cifra**: um número grande que resume o texto e uma linha que diz o que ele é. As fotos institucionais (Biblioteca, Manifesto, Autores, Metodologia) ficam sem nada por cima. Peças no `css/style.css`, seção **18.3**.

```html
<div class="foto-cifra">
  <img src="../assets/foto.jpg" width="1080" height="1440" alt="...">
  <span class="fc-aba" aria-hidden="true">Guia</span>
  <p class="fc-sobre"><span class="fc-cifra fc-cifra--media">1º de <abbr title="fevereiro">fev.</abbr></span><span class="fc-nota">A linha que explica o número</span></p>
</div>
```

- Tamanho da cifra: sem classe extra para números curtos (“18%”); `fc-cifra--meio` para frações (“½”); `fc-cifra--media` para datas e expressões curtas; `fc-cifra--longa` para frases na foto larga das edições.
- Recorte a foto deixando a pessoa ou o objeto principal **acima** do terço de baixo: é ali que a cifra fica.
- Em uso: Edição 01 (“R$ 1 milhão ≠ R$ 1 milhão”), *Ganhar não é receber* (“1º de fev.”) e *O direito à partilha não termina na sentença* (“½”, também na capa da página inicial). *O preço do registro* continua com as barras, que já são a arte tipográfica dele.

Para corrigir uma palavra ou um número, edite o HTML direto. Se o texto mudar muito, peça a página nova: ela é gerada de uma vez a partir do texto revisado, com sumário, tempo de leitura e referências conferidos.

## Como subir arquivos sem perder as pastas

O endereço de cada página depende da pasta onde o arquivo está. `textos/o-preco-do-registro.html` só abre se o arquivo estiver **dentro** da pasta `textos`. Se ele cair na raiz do repositório, o link dá "Esta página não existe".

O botão *choose your files* do GitHub sobe os arquivos soltos, na pasta em que você está, e joga fora as pastas. Há dois jeitos seguros:

- **Arraste as pastas, não os arquivos.** Descompacte o zip no computador, abra o repositório no GitHub, clique em *Add file → Upload files* e arraste as **pastas** (`textos`, `css`, `assets`) e os arquivos soltos da raiz para a área de envio. O GitHub mantém a estrutura.
- **Ou suba pasta por pasta.** Entre na pasta no GitHub (por exemplo, clique em `textos`), e só então use *Add file → Upload files*. O arquivo fica dentro dela.

Depois do *Commit changes*, confira: clique na pasta (`textos`, `css`, `assets`) e veja se o arquivo está lá dentro. Se ele aparecer solto na raiz, apague a cópia da raiz e suba de novo pela pasta.

## Como publicar uma edição nova

Use a Edição 01 como modelo, porque ela tem todas as peças prontas.

Cada edição é uma página única, e o nome do arquivo é o endereço que aparece no Google. Use o título da edição, em minúsculas, sem acento, com as palavras separadas por hífen: `edicoes/quando-o-precatorio-entra-no-balanco.html`.

1. **Crie a página.** Copie `edicoes/quando-o-precatorio-entra-no-balanco.html` para `edicoes/titulo-da-nova-edicao.html` (no GitHub: abra o arquivo, *Raw*, copie; depois *Add file → Create new file* com o novo nome).
2. **Troque o cabeçalho da página** (dentro de `<head>`): `<title>`, `description`, `canonical`, `og:url`, `og:image`, `article:published_time`, o autor e a ficha de dados estruturados (`application/ld+json`: título, descrição, imagens, datas e endereço). O `canonical`, o `og:url` e o `mainEntityOfPage` levam o endereço completo da página nova.
3. **Troque a abertura:** número, mês, chapéu, título, linha fina, assinatura e a imagem de abertura (16:9, 2400 × 1350 px).
4. **Troque a ficha e o sumário** no trilho. O sumário aparece duas vezes: uma para tela larga (`sumario-lateral`) e outra para o celular (`sumario-celular`, onde também vai o total de seções). Cada item aponta para o `id` de um intertítulo (`#s1`, `#s2`...). As "Perguntas em aberto" e o "Fecho" também são seções numeradas: na Edição 01, são a 12 e a 13.
5. **Escreva o corpo** com as peças da Edição 01, todas comentadas no código:
   - `tese`, `glosa`, `olho`, `citacao` (as mesmas do modelo de texto);
   - `abre`: o primeiro parágrafo, que ganha a letra capitular;
   - `numero-destaque`: um dado grande com a explicação ao lado;
   - `tabela-editorial`: tabela com fios finos e números alinhados;
   - `grafico`: gráfico em SVG, com uma versão larga e outra estreita (celular);
   - `lista-fina`, `lista-numerada`, `cadeia`, `mapa-riscos`, `sequencia`, `tres-valores`;
   - `em-aberto`: a caixa com as perguntas que ficam para depois (vem logo abaixo do intertítulo numerado);
   - `fim`: no último parágrafo do fecho, desenha o quadradinho terracota que encerra a edição.
6. **Anuncie a edição** no resto do site:
   - `index.html`: troque a capa (número, título, linha fina, assinatura, tempo de leitura, link e imagem quadrada, 1600 × 1600 px);
   - `edicoes.html`: copie o bloco `<section ... id="edicao-01">`, cole **acima** dele e troque os dados;
   - `biblioteca.html`: acrescente a entrada no índice, no topo;
   - **todas as páginas**: troque a orelha direita do cabeçalho (`Edição 01 / Setembro de 2026`);
   - `sitemap.xml`: acrescente o endereço da edição.
7. **Imagem de compartilhamento:** `assets/edicao-02-og.jpg` (1200 × 630 px) para a edição e, se quiser, a mesma imagem como `assets/og-capa.jpg`, que vale para o site inteiro.

Tempo de leitura = palavras do texto ÷ 200, arredondado para cima.

## Como mudar cores, tamanhos e espaços

Abra `css/style.css`. A seção **02. Variáveis** concentra tudo:

- **Cores:** `--papel`, `--tinta`, `--verde`, `--terracota`, `--areia`. Os números de contraste estão no comentário. A areia não pode ser usada como texto sobre o papel (contraste 2,5:1).
- **Tipos:** `--t-texto` (texto corrido), `--t-h1`, `--t-capa` etc. Cada um vai de um piso (celular) a um teto (tela grande).
- **Medidas:** `--medida` (largura da linha de texto, cerca de 66 caracteres), `--trilho` (coluna da margem), `--respiro` (espaço entre seções).

Mude o valor ali e o site inteiro acompanha.

## Regras da casa

- Nenhum `style="..."` dentro do HTML. A política de segurança do site (`Content-Security-Policy`) bloqueia estilo embutido, então ele simplesmente não funciona.
- Nenhum script e nenhum recurso de outro domínio (fontes, analytics, vídeos). Se um dia precisar, a Política de Privacidade tem de ser revista antes.
- Imagens: veja `assets/README.md`.
- O menu e o rodapé se repetem em todas as páginas. Se mudar um item, mude em todos os arquivos (a busca do GitHub, tecla `t`, ajuda a achar).
- A página atual do menu é marcada com `aria-current="page"`. É isso que desenha o fio terracota embaixo da palavra.
- O e-mail de contato é **coutoepedreiralaw@gmail.com**. Se um dia mudar, troque em todas as páginas, no `.well-known/security.txt` e na linha `EMAILS_OFICIAIS` de `.github/verificar_site.py`.
- Depois de cada alteração, confira o ✓ verde ao lado do commit no GitHub. Se aparecer um ✗ vermelho, a verificação automática diz o arquivo, a linha e o que corrigir (veja `SEGURANCA.md`).
- Nunca suba documentos de trabalho (`.docx`, `.xlsx`, `.pdf` de cliente) para o repositório: tudo o que está nele fica público na internet.

## Assinaturas e inscrições

- A assinatura é sempre **Yago do Couto** e **Thaiany Pedreira**: na abertura dos textos, no índice da Biblioteca, no sumário das edições e no expediente. Texto escrito por um só autor leva só o nome de quem escreveu, também no “Como citar”.
- No "Como citar", a mesma forma em padrão ABNT: `COUTO, Yago do; PEDREIRA, Thaiany.`
- As inscrições na OAB (Código de Ética, art. 44) aparecem no expediente, no rodapé de todas as páginas, e embaixo do nome de cada autor na página inicial: Yago do Couto, OAB/MS 25.837; Thaiany Pedreira, OAB/PE 48.342.

## Pendências registradas

- Créditos das fotografias, se forem de banco de imagens.
- `assets/edicao-01.jpg` e `assets/manifesto-02.jpg` não são mais usadas e podem ser apagadas.
