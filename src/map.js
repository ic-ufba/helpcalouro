(function(){
const V=document.getElementById('v-mapa');if(!V)return;
const $m=s=>V.querySelector(s);
const nrm=s=>s.normalize('NFD').replace(/[̀-ͯ]/g,'').toLowerCase();
const isApple=/iPhone|iPad|iPod|Macintosh/.test(navigator.userAgent);
const byId=Object.fromEntries(MP.map(p=>[p[0],p]));
let map=null,mk={},cur=null,camp='all',cat='',me=null,meMk=null,tried=false,noteShown=false;
const ll=p=>p[5]+','+p[6];
const routeUrl=p=>isApple?`https://maps.apple.com/?daddr=${ll(p)}&dirflg=w&q=${encodeURIComponent(p[4])}`:`https://www.google.com/maps/dir/?api=1&destination=${ll(p)}`;
const gUrl=p=>`https://www.google.com/maps/search/?api=1&query=${ll(p)}`;
const wUrl=p=>`https://waze.com/ul?ll=${ll(p)}&navigate=yes`;
function dist(p){if(!me)return null;const R=6371e3,r=Math.PI/180,a=(p[5]-me[0])*r,b=(p[6]-me[1])*r,h=Math.sin(a/2)**2+Math.cos(me[0]*r)*Math.cos(p[5]*r)*Math.sin(b/2)**2;return 2*R*Math.asin(Math.sqrt(h))}
const fmtD=d=>d==null?'':d<1000?Math.round(d/10)*10+' m':(d/1000).toFixed(1).replace('.',',')+' km';
const badge=(p,cls='')=>{const c=MCATS[p[2]];return `<span class="mbadge ${cls}" style="--b:${c.bg};--f:${c.fg}">${p[1]}</span>`};

const inC=p=>camp=='all'||p[3]==camp;
function tabs(){$m('#mtabs').innerHTML=[['all','Todos'],...Object.entries(MCAMP)].map(([k,l])=>`<button data-c="${k}" class="${k==camp&&!$m('#mq').value?'on':''}">${l}<small>${k=='all'?MP.length:MP.filter(p=>p[3]==k).length}</small></button>`).join('')}
function legend(){const ps=MP.filter(p=>inC(p)&&!p[10]);const seen=new Set(),sig=ps.filter(p=>{const k=p[1]+p[2];if(seen.has(k)||p[2]=='chegar')return false;seen.add(k);return true});
 $m('#mlegc').innerHTML=`<div class="ml-cats">${Object.values(MCATS).map(c=>`<span><i style="background:${c.bg};border-color:${c.bg=='#fff'||c.bg=='#F7F4EC'?c.fg:c.bg}"></i>${c.l}</span>`).join('')}<span><i class="dash"></i>Local aproximado</span><span><b class="mbadge sm" style="--b:#D8C59B;--f:#12173F">Bib</b>Biblioteca dentro do prédio</span></div><h6>Siglas${camp=='all'?'':' · '+MCAMP[camp]}</h6><div class="ml-sig">${sig.map(p=>`<button data-go="${p[0]}">${badge(p,'sm')}<span>${p[4]}</span></button>`).join('')}</div>`;
 $m('#mlegc').querySelectorAll('[data-go]').forEach(b=>b.onclick=()=>{sel(b.dataset.go);if(innerWidth<900)$m('.mbox').scrollIntoView({behavior:'smooth',block:'start'})})}
function cats(){const used=[...new Set(MP.filter(inC).map(p=>p[2]))];$m('#mcats').innerHTML=`<button data-k="" class="${!cat?'on':''}">Tudo</button>`+Object.entries(MCATS).filter(([k])=>used.includes(k)||k==cat).map(([k,c])=>`<button data-k="${k}" class="${k==cat?'on':''}"><i style="background:${c.bg};border-color:${c.bg=='#fff'||c.bg=='#F7F4EC'?c.fg:c.bg}"></i>${c.l}</button>`).join('')}
function list(){
 const q=nrm($m('#mq').value.trim());
 let r=MP.filter(p=>(!cat||p[2]==cat)&&(q?nrm(p[1]+' '+p[4]+' '+p[7]+' '+p[8]+' '+MCATS[p[2]].l+' '+MCAMP[p[3]]).includes(q):inC(p)));
 if(me)r=r.slice().sort((a,b)=>dist(a)-dist(b));
 const grp=camp=='all'&&!q&&!me;let last='';
 $m('#mlist').innerHTML=r.length?r.map(p=>`${grp&&p[3]!=last?`<h6 class="mgrp">${MCAMP[last=p[3]]}</h6>`:''}<button class="mrow${p[0]==cur?' on':''}" data-id="${p[0]}">${badge(p)}<span><b>${p[4]}</b><small>${q||(camp=='all'&&me)?MCAMP[p[3]]+' · ':''}${p[7]}${me?' · <em>'+fmtD(dist(p))+'</em>':''}</small></span><svg><use href="#i-right"/></svg></button>`).join(''):'<p class="ud-none">Nada encontrado. Tente outro nome, como “RU”, “Poli” ou “biblioteca”.</p>';
 $m('#mlbtn').innerHTML=`<svg><use href="#i-menu"/></svg>${V.classList.contains('lopen')?'Esconder lista':'Ver lista de locais'} <small>${r.length}</small>`;
 if(map)Object.entries(mk).forEach(([id,m])=>{const p=byId[id];m.getElement().style.display=(!cat||p[2]==cat)?'':'none'});
}
function card(p){
 const c=MCATS[p[2]],d=dist(p),el=$m('#mcard');
 el.innerHTML=`<button class="mx" aria-label="Fechar"><svg><use href="#i-close"/></svg></button><div class="mc-h">${badge(p,'lg')}<div><small>${MCAMP[p[3]]} · ${c.l}${d!=null?' · a '+fmtD(d)+' de você':''}</small><h3>${p[4]}</h3></div></div><p class="mc-a"><svg><use href="#i-map"/></svg>${p[7]}</p>${(()=>{const hh=p[10]?[byId[p[10]]]:MP.filter(x=>x[10]==p[0]);return hh.length?`<p class="mc-also">${p[10]?'Fica em':'Também aqui'}: ${hh.map(x=>`<button data-go="${x[0]}">${x[4]}</button>`).join(' · ')}</p>`:''})()}${p[8]?`<p class="mc-t${p[9]?' ap':''}">${p[9]?'<svg><use href="#i-alert"/></svg>':''}${p[8]}</p>`:''}<a class="mgo" href="${routeUrl(p)}" target="_blank" rel="noopener"><svg><use href="#i-route"/></svg>Como chegar</a><button class="mmore" aria-expanded="false">Outras opções<svg><use href="#i-expand"/></svg></button><div class="mc-l" hidden><a href="${gUrl(p)}" target="_blank" rel="noopener">Google Maps</a><a href="${wUrl(p)}" target="_blank" rel="noopener">Waze</a><button class="mcopy">Copiar endereço</button></div>`;
 el.querySelector('.mmore').onclick=e=>{const b=e.currentTarget,l=el.querySelector('.mc-l'),o=l.hidden;l.hidden=!o;b.setAttribute('aria-expanded',o)};
 el.hidden=false;
 el.querySelectorAll('[data-go]').forEach(b=>b.onclick=()=>sel(b.dataset.go));
 el.querySelector('.mx').onclick=()=>{el.hidden=true;sel(null)};
 el.querySelector('.mcopy').onclick=e=>{const t=p[4]+' · '+p[7]+' ('+ll(p)+')';(navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(()=>e.target.textContent='Copiado!').catch(()=>{e.target.textContent=ll(p)})};
}
function sel(id,fly){
 cur=id;Object.entries(mk).forEach(([k,m])=>m.getElement().classList.toggle('on',k==id));
 V.querySelectorAll('.mrow').forEach(b=>b.classList.toggle('on',b.dataset.id==id));
 if(!id){history.replaceState(null,'','#mapa');return}
 const p=byId[id];history.replaceState(null,'','#mapa/'+id);
 if(camp!='all'&&p[3]!=camp&&!$m('#mq').value){camp=p[3];tabs();cats();list();legend()}
 card(p);
 if(map&&fly!==false)map.flyTo({center:[p[6],p[5]],zoom:Math.max(map.getZoom(),17),offset:[0,innerWidth<900?-90:0],duration:700});
}
function fitCamp(k,anim){if(!map)return;const ps=MP.filter(p=>k=='all'||p[3]==k);const b=ps.reduce((b,p)=>[[Math.min(b[0][0],p[6]),Math.min(b[0][1],p[5])],[Math.max(b[1][0],p[6]),Math.max(b[1][1],p[5])]],[[180,90],[-180,-90]]);map.fitBounds(b,{padding:innerWidth<900?{top:50,bottom:60,left:30,right:30}:{top:70,bottom:70,left:70,right:70},maxZoom:17,duration:anim?700:0})}
function note(t){const n=$m('#mnote');n.innerHTML=t;n.hidden=false;clearTimeout(note.t);note.t=setTimeout(()=>n.hidden=true,9000)}
function style(){
 const F=['Noto Sans Regular'],FB=['Noto Sans Bold'],nm=['coalesce',['get','name:pt'],['get','name']];
 const mi=['in',['get','class'],['literal',['minor','service']]],ma=['in',['get','class'],['literal',['tertiary','secondary','primary','trunk','motorway']]];
 return {version:8,glyphs:'https://tiles.openfreemap.org/fonts/{fontstack}/{range}.pbf',sources:{om:{type:'vector',url:'https://tiles.openfreemap.org/planet',attribution:'<a href="https://openfreemap.org" target="_blank">OpenFreeMap</a> © <a href="https://www.openmaptiles.org/" target="_blank">OpenMapTiles</a> © <a href="https://www.openstreetmap.org/copyright" target="_blank">OpenStreetMap</a>'}},layers:[
 {id:'bg',type:'background',paint:{'background-color':'#F7F4EC'}},
 {id:'lc',type:'fill',source:'om','source-layer':'landcover',paint:{'fill-color':'#E3E8D0','fill-opacity':.75}},
 {id:'park',type:'fill',source:'om','source-layer':'park',paint:{'fill-color':'#E3E8D0'}},
 {id:'uni',type:'fill',source:'om','source-layer':'landuse',filter:['in',['get','class'],['literal',['university','college','school']]],paint:{'fill-color':'#FCEBC4','fill-opacity':.9}},
 {id:'hosp',type:'fill',source:'om','source-layer':'landuse',filter:['==',['get','class'],'hospital'],paint:{'fill-color':'#F8DED3'}},
 {id:'water',type:'fill',source:'om','source-layer':'water',paint:{'fill-color':'#B7CCF8'}},
 {id:'ww',type:'line',source:'om','source-layer':'waterway',paint:{'line-color':'#B7CCF8','line-width':1.2}},
 {id:'bld',type:'fill',source:'om','source-layer':'building',minzoom:14,paint:{'fill-color':'#ECE2C8','fill-outline-color':'#D3BF90','fill-opacity':['interpolate',['linear'],['zoom'],14,0,15.5,1]}},
 {id:'path',type:'line',source:'om','source-layer':'transportation',minzoom:15,filter:['in',['get','class'],['literal',['path','track']]],paint:{'line-color':'#C9B583','line-width':1.2,'line-dasharray':[2,1.6]}},
 {id:'mi-c',type:'line',source:'om','source-layer':'transportation',minzoom:13,filter:mi,layout:{'line-cap':'round','line-join':'round'},paint:{'line-color':'#E3D3AA','line-width':['interpolate',['exponential',1.6],['zoom'],13,1,18,13]}},
 {id:'ma-c',type:'line',source:'om','source-layer':'transportation',filter:ma,layout:{'line-cap':'round','line-join':'round'},paint:{'line-color':'#E8C46F','line-width':['interpolate',['exponential',1.6],['zoom'],10,1.2,18,22]}},
 {id:'mi',type:'line',source:'om','source-layer':'transportation',minzoom:13,filter:mi,layout:{'line-cap':'round','line-join':'round'},paint:{'line-color':'#fff','line-width':['interpolate',['exponential',1.6],['zoom'],13,.4,18,10]}},
 {id:'ma',type:'line',source:'om','source-layer':'transportation',filter:ma,layout:{'line-cap':'round','line-join':'round'},paint:{'line-color':'#FFF2CF','line-width':['interpolate',['exponential',1.6],['zoom'],10,.6,18,18]}},
 {id:'rdn',type:'symbol',source:'om','source-layer':'transportation_name',minzoom:14,layout:{'symbol-placement':'line','text-field':nm,'text-font':F,'text-size':['interpolate',['linear'],['zoom'],14,10,18,13]},paint:{'text-color':'#5F6480','text-halo-color':'#fff','text-halo-width':1.4}},
 {id:'plc',type:'symbol',source:'om','source-layer':'place',filter:['in',['get','class'],['literal',['suburb','neighbourhood','quarter']]],layout:{'text-field':nm,'text-font':FB,'text-transform':'uppercase','text-letter-spacing':.14,'text-size':['interpolate',['linear'],['zoom'],12,10,16,13]},paint:{'text-color':'#2C3382','text-opacity':.55,'text-halo-color':'#F7F4EC','text-halo-width':1.6}}
 ]};
}
function build(){
 if(!window.maplibregl){note('<b>O mapa não carregou neste navegador.</b> A lista continua funcionando, e “Como chegar” abre seu app de mapas.');return}
 try{map=new maplibregl.Map({container:$m('#mapc'),style:style(),center:[-38.5088,-13.0018],zoom:15.6,minZoom:11,maxZoom:19,maxBounds:[[-38.62,-13.06],[-38.38,-12.88]],dragRotate:false,pitchWithRotate:false,attributionControl:{compact:true}})}catch(e){map=null;note('<b>O mapa não carregou neste navegador.</b> A lista continua funcionando, e “Como chegar” abre seu app de mapas.');return}
 map.touchZoomRotate.disableRotation();
 map.addControl(new maplibregl.NavigationControl({showCompass:false}),'top-right');
 map.on('error',e=>{if(!noteShown&&e&&e.error&&/fetch|Failed|NetworkError|load/i.test(String(e.error.message||e.error))){noteShown=true;note('O fundo do mapa não carregou (conexão?). Os pins e o “Como chegar” continuam funcionando.')}});
 const zc=()=>$m('#mapc').classList.toggle('mlo',map.getZoom()<14.8);map.on('zoom',zc);zc();
 MP.forEach(p=>{const c=MCATS[p[2]],el=document.createElement('button'),hs=p[10]?byId[p[10]]:null;el.className='mpin'+(p[9]?' ap':'')+(hs?' hosted':'');el.style.cssText=`--b:${c.bg};--f:${c.fg};--e:${c.bg=='#fff'||c.bg=='#F7F4EC'?c.fg:'#fff'}`;el.innerHTML=`<span>${p[1]}</span>`;el.title=p[4];el.setAttribute('aria-label',p[4]);el.onclick=e=>{e.stopPropagation();sel(p[0])};mk[p[0]]=new maplibregl.Marker(hs?{element:el,anchor:'bottom-left',offset:[Math.round((hs[1].length*7.4+22)/2)+2,-14]}:{element:el,anchor:'bottom'}).setLngLat([p[6],p[5]]).addTo(map)});
 list();
 if(cur){const p=byId[cur];map.jumpTo({center:[p[6],p[5]],zoom:17});sel(cur,false)}else fitCamp(camp);
}
function init(){
 if(tried){if(map)map.resize();return}tried=true;
 tabs();cats();list();legend();
 if(window.maplibregl)return build();
 try{const s=document.createElement('style');s.textContent=document.getElementById('mlcss').textContent;document.head.appendChild(s);const j=document.createElement('script');j.textContent=document.getElementById('mljs').textContent;document.head.appendChild(j)}catch(e){}
 setTimeout(build,0);
}
function route(){const h=location.hash.slice(1).split('/');if(h[0]!='mapa')return;init();if(h[1]&&byId[h[1]]&&h[1]!=cur){cur=h[1];if(map)sel(cur);else{camp=byId[cur][3];tabs();cats();list();card(byId[cur])}}else if(map)setTimeout(()=>map.resize(),30)}
addEventListener('hashchange',route);setTimeout(route,0);
V.addEventListener('click',e=>{
 const t=e.target.closest('button');if(!t||!V.contains(t))return;
 if(t.dataset.c){camp=t.dataset.c;cat='';$m('#mq').value='';tabs();cats();list();legend();$m('#mcard').hidden=true;sel(null);fitCamp(camp,1)}
 else if(t.dataset.k!==undefined&&t.closest('#mcats')){cat=t.dataset.k;cats();list()}
 else if(t.classList.contains('mrow')){sel(t.dataset.id);if(innerWidth<900)$m('.mbox').scrollIntoView({behavior:'smooth',block:'start'})}
 else if(t.id=='mlbtn'){V.classList.toggle('lopen');list()}
 else if(t.id=='mloc'){
  if(!navigator.geolocation){note('Seu navegador não informa a localização.');return}
  t.classList.add('busy');
  navigator.geolocation.getCurrentPosition(pos=>{t.classList.remove('busy');me=[pos.coords.latitude,pos.coords.longitude];list();if(cur)card(byId[cur]);
   if(map){if(!meMk){const d=document.createElement('div');d.className='mme';meMk=new maplibregl.Marker({element:d}).setLngLat([me[1],me[0]]).addTo(map)}else meMk.setLngLat([me[1],me[0]]);
    const inside=me[0]>-13.06&&me[0]<-12.88&&me[1]>-38.62&&me[1]<-38.38;if(inside)map.flyTo({center:[me[1],me[0]],zoom:16.5});else note('Você parece estar fora de Salvador. A lista mostra a distância até cada local.')}
  },()=>{t.classList.remove('busy');note('Não foi possível pegar sua localização. Verifique a permissão do navegador.')},{enableHighAccuracy:true,timeout:12000})}
});
$m('#mq').addEventListener('input',()=>{if($m('#mq').value)V.classList.add('lopen');tabs();list()});
})();
