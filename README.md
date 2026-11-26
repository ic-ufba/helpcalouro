# HelpCalouro UFBA

**Guia de sobrevivência do calouro da Universidade Federal da Bahia.**
Tudo o que importa nas primeiras semanas, num só lugar e sem burocratês: primeiros passos, SIGAA, matrícula, regras acadêmicas, RU, Buzufba, bibliotecas, assistência estudantil, saúde, oportunidades e um mapa dos campi com rota no celular.

**Acesse:** https://ic-ufba.github.io/helpcalouro/

> **Projeto independente, não oficial.** O HelpCalouro não é uma página da UFBA: foi desenvolvido por uma estudante, de forma voluntária, para a comunidade. As informações são conferidas em fontes oficiais, mas em caso de divergência valem sempre os canais oficiais da universidade.
>
> Desenvolvido por **Eduarda Almeida** ([@adaah](https://github.com/adaah)).

![Prévia do HelpCalouro](assets/og-image.png)

---

## O que tem no site

| Seção | Conteúdo |
|---|---|
| Começar | Roteiro da primeira semana, checklist e matrícula de ingresso |
| Estudar | SIGAA na prática (horário 24N12, notas, documentos), regras do REGPG, cursos e onde achar informação de cada um, bibliotecas e sistemas (Central de Autenticação, e-mail, Wi-Fi, bibliotecas digitais) |
| Viver a UFBA | **Mapa dos campi**, campi e Buzufba, assistência estudantil (PROAE) e saúde |
| Aproveitar | Pesquisa, extensão, monitoria, intercâmbio, idiomas, cultura e lazer |
| Ajuda | Dúvidas frequentes e glossário de siglas |

Também tem uma busca que entende o jeito de falar do estudante: “bandejão” leva ao RU, “busu” ao Buzufba, “onde fica a Poli” ao mapa.

### Mapa dos campi

- 102 locais em Ondina, Federação, São Lázaro, Canela e Centro: unidades, pavilhões, RU e pontos de distribuição, 20 bibliotecas, residências, atendimento, saúde, cultura, entradas, pontos de ônibus e bicicletas.
- “Como chegar” abre o app de mapas do aparelho (Apple Maps no iPhone, Google Maps nos demais) já com o destino marcado. Também há atalhos para Google Maps, Waze e copiar endereço.
- “Perto de mim” ordena os locais pela distância.
- As posições vêm do OpenStreetMap e foram conferidas com os endereços da Carta de Serviços e da PROAE. Pins com **borda tracejada** são aproximados.

---

## Estrutura do repositório

```
helpcalouro/
├── index.html              ← o site (gerado; é o que o GitHub Pages publica)
├── 404.html                ← página de “não encontrado”
├── manifest.webmanifest    ← permite instalar como app
├── sw.js                   ← service worker (funciona offline após a 1ª visita)
├── favicon.ico
├── robots.txt / sitemap.xml
├── .nojekyll               ← diz ao GitHub Pages para publicar os arquivos como estão
├── assets/
│   ├── og-image.png        ← imagem da prévia de link (1200×630)
│   └── icons/              ← ícones do app e favicon
├── src/                    ← código-fonte para editar
│   ├── base.html           ← páginas e todos os dados (textos, links, locais do mapa)
│   ├── styles.css          ← estilos da identidade visual
│   ├── map.js              ← funcionamento do mapa
│   ├── head.html           ← SEO, prévia de link e ícones (vai para o <head>)
│   └── build.py            ← junta tudo e gera o index.html
└── package.json            ← dependências do build (ícones e biblioteca do mapa)
```

O site é **um único arquivo** (`index.html`): CSS, JavaScript, ícones e a biblioteca do mapa vão embutidos. Não precisa de servidor nem de banco de dados.

---

## Como publicar no GitHub Pages

1. Envie o conteúdo desta pasta para o repositório `ic-ufba/helpcalouro` (pelo botão **Add file › Upload files** ou com `git push`). A pasta `node_modules/` não deve ser enviada.
2. Em **Settings › Pages**, escolha **Deploy from a branch**, branch **main**, pasta **/(root)** e salve.
3. Em 1 ou 2 minutos o site fica no ar em https://ic-ufba.github.io/helpcalouro/.

Para atualizar, basta enviar o novo `index.html` (e os outros arquivos alterados). O Pages republica sozinho.

---

## Como editar o conteúdo

Edite os arquivos em `src/` e gere o site de novo:

```bash
npm install            # só na primeira vez (baixa ícones e a biblioteca do mapa)
npm run build          # ou: python3 src/build.py
```

Isso reescreve o `index.html` na raiz. Precisa de Node.js (para o `npm install`) e Python 3.

**Onde fica cada coisa em `src/base.html`** (procure pelo nome):

| Dado | Variável |
|---|---|
| Locais do mapa | `MP` (cada linha: id, sigla, categoria, campus, nome, latitude, longitude, endereço, dica, aproximado, prédio-sede) |
| Categorias e cores do mapa | `MCATS` |
| Sistemas e portais | `SYS` |
| Dúvidas frequentes | `FAQ` |
| Glossário de siglas | `GLOS` |
| Cursos | `CURS` e `UNIS` (sites das unidades) |
| Unidades (endereços e telefones) | `UNID` |
| Bibliotecas | `BIB` |
| Assistência, saúde, oportunidades, cultura | `APOIO`, `SAUDE`, `OPS`, `CULT`, `CUR` |
| Itens da busca | `IDX` |

Para corrigir a posição de um pin, troque latitude e longitude na linha do local em `MP`. Um jeito fácil de achar as coordenadas: no Google Maps, clique com o botão direito no prédio e copie os números.

---

## Instalar como app

O site pode ser instalado na tela inicial e abre em tela cheia, como um aplicativo:

- **Android (Chrome):** menu **⋮ › Instalar app** (ou “Adicionar à tela inicial”).
- **iPhone (Safari):** botão **Compartilhar › Adicionar à Tela de Início**.
- **Computador (Chrome/Edge):** ícone de instalar na barra de endereço.

Depois da primeira visita, as páginas funcionam mesmo sem internet. O mapa de fundo e as rotas precisam de conexão.

Ao publicar uma mudança grande, aumente o número de `VERSAO` no `sw.js` (por exemplo, `helpcalouro-v2`) para que quem instalou receba a versão nova na hora.

---

## Prévia de link

Ao compartilhar o endereço no WhatsApp, Instagram, Telegram, LinkedIn ou X, aparece o cartão com imagem, título e descrição. Tudo isso está em `src/head.html`.

- O WhatsApp guarda a prévia por um tempo. Se mudar a imagem, pode levar alguns dias para atualizar em conversas antigas.
- Para conferir: [opengraph.xyz](https://www.opengraph.xyz/) ou o [Depurador de Compartilhamento do Facebook](https://developers.facebook.com/tools/debug/).

**Se o endereço do site mudar** (outro repositório ou domínio próprio), troque `https://ic-ufba.github.io/helpcalouro/` em: `src/head.html`, `robots.txt`, `sitemap.xml`, e o caminho `/helpcalouro/` em `404.html` e no `"id"` do `manifest.webmanifest`. Depois rode o build.

---

## Créditos e licenças

- Dados do mapa: © colaboradores do [OpenStreetMap](https://www.openstreetmap.org/copyright) (ODbL).
- Mapa de fundo: [OpenFreeMap](https://openfreemap.org/) e [OpenMapTiles](https://www.openmaptiles.org/).
- Biblioteca do mapa: [MapLibre GL JS](https://maplibre.org/) (BSD-3-Clause).
- Ícones: [Material Symbols](https://fonts.google.com/icons) (Apache 2.0).
- Fontes: Fraunces e Manrope (SIL Open Font License), via Google Fonts.

## Aviso

O HelpCalouro é um projeto independente, feito por estudante para a comunidade, e **não é uma página oficial da Universidade Federal da Bahia**. Não tem vínculo institucional com a UFBA nem fala em nome dela.

Conteúdo conferido em novembro de 2026 em páginas oficiais (ufba.br, UFBA SIM, SUPAC, PROAE, Carta de Serviços e REGPG). Prazos, valores, rotas e contatos mudam: em caso de divergência, valem sempre os canais oficiais da UFBA.

## Autoria

Desenvolvido por **Eduarda Almeida** ([@adaah](https://github.com/adaah)). Sugestões e correções são bem-vindas pelas *issues* do repositório.
