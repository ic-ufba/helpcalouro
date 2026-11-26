#!/usr/bin/env python3
"""Gera o index.html do HelpCalouro a partir de src/.
Uso (na raiz do repositório):  npm install  &&  python3 src/build.py"""
import re,json,os
SRC=os.path.dirname(os.path.abspath(__file__))
ROOT=os.path.dirname(SRC)
NM=os.path.join(ROOT,'node_modules')
D=os.path.join(NM,'@material-symbols','svg-400','rounded')+os.sep
h=open(os.path.join(SRC,'base.html'),encoding='utf-8').read()
def rep(a,b,n=1):
    global h
    assert a in h,('MISSING',a[:80]); h=h.replace(a,b,n)

# ---------- 1. ICONS -> Material Symbols ----------
MAP={'abc':'abc','alert':'warning','arrow':'arrow_forward','ball':'sports_soccer','bell':'notifications','book':'menu_book','bulb':'lightbulb','bus':'directions_bus','cap':'school','card':'badge','chat':'forum','check':'check_circle','doc':'description','flag':'flag','flask':'science','food':'restaurant','globe':'public','grid':'apps','hand':'volunteer_activism','health':'medical_services','heart':'favorite','home':'home','house':'home_work','lang':'translate','left':'chevron_left','lib':'local_library','map':'location_on','menu':'menu','mind':'psychology','people':'groups','phone':'call','right':'chevron_right','search':'search','star':'star','sync':'sync','cal':'calendar_month',
 'key':'key','rule':'rule','computer':'computer','movie':'movie','close':'close','expand':'keyboard_arrow_down','museum':'museum','bolt':'bolt','help':'help','event':'event','info':'info','idcard':'id_card','video':'video_call','user':'manage_accounts','stories':'auto_stories','gavel':'gavel','lock':'lock','books':'library_books','pin':'pin_drop','route':'directions','myloc':'my_location','apt':'apartment','theater':'theater_comedy','door':'door_front'}
syms=[]
for k,n in MAP.items():
    s=open(D+n+'.svg',encoding='utf-8').read()
    vb=re.search(r'viewBox="([^"]+)"',s).group(1);inner=re.search(r'<svg[^>]*>(.*)</svg>',s,re.S).group(1)
    syms.append(f'<symbol id="i-{k}" viewBox="{vb}">{inner}</symbol>')
# remove old i-* symbols
h=re.sub(r'<symbol id="i-[a-z]+"[^>]*>.*?</symbol>\s*','',h,flags=re.S)
rep('</defs></svg>',''.join(syms)+'</defs></svg>')
# inline style stroke colors -> color
h=re.sub(r'style="stroke:([^";]+)"',r'style="color:\1"',h)
h=h.replace('<svg style="stroke:${','<svg style="color:${')
# CSS: within rules whose selector mentions svg, convert stroke color -> color, drop fill:none & stroke-width
st_i=h.index('<style>')+7;st_j=h.index('</style>',st_i)
css=h[st_i:st_j]
def fixrule(m):
    sel,body=m.group(1),m.group(2)
    if 'svg' in sel and 'ramo' not in sel and 'ring' not in sel:
        body=re.sub(r'(?<![-\w])stroke:\s*([^;}]+)',r'color:\1',body)
        body=re.sub(r'fill:\s*none;?','',body)
        body=re.sub(r'stroke-(width|linecap|linejoin):[^;}]+;?','',body)
    return sel+'{'+body+'}'
css=re.sub(r'([^{}]+)\{([^{}]*)\}',fixrule,css)
h=h[:st_i]+css+h[st_j:]
ICSS='svg:not(.ramo):not(.halframo){fill:currentColor}'

