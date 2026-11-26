/* HelpCalouro UFBA · service worker
   - Página e ícones: funcionam offline depois da primeira visita.
   - index.html: busca a versão nova primeiro (rede) e usa o cache se estiver sem internet.
   - Fontes do Google: cache após o primeiro uso.
   - Mapa de fundo (OpenFreeMap): não é guardado; precisa de internet.
   Ao publicar mudanças grandes, aumente o número de VERSAO. */
const VERSAO = 'helpcalouro-v1';
const ESSENCIAIS = ['./', 'index.html', 'manifest.webmanifest', 'favicon.ico',
  'assets/icons/icon-192.png', 'assets/icons/icon-512.png', 'assets/icons/apple-touch-icon.png'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(VERSAO).then(c => c.addAll(ESSENCIAIS)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys()
    .then(ks => Promise.all(ks.filter(k => k !== VERSAO).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  // Página: rede primeiro, cache como reserva
  if (req.mode === 'navigate') {
    e.respondWith(fetch(req).then(r => {
      const c = r.clone(); caches.open(VERSAO).then(k => k.put('index.html', c)); return r;
    }).catch(() => caches.match('index.html')));
    return;
  }
  // Arquivos do próprio site: cache primeiro
  if (url.origin === location.origin) {
    e.respondWith(caches.match(req).then(hit => hit || fetch(req).then(r => {
      if (r.ok) { const c = r.clone(); caches.open(VERSAO).then(k => k.put(req, c)); }
      return r;
    })));
    return;
  }
  // Fontes do Google: cache após o primeiro uso
  if (/fonts\.(googleapis|gstatic)\.com$/.test(url.hostname)) {
    e.respondWith(caches.match(req).then(hit => hit || fetch(req).then(r => {
      const c = r.clone(); caches.open(VERSAO).then(k => k.put(req, c)); return r;
    })));
  }
  // Demais (mapa, rotas, links externos): direto da rede
});
