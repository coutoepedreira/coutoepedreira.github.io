# coutoepedreira.com.br

Site editorial de Couto & Pedreira Advocacia Consultiva: Direito, patrimônio, créditos judiciais e economia.

Versão 3.0, setembro de 2026. HTML e CSS puros, sem scripts, sem dependências e sem recursos de fora. Publicado pelo GitHub Pages.

---

## O que tem em cada pasta

```
/
├── index.html          Início: capa da edição, Biblioteca, Manifesto, Autores, Escritório
├── biblioteca.html     Índice de textos e os cinco formatos
├── edicoes.html        Lista de edições (a mais nova primeiro)
├── manifesto.html
├── metodologia.html
├── termos.html
├── privacidade.html
├── 404.html            Página de erro (usa caminhos absolutos, de propósito)
├── textos/
│   └── modelo.html     MODELO de texto. Copie este arquivo para publicar.
├── css/style.css       Toda a aparência do site. Comentado, com índice no topo.
├── fonts/              Newsreader e Montserrat, servidas pelo próprio site (+ licenças)
├── assets/             Imagens, ícones e a imagem de compartilhamento
├── sitemap.xml         Mapa do site para buscadores
├── robots.txt
├── favicon.ico
├── CNAME               Domínio (não mexa)
└── .nojekyll           Diz ao GitHub para servir os arquivos como estão (não mexa)
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
7. **Acrescente o endereço no `sitemap.xml`.**
8. *Commit changes.* Em um ou dois minutos o texto está no ar.

## Como abrir uma edição nova

1. Em `edicoes.html`, copie o bloco `<section ... id="edicao-01">` inteiro e cole **acima** dele. Troque número, mês, título, linha fina, imagem e sumário.
2. Em `index.html`, troque a capa (número, mês, título, linha fina, imagem).
3. Em **todas** as páginas, troque a orelha direita do cabeçalho (`Edição 01 / Setembro de 2026`).
4. Se quiser, gere uma nova `assets/og-capa.jpg` (1200 × 630 px) com a capa da edição.

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

## Assinaturas e inscrições

- A assinatura é sempre **Yago do Couto** e **Thaiany Pedreira**: na abertura dos textos, no índice da Biblioteca, no sumário das edições e no expediente.
- No "Como citar", a mesma forma em padrão ABNT: `COUTO, Yago do; PEDREIRA, Thaiany.`
- As inscrições na OAB (Código de Ética, art. 44) aparecem no expediente, no rodapé de todas as páginas, e embaixo do nome de cada autor na página inicial: Yago do Couto, OAB/MS 25.837; Thaiany Pedreira, OAB/PE 48.342.

## Pendências registradas

- Créditos das fotografias, se forem de banco de imagens.