# ---------- 2. HEADER ----------
GROUPS=[
 ('comecar','Começar',[('passos',None,'flag','Primeiros passos','Roteiro das primeiras semanas e checklist'),('passos','ps-ing','description','Matrícula de ingresso','SISCON, documentos e heteroidentificação')]),
 ('estudar','Estudar',[('sigaa',None,'key','SIGAA na prática','Login, horário 24N12, notas e documentos'),('academico',None,'rule','Regras do jogo','Aprovação, faltas, trancamento e prazos'),('cursos',None,'school','Cursos','Ache seu curso e onde buscar tudo sobre ele'),('sistemas','si-bib','local_library','Bibliotecas','Pergamum, empréstimo e ABNT'),('sistemas',None,'computer','Sistemas e e-mail','SIGAA, Moodle e e-mail @ufba.br')]),
 ('viver','Viver a UFBA',[('mapa',None,'pin_drop','Mapa dos campi','Pins, endereços e rota no seu celular'),('campus',None,'location_on','Campi e Buzufba','Unidades, endereços e o ônibus da UFBA'),('apoio',None,'volunteer_activism','Assistência (PROAE)','Auxílios, RU, moradia e creche'),('saude',None,'medical_services','Saúde','SMURB, PsiU e serviços pelo SUS')]),
 ('aproveitar','Aproveitar',[('oportunidades',None,'science','Oportunidades','Pesquisa, extensão, monitoria e intercâmbio'),('oportunidades','op-cur','translate','Cursos e idiomas','NUPEL, PROFICI, música, dança'),('oportunidades','op-cult','movie','Cultura e lazer','Cinema, teatro, galeria e museus')]),
 ('ajuda','Ajuda',[('faq',None,'forum','Dúvidas frequentes','Respostas curtas e diretas'),('glossario',None,'abc','Siglas e contatos','PMI, RF, CR… e a quem recorrer')]),
]
ICMAP={v:k for k,v in MAP.items()}
def ic(name): return f'<svg class="mi"><use href="#i-{ICMAP[name]}"/></svg>'
tint=['#E8EAF6','#FDE7DE','#FDF1D6']
tcol=['var(--virtute)','#B4421A','#8A5C00']
nav=''
for gid,gl,items in GROUPS:
    links=''.join(f'<a href="#{v}" data-v="{v}"{f" data-jump=\"{j}\"" if j else ""}><i style="background:{tint[n%3]};color:{tcol[n%3]}">{ic(icn)}</i><span><b>{t}</b><small>{d}</small></span></a>' for n,(v,j,icn,t,d) in enumerate(items))
    nav+=f'<div class="ng" data-g="{gid}"><button type="button" aria-expanded="false">{gl}{ic("keyboard_arrow_down")}</button><div class="mega">{links}</div></div>'
HDR=f'''<header class="hx" id="topo"><div class="hx-in">
  <a class="hx-logo" href="#inicio" aria-label="HelpCalouro UFBA, início"><img src="CRESTURI" alt=""><b>Help<em>Calouro</em></b></a>
  <nav class="hx-nav" id="nav" aria-label="Seções do guia">{nav}</nav>
  <button class="hx-ib" id="sbtn" aria-label="Buscar no guia">{ic('search')}</button>
  <button class="hx-ib hx-mm" id="mmBtn" aria-label="Abrir menu">{ic('menu')}</button>
</div>
<div class="sov" id="sov" aria-hidden="true"><div class="sov-in"><div class="sbox">{ic('search')}<input id="q" type="search" placeholder="O que você procura?" autocomplete="off" aria-label="Buscar no guia"><button class="sov-x" id="sovx" aria-label="Fechar busca">{ic('close')}</button></div><div class="drop" id="res"></div></div></div>
</header>'''
crest=re.search(r'<span class="logo-c"><img src="([^"]+)"',h).group(1)
HDR=HDR.replace('CRESTURI',crest)
i=h.index('<header class="hdr"');j=h.index('</header>',i)+9
h=h[:i]+HDR+h[j:]

# ---------- 3. HOME ----------
ramo=re.search(r'<symbol id="ramo"[^>]*>(.*?)</symbol>',h,re.S).group(1)
i=h.index('<section class="view" id="v-inicio">');j=h.index('</section>',i)+10
old=h[i:j]
slider=old[old.index('<div class="tslider'):old.index('<div class="h-sec">',old.index('<div class="tslider'))]
wkpre=re.search(r'<p class="wk-pre">.*?</p>',old,re.S).group(0)
OPP=[('#apoio',None,'restaurant','RU a R$ 2,50','Almoço e jantar com matrícula ativa',''),
 ('#oportunidades','op-cur','translate','Idiomas','PROFICI e NUPEL, inclusive LIBRAS','Inscrições por edital'),
 ('#oportunidades','op-cult','movie','Cinema e museus','Sala de Arte, MAFRO e MAE com vantagens para a UFBA',''),
 ('#saude',None,'psychology','PsiU','Acolhimento gratuito pelo WhatsApp',''),
 ('#sistemas','si-bib','local_library','Bibliotecas','Empréstimo e orientação de ABNT',''),
 ('#campus','cp-app','directions_bus','Siga o BuzUFBA','O ônibus da UFBA em tempo real','')]
