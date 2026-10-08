#!/usr/bin/env python3
"""
Verificação do site coutoepedreira.com.br

Roda sozinha no GitHub (veja .github/workflows/verificacao.yml) a cada
alteração, toda segunda-feira e quando você pedir. Também roda no seu
computador, se quiser:  python3 .github/verificar_site.py

Ela confere as regras da casa e para com erro (execução vermelha no GitHub,
e-mail para você) quando encontra algo que abre uma brecha ou quebra o site:

  - página sem a política de segurança, ou com a política alterada;
  - script, estilo embutido, evento "onclick" e afins;
  - recurso carregado de outro site (fonte, imagem, estilo);
  - link interno quebrado ou âncora (#s3) que não existe;
  - e-mail de contato diferente do oficial;
  - documento de trabalho publicado por engano (.docx, .xlsx, .zip...);
  - número de CPF no texto de uma página;
  - foto com localização GPS gravada no arquivo;
  - security.txt vencido;
  - endereço do sitemap que não existe.

Avisos (amarelos) não travam nada: são lembretes.

Usa só a biblioteca padrão do Python. Não instala nada, não acessa a internet.
"""

import json
import os
import re
import sys
from datetime import datetime, timezone
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote

# ---------------------------------------------------------------------------
# CONFIGURAÇÃO DA CASA (mude aqui, se um dia precisar)
# ---------------------------------------------------------------------------
DOMINIO = "https://coutoepedreira.com.br"

# O único e-mail que pode aparecer em links "mailto:" no site.
EMAILS_OFICIAIS = {"coutoepedreiralaw@gmail.com"}

# A política de segurança que toda página precisa ter, exatamente assim.
# Se mudar a política no HTML, mude aqui também (e o contrário).
CSP_ESPERADA = (
    "default-src 'none'; img-src 'self'; style-src 'self'; font-src 'self'; "
    "script-src 'none'; object-src 'none'; frame-src 'none'; connect-src 'none'; "
    "base-uri 'none'; form-action 'none'; upgrade-insecure-requests"
)

# Arquivos que não devem ir para o site (e, portanto, para a internet).
# Um .docx de cliente publicado por engano fica acessível a qualquer pessoa.
EXTENSOES_PROIBIDAS = {
    ".doc", ".docx", ".odt", ".rtf", ".pages",
    ".xls", ".xlsx", ".ods", ".numbers", ".csv",
    ".ppt", ".pptx", ".key",
    ".zip", ".rar", ".7z", ".tar", ".gz",
    ".env", ".pem", ".p12", ".pfx", ".crt", ".sqlite", ".db", ".bak",
}
# PDF pode ser publicado de propósito (um artigo, um e-book): só avisa.
EXTENSOES_AVISO = {".pdf"}
# Nomes de arquivo que nunca devem subir.
NOMES_PROIBIDOS = {".DS_Store", "Thumbs.db", "desktop.ini", "id_rsa", "id_ed25519"}

PASTAS_IGNORADAS = {".git", ".github", "node_modules"}
LIMITE_IMAGEM_KB = 800
DIAS_AVISO_SECURITY_TXT = 45

# ---------------------------------------------------------------------------
RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
erros, avisos = [], []


def erro(arquivo, linha, msg):
    erros.append((arquivo, linha, msg))


def aviso(arquivo, linha, msg):
    avisos.append((arquivo, linha, msg))


def rel(caminho):
    return os.path.relpath(caminho, RAIZ).replace(os.sep, "/")


def todos_os_arquivos():
    for pasta, subpastas, arquivos in os.walk(RAIZ):
        subpastas[:] = [p for p in subpastas if p not in PASTAS_IGNORADAS]
        for nome in arquivos:
            yield os.path.join(pasta, nome)


