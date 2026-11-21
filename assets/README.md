# Imagens

Imagens usadas no site da Couto & Pedreira.

| Arquivo | Onde aparece | Proporção na tela |
| --- | --- | --- |
| `edicao-01-capa.jpg` | Abertura da Edição 01 (`edicoes/quando-o-precatorio-entra-no-balanco.html`) | 16:9, 2400 × 1350 px |
| `edicao-01-capa-quadrada.jpg` | Capa da página inicial e página Edições | 1:1, 1600 × 1600 px |
| `edicao-01-autos.jpg` | Imagem interna da Edição 01, em duotom (tinta e papel) | 2:1, 2400 × 1200 px |
| `edicao-01-og.jpg` | Prévia ao compartilhar o link da Edição 01 | 1200 × 630 px |
| `edicao-01.jpg` | Não é mais usada. Pode apagar. | — |
| `manifesto-03.jpg` | Chamada do manifesto (início) e abertura do Manifesto | 2:3 e 3:4, em preto e branco |
| `biblioteca-abertura.jpg` | Abertura da Biblioteca (Real Gabinete Português de Leitura) | 3:4, 1080 × 1440 px |
| `guia-ganhar-abertura.jpg` | Abertura de *Ganhar não é receber* | 3:4, 1080 × 1440 px |
| `interpretacao-partilha-abertura.jpg` | Abertura de *O direito à partilha não termina na sentença* | 3:4, 1080 × 1440 px |
| `interpretacao-partilha-capa.jpg` | Capa da página inicial até 16 nov. 2026 (texto da Thaiany Pedreira). Fora da capa, pode ficar guardada | 1:1, 1400 × 1400 px |
| `ensaio-casamento-abertura.jpg` | Abertura de *O casamento começa antes do altar* (foto de Sinitta Leunen / Unsplash) | 3:4, 1080 × 1440 px |
| `ensaio-casamento-capa.jpg` | Capa da página inicial (o ensaio, desde 17 nov. 2026) | 1:1, 1400 × 1400 px |
| `manifesto-02.jpg` | Não é mais usada. Pode apagar. | — |
| `manifesto-01.jpg` | Abertura da Metodologia | 21:9, em preto e branco |
| `yago-do-couto.jpg`, `thaiany-pedreira.jpg` | Autores (início) | 3:4, em preto e branco |
| `og-capa.jpg` | Prévia ao compartilhar o link (WhatsApp, LinkedIn) | 1200 × 630 px |
| `guia-ganhar-nao-e-receber-og.jpg`, `interpretacao-o-direito-a-partilha-og.jpg`, `analise-o-preco-do-registro-og.jpg`, `ensaio-o-casamento-comeca-antes-do-altar-og.jpg` | Prévia ao compartilhar cada texto | 1200 × 630 px |
| `favicon.svg`, `favicon-32.png`, `apple-touch-icon.png` (e `/favicon.ico`) | Ícone da aba e da tela inicial do celular: o símbolo em Vazante sobre Rio à noite, no corte para tamanho pequeno (as cores da assinatura escura) | quadrado |
| `marca/assinatura-horizontal.svg` | Cabeçalho de todas as páginas (versão papel: símbolo Vazante, texto Mata) | vetor, 280 px de largura na tela |
| `marca/assinatura-vertical-escuro.svg` | Rodapé (versão escuro: símbolo Vazante, texto Garça, só sobre Rio à noite) | vetor, 180 px |
| `marca/simbolo.svg` | O símbolo sozinho, em Vazante | vetor |
| `marca/assinatura-email.png` | Logotipo das assinaturas de e-mail (carregado do site pelos programas de e-mail) | 400 × 59 px, fundo transparente |

Regras para imagens novas:

- O site mostra todas as fotos em preto e branco (o CSS faz isso sozinho). Escolha fotos com bom contraste de luz e sombra: é o que sustenta a imagem sem cor.
- JPG com qualidade entre 70 e 85, lado maior entre 1400 e 1800 px, abaixo de 350 KB.
- Exporte sem metadados (EXIF). Foto de celular costuma guardar o lugar onde foi tirada; a verificação automática recusa foto com GPS.
- Nome em minúsculas, sem acento e sem espaço: `edicao-02.jpg`, `precatorio-balanco.jpg`.
- No HTML, sempre com `width`, `height` e um `alt` que descreva a imagem para quem não enxerga.
- Fotos de abertura, capa, manifesto, autores e edições já saem em preto e branco. Em outra foto, use a classe `pb` no `<img>`. Gráficos e imagens de dados não levam `pb`.
- Tratamento: nada de filtro de aplicativo, vinheta ou moldura. A foto é documento, não decoração.
- Crédito do fotógrafo na legenda: `Foto: Nome / Unsplash`.