opp=''.join(f'<a href="{u}"{f" data-jump=\"{j}\"" if j else ""}><i>{ic(icn)}</i><span><b>{t}</b><small>{d}</small>{f"<em>{tg}</em>" if tg else ""}</span></a>' for u,j,icn,t,d,tg in OPP)
HOME=f'''<section class="view" id="v-inicio">
  <div class="hh lines">
    <svg class="halframo" viewBox="0 0 540 622" aria-hidden="true">{ramo}</svg>
    <div class="hh-in">
      <span class="hpill">Guia de sobrevivência · UFBA</span>
      <h1>Passou? <em>Respira.</em><br>A gente te guia.</h1>
      <p>Só o que importa nas primeiras semanas, sem burocratês. Pergunte do seu jeito: a busca entende.</p>
      <div class="hs" id="hs"><div class="hs-bar">{ic('search')}<input id="hq" type="search" placeholder="O que você procura?" autocomplete="off" aria-label="Buscar no guia"><kbd>/</kbd><button type="button" id="hgo">Buscar</button></div><div class="drop" id="hres"></div></div>
      <div class="hs-pop">Mais buscados: <button data-q="trancar disciplina">trancar disciplina</button><button data-q="24N12">24N12</button><button data-q="auxílio moradia">auxílio moradia</button><button data-q="Buzufba">Buzufba</button></div>
      <p class="hnote">Projeto independente, feito por estudante para a comunidade. Não é uma página oficial da UFBA.</p>
    </div>
  </div>
  <div class="band">
    <span class="kick">Comece por aqui</span>
    <h2 class="bh">Sua primeira <em>semana</em></h2>
    <div class="wk4">
      <div class="wk"><span class="kick">Passo 1</span><h3>Entre no SIGAA</h3><p>Login e senha chegam no e-mail que você usou na inscrição.</p><a href="#sigaa" data-jump="sg-login">Como entrar {ic('arrow_forward')}</a><i>1</i></div>
      <div class="wk"><span class="kick">Passo 2</span><h3>Veja suas aulas</h3><p>Você já está matriculado(a) no 1º semestre. O horário vem em código, tipo 24N12.</p><a href="#sigaa" data-jump="sg-hor">Ler meu horário {ic('arrow_forward')}</a><i>2</i></div>
      <div class="wk"><span class="kick">Passo 3</span><h3>Saiba chegar</h3><p>O Buzufba é grátis e dá para ver em tempo real no app Siga o BuzUFBA.</p><a href="#campus" data-jump="cp-app">Rotas e app {ic('arrow_forward')}</a><i>3</i></div>
      <div class="wk"><span class="kick">Passo 4</span><h3>Garanta seu apoio</h3><p>Auxílio da PROAE sai por edital, com prazo curto. Inscreva-se já.</p><a href="#apoio">Ver auxílios {ic('arrow_forward')}</a><i>4</i></div>
    </div>
    {wkpre}
    {slider}
    <div class="opp lines">
      <div><span class="hpill">Já no 1º semestre</span><h3>O que você já pode <em>aproveitar</em></h3><p>Não precisa esperar o 2º semestre. Tudo isso já vale para calouro, e muita coisa é de graça.</p><a class="obtn" href="#oportunidades">Ver todas as oportunidades {ic('arrow_forward')}</a></div>
      <div class="ol">{opp}</div>
    </div>
  </div>
</section>'''
h=h[:i]+HOME+h[j:]

# ---------- 4. tabbar / sheet ----------
i=h.index('<nav class="tabbar"');j=h.index('</nav>',i)+6;h=h[:i]+h[j:]
sheet=''.join(f'<h5>{gl}</h5><div class="ms-row">'+''.join(f'<a href="#{v}" data-v="{v}"{f" data-jump=\"{j}\"" if j else ""}>{t}<small>{d}</small></a>' for v,j,icn,t,d in items)+'</div>' for gid,gl,items in GROUPS)
i=h.index('<div class="sheet" id="sheet"');j=h.index('</div>\n</div>',i)+len('</div>\n</div>')
h=h[:i]+f'''<div class="sheet" id="sheet" aria-hidden="true"><div class="ms-top"><a class="hx-logo" href="#inicio"><img src="{crest}" alt=""><b>Help<em>Calouro</em></b></a><button class="hx-ib on" data-close aria-label="Fechar menu">{ic('close')}</button></div><button class="ms-search" id="msq">{ic('search')}<span>O que você procura?</span></button><div id="gridm">{sheet}</div></div>'''+h[j:]