# ---------------------------------------------------------------------------
# Leitura das páginas
# ---------------------------------------------------------------------------
class Pagina(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tags = []          # (tag, attrs, linha)
        self.ids = {}           # id -> linha
        self.scripts = []       # (type, conteúdo, linha)
        self.estilos = []       # linhas de <style>
        self.texto = []         # texto visível, para procurar CPF
        self._no_script = None
        self._ignorar_texto = 0

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or "") for k, v in attrs}
        linha = self.getpos()[0]
        self.tags.append((tag, a, linha))
        if "id" in a:
            if a["id"] in self.ids:
                erro(self.arquivo, linha, f'id repetido na mesma página: "{a["id"]}" (a âncora fica ambígua).')
            self.ids[a["id"]] = linha
        if tag == "script":
            self._no_script = [a.get("type", ""), "", linha]
        if tag == "style":
            self.estilos.append(linha)
        if tag in ("script", "style"):
            self._ignorar_texto += 1

    def handle_endtag(self, tag):
        if tag == "script" and self._no_script is not None:
            self.scripts.append(tuple(self._no_script))
            self._no_script = None
        if tag in ("script", "style") and self._ignorar_texto:
            self._ignorar_texto -= 1

    def handle_data(self, data):
        if self._no_script is not None:
            self._no_script[1] += data
        elif not self._ignorar_texto:
            self.texto.append((data, self.getpos()[0]))


def ler_pagina(caminho):
    p = Pagina()
    p.arquivo = rel(caminho)
    with open(caminho, encoding="utf-8") as f:
        p.feed(f.read())
    return p


# ---------------------------------------------------------------------------
# Resolução de links internos
# ---------------------------------------------------------------------------
def alvo_interno(pagina_rel, href):
    """Devolve (arquivo_alvo_rel, âncora) para links internos; None para externos."""
    href = href.strip()
    if not href or href.startswith(("mailto:", "tel:", "data:")):
        return None
    if href.startswith(DOMINIO):
        href = href[len(DOMINIO):] or "/"
    partes = urlsplit(href)
    if partes.scheme or partes.netloc:
        return None  # outro site
    caminho, ancora = unquote(partes.path), partes.fragment
    if not caminho:
        return pagina_rel, ancora
    if caminho.startswith("/"):
        base = caminho.lstrip("/")
    else:
        base = os.path.normpath(os.path.join(os.path.dirname(pagina_rel), caminho)).replace(os.sep, "/")
    if caminho.endswith("/") and base not in ("", "."):
        base = base.rstrip("/") + "/index.html"
    if base in ("", "."):
        base = "index.html"
    # O GitHub Pages também serve "pagina" como "pagina.html".
    if not os.path.exists(os.path.join(RAIZ, base)) and os.path.exists(os.path.join(RAIZ, base + ".html")):
        base += ".html"
    return base, ancora


# ---------------------------------------------------------------------------
# Fotos: localização GPS gravada no arquivo
# ---------------------------------------------------------------------------
def exif_jpeg(caminho):
    """Devolve None (sem EXIF), ou {'gps': bool} quando há EXIF."""
    with open(caminho, "rb") as f:
        d = f.read()
    if d[:2] != b"\xff\xd8":
        return None
    i = 2
    while i + 4 <= len(d) and d[i] == 0xFF:
        marcador = d[i + 1]
        if marcador in (0xD9, 0xDA):
            break
        tam = int.from_bytes(d[i + 2:i + 4], "big")
        if marcador == 0xE1 and d[i + 4:i + 10] == b"Exif\x00\x00":
            t = d[i + 10:i + 2 + tam]
            ordem = "little" if t[:2] == b"II" else "big"
            try:
                inicio = int.from_bytes(t[4:8], ordem)
                n = int.from_bytes(t[inicio:inicio + 2], ordem)
                tags = {int.from_bytes(t[inicio + 2 + 12 * k:inicio + 4 + 12 * k], ordem) for k in range(n)}
            except Exception:
                tags = set()
            return {"gps": 0x8825 in tags}
        i += 2 + tam
    return None


# ---------------------------------------------------------------------------
# VERIFICAÇÕES
# ---------------------------------------------------------------------------
def verificar_arquivos_soltos():
    for caminho in todos_os_arquivos():
        nome = os.path.basename(caminho)
        ext = os.path.splitext(nome)[1].lower()
        r = rel(caminho)
        if nome in NOMES_PROIBIDOS or ext in EXTENSOES_PROIBIDAS:
            erro(r, 1, "Arquivo que não deve ser publicado. Tudo o que está no repositório fica acessível na internet. Apague do GitHub.")
        elif ext in EXTENSOES_AVISO:
            aviso(r, 1, "PDF publicado. Confirme que é para ser público e que não traz dados de cliente.")
        if ext in (".jpg", ".jpeg", ".png", ".webp"):
            kb = os.path.getsize(caminho) // 1024
            if kb > LIMITE_IMAGEM_KB:
                aviso(r, 1, f"Imagem pesada ({kb} KB). Acima de {LIMITE_IMAGEM_KB} KB a página demora a abrir no celular.")
        if ext in (".jpg", ".jpeg"):
            ex = exif_jpeg(caminho)
            if ex and ex["gps"]:
                erro(r, 1, "A foto guarda a localização GPS de onde foi tirada. Exporte de novo sem metadados antes de publicar.")
            elif ex:
                aviso(r, 1, "A foto guarda metadados (câmera, data). Não é grave, mas o ideal é exportar sem eles.")


