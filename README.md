# Site IVAN International Trade

Site institucional da **IVAN International Trader Group Ltda** (nome fantasia IVAN International Trade), em português, inglês e chinês.

Site estático: HTML, CSS e um pouco de JavaScript, sem framework. O formulário de contato não precisa de servidor, porque monta a mensagem e abre o WhatsApp.

## Estrutura

```
content.py          todos os textos, nos 3 idiomas, e os dados da empresa
build.py            gera o site em docs/ (só precisa de Python 3.8+)
src/assets/         CSS, JS, fontes (Archivo, licença OFL), imagens e ícones
docs/               site pronto, que é o que o GitHub Pages publica
```

Páginas geradas: `/` (português), `/en/` e `/zh/`. O endereço `/pt/` leva para a versão em português. Também são gerados `404.html` e `robots.txt`; `sitemap.xml` e `CNAME` só depois que o domínio for definido.

## Editar

1. Mude os textos em `content.py` (ou troque as fotos em `src/assets/img/`, mantendo os nomes).
2. Rode `python3 build.py`.
3. Faça commit da pasta `docs/` junto.

Para ver antes de publicar: `python3 -m http.server -d docs 8000` e abra http://localhost:8000.

## Publicar no GitHub Pages

1. No repositório: **Settings → Pages → Build and deployment**
   - Source: *Deploy from a branch*
   - Branch: `main`, pasta `/docs`
2. O site fica em `https://SEU-USUARIO.github.io/NOME-DO-REPOSITORIO/`. Todos os caminhos são relativos, então ele funciona nesse endereço, inclusive a página 404.

### Quando o domínio estiver pronto

Só depois que o domínio estiver registrado e o DNS configurado (próxima seção):

1. Em `content.py`, preencha `SITE_URL` e `CUSTOM_DOMAIN` com o domínio escolhido (em avaliação: ivanpcb.com.br ou ivangroup.com.br). Ex.: `SITE_URL = "https://ivanpcb.com.br"` e `CUSTOM_DOMAIN = "ivanpcb.com.br"`.
2. Rode `python3 build.py` e faça commit. Isso ativa o canonical, os links hreflang absolutos, o `sitemap.xml` e o arquivo `CNAME`.
3. Em **Settings → Pages**, confirme o domínio e marque **Enforce HTTPS**.

Não preencha o `CUSTOM_DOMAIN` antes do DNS estar pronto: o GitHub passa a redirecionar para o domínio, e o site fica fora do ar até ele funcionar.

## DNS no Registro.br

Em *Registro.br → Domínios → (seu domínio) → DNS → Editar zona* (use os servidores DNS do Registro.br, modo avançado):

| Tipo | Nome | Valor |
|------|------|-------|
| A | (vazio) | 185.199.108.153 |
| A | (vazio) | 185.199.109.153 |
| A | (vazio) | 185.199.110.153 |
| A | (vazio) | 185.199.111.153 |
| AAAA | (vazio) | 2606:50c0:8000::153 |
| AAAA | (vazio) | 2606:50c0:8001::153 |
| AAAA | (vazio) | 2606:50c0:8002::153 |
| AAAA | (vazio) | 2606:50c0:8003::153 |
| CNAME | www | SEU-USUARIO.github.io |

A propagação costuma levar de alguns minutos a algumas horas.

## Pontos que dependem de confirmação

- **MAX-500:** os termos "cabeça grande / cabeça pequena" e "sobreposição / separação" foram mantidos como no documento original. Confirmar com o fabricante.
- **MAX-500, alimentação:** "400 W/H" foi mantido como no documento. Provavelmente é 400 W de consumo.
- **MAX600:** "aplicação de anéis" é uma sugestão comercial. Confirmar se é o termo usado pelo fabricante.
- **Linha PTH (2026):** o documento em inglês diz "electroless copper", e o site usa "deposição química de cobre". Não usar "cobre eletrolítico" sem confirmação.
- **Nomes de clientes:** mantidos como no documento. Dois parecem ter tradução diferente do nome oficial: 依顿 ("Eliant", provavelmente Ellington Electronics) e 金洲 ("Shenzhen Jincheng Precision Technology", provavelmente Jinzhou Precision).
- **Endereço:** "Condomínio Portal Anhangueira" está como no documento. O nome comum da região é Anhanguera.
- **Logo e e-mail:** o site usa a marca "IVAN" em texto e não publica e-mail.
- **WhatsApp:** confirmar que o +55 11 95849-6113 atende por WhatsApp.