# ---------- 5. JS ----------
s_i=h.rindex('<script>');js=h[s_i:]
js=js.replace("document.querySelectorAll('#nav a[data-v]').forEach(a=>a.classList.toggle('on',a.dataset.v==v));",
 "document.querySelectorAll('#nav .ng').forEach(g=>g.classList.toggle('cur',!!g.querySelector('a[data-v=\"'+v+'\"]')));document.querySelectorAll('#nav a[data-v],#gridm a[data-v]').forEach(a=>a.classList.toggle('on',a.dataset.v==v));document.body.classList.toggle('home',v=='inicio');")
js=js.replace("$('#mmBtn').classList.toggle('on',!['inicio','passos','sistemas','apoio'].includes(v));","")
js=re.sub(r"\$\('#gridm'\)\.innerHTML=VIEWS\.map\([^\n]*\n","\n",js)
js=js.replace("sheet.addEventListener('click',e=>{if(e.target.dataset.close!==undefined||e.target.closest('.gridm a'))closeSheet()});",
 "sheet.addEventListener('click',e=>{if(e.target.closest('[data-close]')||e.target.closest('#gridm a'))closeSheet()});")
assert "#gridm a'))closeSheet" in js
js=js.replace("function openSheet(){sheet.classList.add('show');","function openSheet(){document.body.classList.add('lock');sheet.classList.add('show');")
js=js.replace("function closeSheet(){sheet.classList.remove('show');","function closeSheet(){document.body.classList.remove('lock');sheet.classList.remove('show');")
# remove old search block & sbar block
a=js.index("$('#q').addEventListener('input'");b=js.index('\n',js.index("document.addEventListener('click',e=>{if(!e.target.closest(",a))+1
js=js[:a]+js[b:]
a=js.index("const sbar=$('#sbar')") if "const sbar=$('#sbar')" in js else js.index("sbar=$('#sbar')")
a=js.rfind('\n',0,a)+1
b=js.index("addEventListener('hashchange',()=>{if(location.hash!='#menu')closeSearch()});")+len("addEventListener('hashchange',()=>{if(location.hash!='#menu')closeSearch()});")
js=js[:a]+js[b:]
GL={}
for gid,gl,items in GROUPS:
    for v,*_ in items: GL.setdefault(v,gl)
