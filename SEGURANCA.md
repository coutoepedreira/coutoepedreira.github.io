# Segurança do site

O site é estático: não tem banco de dados, login, formulário nem JavaScript. Isso já elimina a maior parte dos ataques comuns. Os riscos que sobram são três: alguém tomar a conta do GitHub ou o domínio, alguém publicar algo por engano (um documento, um script, um dado pessoal) e o site ser aberto dentro de outro site para enganar o leitor. Este arquivo diz o que já está resolvido no código, o que a verificação automática confere e o que precisa ser ajustado nas contas.

---

## 1. O que já está no código

- **Política de segurança (CSP) em todas as páginas.** O navegador só aceita estilo, fonte e imagem vindos do próprio site. Script, formulário, quadro (iframe), conexão externa e troca do endereço-base estão bloqueados. Se alguém conseguir enfiar um trecho de código numa página, ele não roda.
- **Política de referência.** Quando o leitor clica num link externo, o outro site não recebe o endereço completo da página de onde ele veio.
- **Nenhum recurso de terceiros.** Fontes, imagens e estilo estão no próprio repositório. Não há Google Fonts, analytics, pixel ou cookie. O site não coleta dado de visitante.
- **security.txt** (`.well-known/security.txt`). Diz a quem encontrar uma falha como avisar vocês (padrão RFC 9116). Vale até 26 de setembro de 2027. A verificação avisa 45 dias antes de vencer.
- **Dados estruturados (JSON-LD)** na página da edição. É uma ficha para o Google, em formato de dados. Não executa nada.

## 2. A verificação automática

Dois arquivos na pasta `.github/`:

- `workflows/verificacao.yml` diz ao GitHub quando rodar: a cada alteração, toda segunda-feira de manhã e quando vocês pedirem.
- `verificar_site.py` faz a conferência. Usa só o Python que já vem no GitHub, não instala nada e não acessa a internet.

Ela para com erro quando encontra:

- página sem a política de segurança, ou com a política alterada;
- script, `style="..."`, `onclick` e afins;
- fonte, imagem ou estilo carregado de outro site;
- link interno quebrado ou âncora que não existe (`#s3`);
- e-mail de contato diferente de coutoepedreiralaw@gmail.com;
- documento de trabalho publicado por engano (`.docx`, `.xlsx`, `.zip`, `.csv`...);
- número de CPF no texto de uma página;
- foto com a localização GPS gravada no arquivo;
- `security.txt` vencido;
- endereço no `sitemap.xml` que não existe.

E avisa, sem travar, quando vê: imagem pesada, foto com metadados de câmera, PDF publicado, CNPJ no texto, página fora do sitemap.

**Onde ver o resultado.** Na página do repositório, ao lado de cada alteração aparece um ✓ verde ou um ✗ vermelho. Na aba **Actions** está a lista de execuções. Abrindo uma execução vermelha, o resumo mostra arquivo, linha e o que corrigir.

**Por que só avisa e não bloqueia.** O GitHub Pages publica direto do ramo principal, então a verificação não tem como segurar a publicação. Ela serve para vocês ficarem sabendo na hora e corrigirem.

## 3. O que o código não resolve: seis ajustes de conta

Leva uns 15 minutos, uma vez só.

1. **Verificação em duas etapas no GitHub.** Foto do perfil → *Settings* → *Password and authentication* → *Enable two-factor authentication*. Use um aplicativo autenticador ou uma passkey. Guarde os códigos de recuperação fora do computador.
2. **Domínio verificado no GitHub.** Impede que outra conta publique algo no endereço de vocês se a configuração do Pages for desfeita um dia. Foto do perfil → *Settings* → *Pages* → *Add a domain* → `coutoepedreira.com.br`. O GitHub mostra um registro TXT. Crie esse registro no Registro.br (*DNS* → *Editar zona*), espere alguns minutos e volte para clicar em *Verify*.
3. **HTTPS obrigatório.** No repositório: *Settings* → *Pages* → marque *Enforce HTTPS*.
4. **Proteção do ramo principal.** No repositório: *Settings* → *Rules* → *Rulesets* → *New branch ruleset*. Em *Enforcement status*, *Active*. Em *Target branches*, *Include default branch*. Marque *Restrict deletions* e *Block force pushes*. Salve. Isso não atrapalha o upload pelo navegador; só impede que o histórico seja apagado ou reescrito.
5. **Registro.br.** Ative a verificação em duas etapas na conta e atualize o e-mail de contato do domínio para coutoepedreiralaw@gmail.com. Quem controla o Registro.br controla o site. Se o painel oferecer DNSSEC, ative. Se permitir registro CAA, crie `0 issue "letsencrypt.org"`: só a autoridade que emite o certificado do GitHub Pages poderá emitir certificados para o domínio.
6. **E-mail de alerta.** Foto do perfil → *Settings* → *Notifications* → *Actions* → marque o envio por e-mail só para execuções que falharem. É por aí que o aviso da verificação chega.

E o básico: o Gmail coutoepedreiralaw@gmail.com também com verificação em duas etapas, porque é ele que recupera as outras contas.

## 4. Um passo além (opcional): cabeçalhos de segurança

O GitHub Pages não deixa o site enviar cabeçalhos HTTP próprios. Três proteções só existem como cabeçalho:

- impedir que o site seja aberto dentro de um quadro em outro endereço (o golpe de clicar em algo por cima da página verdadeira);
- obrigar o navegador a usar HTTPS por um ano, mesmo que alguém digite `http://`;
- desligar recursos do navegador que o site não usa (câmera, microfone, localização).

O caminho é colocar o Cloudflare, no plano gratuito, entre o domínio e o GitHub Pages, e criar uma regra de resposta (*Rules* → *Transform Rules* → *Modify Response Header*) com:

```
Strict-Transport-Security: max-age=31536000
X-Frame-Options: DENY
Content-Security-Policy: frame-ancestors 'none'
X-Content-Type-Options: nosniff
Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(), usb=()
Referrer-Policy: strict-origin-when-cross-origin
```

Exige trocar os servidores DNS do domínio no Registro.br para os do Cloudflare. Façam só depois dos seis ajustes acima, num dia sem publicação.

## 5. Se algo der errado

1. Troquem a senha do GitHub e confiram *Settings* → *Sessions* e o 2FA.
2. No repositório, confiram *Settings* → *Collaborators* e *Settings* → *Deploy keys*: não deve haver ninguém além de vocês.
3. Em *Settings* → *Pages*, confiram se o domínio continua `coutoepedreira.com.br`.
4. O histórico do GitHub guarda todas as versões (*Commits*). Para voltar, abram a última versão boa de cada arquivo e publiquem de novo. O zip mais recente entregue também serve de cópia.

Para relatar uma falha: coutoepedreiralaw@gmail.com.