def verificar_css():
    pasta = os.path.join(RAIZ, "css")
    for nome in sorted(os.listdir(pasta)) if os.path.isdir(pasta) else []:
        if not nome.endswith(".css"):
            continue
        caminho = os.path.join(pasta, nome)
        with open(caminho, encoding="utf-8") as f:
            linhas = f.read().split("\n")
        for n, linha in enumerate(linhas, 1):
            if "@import" in linha:
                erro(rel(caminho), n, "@import carrega estilo de outro lugar. Mantenha tudo em style.css.")
            for url in re.findall(r"url\(\s*['\"]?([^'\")]+)", linha):
                if re.match(r"^(https?:)?//", url):
                    erro(rel(caminho), n, f"Recurso de outro site no CSS: {url}")
                elif not url.startswith("data:"):
                    alvo = os.path.normpath(os.path.join(pasta, url.split("#")[0].split("?")[0]))
                    if not os.path.exists(alvo):
                        erro(rel(caminho), n, f"O CSS aponta para um arquivo que não existe: {url}")


def verificar_paginas():
    paginas = {}
    for caminho in todos_os_arquivos():
        if caminho.endswith(".html"):
            paginas[rel(caminho)] = ler_pagina(caminho)

    for arq, p in sorted(paginas.items()):
        metas = [(a, l) for t, a, l in p.tags if t == "meta"]
        csp = [(a.get("content", ""), l) for a, l in metas if a.get("http-equiv", "").lower() == "content-security-policy"]
        refresh = any(a.get("http-equiv", "").lower() == "refresh" for a, l in metas)
        robots = " ".join(a.get("content", "") for a, l in metas if a.get("name", "").lower() == "robots").lower()

        # 1. Política de segurança
        if not csp:
            erro(arq, 1, "Página sem a política de segurança (Content-Security-Policy). Copie a linha do cabeçalho de outra página.")
        elif " ".join(csp[0][0].split()) != CSP_ESPERADA:
            erro(arq, csp[0][1], "A política de segurança desta página é diferente da oficial. Se foi de propósito, atualize CSP_ESPERADA em .github/verificar_site.py.")
        if not any(a.get("name", "").lower() == "referrer" for a, l in metas):
            erro(arq, 1, 'Falta <meta name="referrer" content="strict-origin-when-cross-origin">.')

        # 2. Scripts: só a ficha de dados estruturados (JSON-LD), que não executa nada.
        for tipo, conteudo, linha in p.scripts:
            if tipo.lower() != "application/ld+json":
                erro(arq, linha, "Script na página. O site não usa JavaScript; a política de segurança bloquearia de qualquer jeito.")
            else:
                try:
                    json.loads(conteudo)
                except ValueError as e:
                    erro(arq, linha, f"Dados estruturados (JSON-LD) com erro de digitação: {e}")

        # 3. Estilo embutido e eventos
        for linha in p.estilos:
            erro(arq, linha, "Bloco <style> na página. Os estilos ficam em css/style.css.")
        for tag, a, linha in p.tags:
            if "style" in a:
                erro(arq, linha, f'Atributo style="..." em <{tag}>. A política de segurança bloqueia; use uma classe no style.css.')
            for nome, valor in a.items():
                if nome.startswith("on"):
                    erro(arq, linha, f'Evento "{nome}" em <{tag}>. O site não executa scripts.')
                if nome in ("href", "src", "action", "formaction") and valor.strip().lower().startswith("javascript:"):
                    erro(arq, linha, f'Link "javascript:" em <{tag}>.')

        # 4. Recursos de fora e links
        for tag, a, linha in p.tags:
            recurso = None
            if tag in ("img", "source", "audio", "video", "track", "embed", "iframe", "script"):
                recurso = a.get("src") or a.get("srcset", "").split(" ")[0] or None
            elif tag == "object":
                recurso = a.get("data")
            elif tag == "link" and a.get("rel", "").lower() not in ("canonical", "alternate", "me"):
                recurso = a.get("href")
            if recurso:
                if re.match(r"^(https?:)?//", recurso) and not recurso.startswith(DOMINIO):
                    erro(arq, linha, f"<{tag}> carrega recurso de outro site: {recurso}")
                else:
                    alvo = alvo_interno(arq, recurso)
                    if alvo and not os.path.exists(os.path.join(RAIZ, alvo[0])):
                        erro(arq, linha, f"<{tag}> aponta para um arquivo que não existe: {recurso}")
            if tag == "img":
                if "alt" not in a:
                    erro(arq, linha, "Imagem sem texto alternativo (alt). Quem usa leitor de tela fica sem saber o que é.")
                if not a.get("width") or not a.get("height"):
                    aviso(arq, linha, "Imagem sem width e height: a página pula enquanto carrega.")
            if tag == "a":
                href = a.get("href", "")
                if a.get("target", "").lower() == "_blank" and "noopener" not in a.get("rel", "").lower():
                    erro(arq, linha, 'Link que abre nova aba sem rel="noopener noreferrer".')
                if href.lower().startswith("mailto:"):
                    email = href[7:].split("?")[0].strip().lower()
                    if email not in EMAILS_OFICIAIS:
                        erro(arq, linha, f"E-mail diferente do oficial: {email}")
                    continue
                if href.startswith("http://"):
                    aviso(arq, linha, f"Link sem https: {href}")
                alvo = alvo_interno(arq, href)
                if alvo is None:
                    continue
                destino, ancora = alvo
                if not os.path.exists(os.path.join(RAIZ, destino)):
                    erro(arq, linha, f"Link quebrado: {href}")
                elif ancora and destino.endswith(".html"):
                    alvo_p = paginas.get(destino)
                    if alvo_p is not None and ancora not in alvo_p.ids:
                        erro(arq, linha, f'Âncora que não existe: {href} (não há id="{ancora}" em {destino}).')

        # 5. Endereço canônico (o que o Google indexa)
        canon = [(a.get("href", ""), l) for t, a, l in p.tags if t == "link" and a.get("rel", "").lower() == "canonical"]
        indexavel = "noindex" not in robots and not refresh and arq != "404.html"
        if indexavel:
            esperado = {f"{DOMINIO}/{arq}"}
            if arq == "index.html":
                esperado |= {f"{DOMINIO}/", DOMINIO}
            if not canon:
                erro(arq, 1, "Página sem endereço canônico (<link rel=\"canonical\">).")
            elif canon[0][0] not in esperado:
                erro(arq, canon[0][1], f"Endereço canônico não bate com o arquivo: {canon[0][0]}")
            og = [a.get("content", "") for t, a, l in p.tags if t == "meta" and a.get("property") == "og:url"]
            if canon and og and og[0] != canon[0][0]:
                erro(arq, 1, "og:url diferente do endereço canônico (o compartilhamento aponta para outro endereço).")

        # 6. Dados pessoais no texto
        for trecho, linha in p.texto:
            if re.search(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b", trecho):
                erro(arq, linha, "Parece haver um CPF no texto da página. Dado pessoal não vai para o site.")
            if re.search(r"\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b", trecho):
                aviso(arq, linha, "Há um CNPJ no texto. Confirme que é para ser público.")

    return paginas


def verificar_sitemap(paginas):
    caminho = os.path.join(RAIZ, "sitemap.xml")
    if not os.path.exists(caminho):
        erro("sitemap.xml", 1, "sitemap.xml não encontrado.")
        return
    with open(caminho, encoding="utf-8") as f:
        texto = f.read()
    locs = re.findall(r"<loc>\s*([^<]+?)\s*</loc>", texto)
    no_sitemap = set()
    for loc in locs:
        if not loc.startswith(DOMINIO):
            erro("sitemap.xml", 1, f"Endereço de outro domínio no sitemap: {loc}")
            continue
        caminho_rel = loc[len(DOMINIO):].lstrip("/") or "index.html"
        no_sitemap.add(caminho_rel)
        p = paginas.get(caminho_rel)
        if p is None:
            erro("sitemap.xml", 1, f"O sitemap lista um endereço que não existe: {loc}")
            continue
        robots = " ".join(a.get("content", "") for t, a, l in p.tags if t == "meta" and a.get("name") == "robots").lower()
        if "noindex" in robots:
            erro("sitemap.xml", 1, f"O sitemap lista uma página marcada para não aparecer no Google: {loc}")
    for arq, p in paginas.items():
        robots = " ".join(a.get("content", "") for t, a, l in p.tags if t == "meta" and a.get("name") == "robots").lower()
        refresh = any(t == "meta" and a.get("http-equiv", "").lower() == "refresh" for t, a, l in p.tags)
        if "noindex" not in robots and not refresh and arq != "404.html" and arq not in no_sitemap:
            aviso(arq, 1, "Página publicada que não está no sitemap.xml (o Google demora mais a achar).")


def verificar_security_txt():
    arq = ".well-known/security.txt"
    caminho = os.path.join(RAIZ, arq)
    if not os.path.exists(caminho):
        erro(arq, 1, "security.txt não encontrado.")
        return
    with open(caminho, encoding="utf-8") as f:
        linhas = f.read().split("\n")
    campos = {}
    for n, linha in enumerate(linhas, 1):
        if ":" in linha and not linha.startswith("#"):
            k, v = linha.split(":", 1)
            campos[k.strip().lower()] = (v.strip(), n)
    if "contact" not in campos:
        erro(arq, 1, "security.txt sem a linha Contact.")
    else:
        email = campos["contact"][0].replace("mailto:", "").strip().lower()
        if email not in EMAILS_OFICIAIS:
            erro(arq, campos["contact"][1], f"E-mail do security.txt diferente do oficial: {email}")
    if "expires" not in campos:
        erro(arq, 1, "security.txt sem a linha Expires.")
        return
    valor, n = campos["expires"]
    try:
        validade = datetime.fromisoformat(valor.replace("Z", "+00:00"))
    except ValueError:
        erro(arq, n, f"Data de validade ilegível: {valor}")
        return
    dias = (validade - datetime.now(timezone.utc)).days
    if dias < 0:
        erro(arq, n, "security.txt vencido. Troque a data de Expires para daqui a um ano.")
    elif dias < DIAS_AVISO_SECURITY_TXT:
        aviso(arq, n, f"security.txt vence em {dias} dias. Troque a data de Expires para daqui a um ano.")
    elif dias > 366:
        aviso(arq, n, "Validade do security.txt maior que um ano. O padrão recomenda no máximo um ano.")


# ---------------------------------------------------------------------------
def relatorio():
    no_github = os.environ.get("GITHUB_ACTIONS") == "true"
    for tipo, lista in (("error", erros), ("warning", avisos)):
        for arq, linha, msg in lista:
            if no_github:
                print(f"::{tipo} file={arq},line={linha}::{msg}")
            else:
                rotulo = "ERRO " if tipo == "error" else "AVISO"
                print(f"{rotulo}  {arq}:{linha}  {msg}")

    resumo = os.environ.get("GITHUB_STEP_SUMMARY")
    if resumo:
        with open(resumo, "a", encoding="utf-8") as f:
            f.write("## Verificação do site\n\n")
            if not erros and not avisos:
                f.write("Tudo certo. Nenhum erro, nenhum aviso.\n")
            else:
                f.write(f"**{len(erros)} erro(s)** e **{len(avisos)} aviso(s)**.\n\n")
                f.write("| | Arquivo | Linha | O que foi encontrado |\n|---|---|---|---|\n")
                for tipo, lista in (("Erro", erros), ("Aviso", avisos)):
                    for arq, linha, msg in lista:
                        f.write(f"| {tipo} | `{arq}` | {linha} | {msg.replace('|', '/')} |\n")

    print(f"\n{len(erros)} erro(s), {len(avisos)} aviso(s).")
    if not erros:
        print("Tudo dentro das regras da casa.")


if __name__ == "__main__":
    verificar_arquivos_soltos()
    verificar_css()
    paginas = verificar_paginas()
    verificar_sitemap(paginas)
    verificar_security_txt()
    relatorio()
    sys.exit(1 if erros else 0)