GL['inicio']='Início'
NEWJS=r'''
/* ===== v9: busca inteligente ===== */
const GROUPL=__GL__;
const SYN=[[/\b(bandej(ao|ão)|rango|almo[cç]o|janta[r]?|comida|refei[cç][aã]o)\b/,'ru restaurante','Restaurante Universitário (RU)'],
 [/\b(busu|onibus|ônibus|circular|buzu)\b/,'buzufba','Buzufba'],
 [/\b(grana|dinheiro|bolsa|ajuda financeira|benef[ií]cio)\b/,'auxilio','Auxílios da PROAE'],
 [/\btranca(r|mento)?\b/,'trancamento',''],
 [/\b(faltas?|faltar|presen[cç]a)\b/,'frequencia','Frequência (75%)'],
 [/\b(senha|login|logar|acesso)\b/,'sigaa login central autenticacao','Login no SIGAA e na rede UFBA'],
 [/\b(e-?books?|livros? digita(l|is)|springer|ebsco|lectio|vlex)\b/,'bibliotecas digitais ebook','Bibliotecas digitais'],
 [/\b(sisau|sius|autentica[cç][aã]o)\b/,'central autenticacao','Central de Autenticação'],
 [/\b(placas?|carro|moto|estacionamento|ve[ií]culo)\b/,'registro placas','Registro de Placas'],
 [/\b(processo|protocolo|sipac)\b/,'sipac processo','SIPAC (processos)'],
 [/\b(psic[oó]log[oa]|ansiedade|terapia|triste|sozinh[oa]|saudade)\b/,'psiu saude mental','Saúde mental e PsiU'],
 [/\b(m[eé]dico|consulta|doente)\b/,'smurb','SMURB (serviço médico)'],
 [/\b(livros?|emprestimo|empréstimo)\b/,'biblioteca','Bibliotecas'],
 [/\b(horario|horário|grade)\b/,'horario 24n12',''],
 [/\b(ingl[eê]s|espanhol|franc[eê]s|idioma|l[ií]ngua)\b/,'idiomas','Cursos de idiomas'],
 [/\b(dentista|dente)\b/,'odontologia','Odontologia pelo SUS'],
 [/\b(casa|moradia|morar|aluguel|resid[eê]ncia)\b/,'moradia','Moradia estudantil'],
 [/\b(cinema|teatro|show|museu|lazer)\b/,'cultura','Cultura e lazer'],
 [/\b(email|e-mail|gmail)\b/,'google gmail','Conta Google UFBA'],
 [/\b(wifi|wi-fi|internet|rede)\b/,'eduroam wi-fi','Wi-Fi eduroam'],
 [/\b(office|word|excel|powerpoint)\b/,'microsoft 365','Microsoft 365'],
 [/\b(artigo|periodico|periódico|revista)\b/,'periodicos capes','Periódicos CAPES'],
 [/\b(seguran[cç]a|assalto|roubo)\b/,'seguranca coseg','Segurança no campus'],
 [/\b(mapa|onde fica|como chego|como chegar|rota|gps|localiza[cç][aã]o|pr[eé]dio)\b/,'mapa onde fica','Mapa dos campi']];
function searchIn(raw){let q=norm(raw.trim()),label='';if(q.length<2)return null;
 for(const [re,add,l] of SYN){if(re.test(q)){q=q+' '+add;if(l&&!label)label=l}}
 const words=[...new Set(q.split(/\s+/).filter(w=>w.length>1))].map(w=>w.length>5?w.slice(0,Math.max(5,w.length-3)):w);
 const has=(t,w)=>w.length<=3?new RegExp('(^|[^a-z0-9])'+w.replace(/[.*+?^${}()|[\]\\]/g,'')+'($|[^a-z0-9])').test(t):t.includes(w);const sc=IDX.map(x=>{const T=norm(x.t),D=norm(x.d.replace(/<[^>]+>/g,' '));let s=0;for(const w of words){if(has(T,w))s+=3;else if(has(D,w))s+=1}return s?{...x,s}:null}).filter(Boolean).sort((a,b)=>b.s-a.s);
 const best=sc.length?sc[0].s:0;const hits=sc.filter(x=>x.s>=Math.max(1,best*0.34)).slice(0,8);return {label,hits}}
function renderDrop(raw,box){const r=searchIn(raw);if(!r){box.classList.remove('show');return}
 const faq=r.hits.filter(x=>x.v=='faq').slice(0,2),pag=r.hits.filter(x=>x.v!='faq').slice(0,5);
 const row=(x,icn)=>`<a href="#${x.v}" ${x.j?`data-jump="${x.j}"`:''}><i>${'<svg><use href="#i-'+icn+'"/></svg>'}</i><span><b>${esc(x.t)}</b><small>${esc(x.d.replace(/<[^>]+>/g,'').slice(0,80))}${x.d.length>80?'…':''}</small></span><em>${x.v=='faq'?'Dúvida':x.v.startsWith('mapa/')?'No mapa':(GROUPL[x.v]||'')}</em></a>`;
 box.innerHTML=(r.label?`<p class="syn">Mostrando resultados para <b>${r.label}</b></p>`:'')+
  (faq.length?`<h6>Respostas rápidas</h6>${faq.map(x=>row(x,'help')).join('')}`:'')+
  (pag.length?`<h6>Páginas</h6>${pag.map(x=>row(x,'arrow')).join('')}`:'')+
  (!faq.length&&!pag.length?'<p class="none">Nada encontrado. Tente “matrícula”, “RU”, “trancar”, “horário”…</p>':'');
 box.classList.add('show')}
const sov=$('#sov'),q=$('#q'),res=$('#res'),hq=$('#hq'),hres=$('#hres');
function openSearch(v){closeSheet();sov.classList.add('show');document.body.classList.add('lock');if(v!=null){q.value=v;renderDrop(v,res)}setTimeout(()=>q.focus(),40)}
function closeSearch(){sov.classList.remove('show');document.body.classList.remove('lock');res.classList.remove('show');hres.classList.remove('show')}
q.addEventListener('input',()=>renderDrop(q.value,res));
hq.addEventListener('input',()=>renderDrop(hq.value,hres));
hq.addEventListener('keydown',e=>{if(e.key=='Enter'){const a=hres.querySelector('a');if(a)a.click()}});
q.addEventListener('keydown',e=>{if(e.key=='Enter'){const a=res.querySelector('a');if(a)a.click()}});
$('#hgo').onclick=()=>{if(hq.value.trim().length<2){hq.focus();return}renderDrop(hq.value,hres);const a=hres.querySelector('a');if(a)a.click()};
document.querySelectorAll('[data-q]').forEach(b=>b.onclick=()=>{hq.value=b.dataset.q;renderDrop(hq.value,hres);hq.focus()});
$('#sbtn').onclick=()=>openSearch();$('#sovx').onclick=closeSearch;$('#msq').onclick=()=>openSearch();
sov.addEventListener('click',e=>{if(e.target==sov)closeSearch()});
[res,hres].forEach(b=>b.addEventListener('click',e=>{if(e.target.closest('a'))setTimeout(()=>{closeSearch();hq.value='';q.value=''},0)}));
document.addEventListener('click',e=>{if(!e.target.closest('#hs'))hres.classList.remove('show');if(!e.target.closest('.ng'))document.querySelectorAll('.ng').forEach(g=>{g.classList.remove('open');g.querySelector('button').setAttribute('aria-expanded','false')})});
document.addEventListener('keydown',e=>{if(e.key=='Escape'){closeSearch();closeSheet()}if(e.key=='/'&&!/input|textarea/i.test(document.activeElement.tagName)){e.preventDefault();if(document.body.classList.contains('home')){hq.focus();scrollTo({top:0,behavior:'smooth'})}else openSearch()}});
/* menu por categorias */
document.querySelectorAll('.ng>button').forEach(b=>b.addEventListener('click',e=>{const g=b.parentElement,o=!g.classList.contains('open');document.querySelectorAll('.ng').forEach(x=>{x.classList.remove('open');x.querySelector('button').setAttribute('aria-expanded','false')});if(o){g.classList.add('open');b.setAttribute('aria-expanded','true')}}));
document.querySelectorAll('.mega a').forEach(a=>a.addEventListener('click',()=>document.querySelectorAll('.ng').forEach(x=>x.classList.remove('open'))));
'''.replace('__GL__',json.dumps(GL,ensure_ascii=False))
js=js.replace('</script>',NEWJS+'\n</script>',1)
js=js.replace("$('#mmBtn').addEventListener('click',e=>{e.preventDefault();openSheet()});","$('#mmBtn').addEventListener('click',e=>{e.preventDefault();closeSearch&&0;openSheet()});")
h=h[:s_i]+js

