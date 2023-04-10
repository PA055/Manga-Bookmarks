var CACHE_NAME = 'offline-cache';
var urlsToCache = [
    '/',
    '/new',
    '/static/js/main.js',
    '/static/css/main.css',
    '/static/img/searchicon.png',
];

self.addEventListener('install', function(event) {
    event.waitUntil(
      caches.open(CACHE_NAME)
        .then(function(cache) {
          console.log('Opened cache');
          return cache.addAll(urlsToCache);
        })
    );
  });

self.addEventListener('fetch', function(event) {
    console.log('I am a request with url:', event.request.clone().url)
    event.respondWith(caches.match(event.request).then(function(response) {
        try {
            return fetch(event.request);
        } catch (err) {
            if (response) {
                return response;
            } else {
                window.location.href = '/offline';
            }
        }
    }));
});