# ---------- 6. CSS ----------
NEWCSS=open(os.path.join(SRC,'styles.css'),encoding='utf-8').read()
h=h.replace('</style>',ICSS+NEWCSS+'</style>',1)
ML=os.path.join(NM,'maplibre-gl','dist')+os.sep
mljs=open(ML+'maplibre-gl.js',encoding='utf-8').read().replace('</script','<\\/script')
mlcss=open(ML+'maplibre-gl.css',encoding='utf-8').read()
h=h.replace('</body>','<script type="text/plain" id="mljs">'+mljs+'</script><script type="text/plain" id="mlcss">'+mlcss+'</script><script>'+open(os.path.join(SRC,'map.js'),encoding='utf-8').read()+'</script></body>',1)
# ---------- 8. <head>: SEO, prévia de link, app instalável ----------
HEAD=open(os.path.join(SRC,'head.html'),encoding='utf-8').read()
h=re.sub(r'<meta name="theme-color"[^>]*>\s*','',h,count=1)
h=re.sub(r'<meta name="description"[^>]*>\s*','',h,count=1)
h=h.replace('</head>',HEAD+'</head>',1)
SW='<script>if("serviceWorker"in navigator&&location.protocol=="https:")addEventListener("load",()=>navigator.serviceWorker.register("sw.js").catch(()=>{}))</script>'
h=h.replace('</body>',SW+'</body>',1)
OUT=os.path.join(ROOT,'index.html')
open(OUT,'w',encoding='utf-8').write(h)
print('ok',OUT,round(len(h.encode())/1024),'KB')
