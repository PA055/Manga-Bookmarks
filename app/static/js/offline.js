var CACHE_NAME = 'offline-cache';
var urlsToCache = [
    '/offline',
    '/static/css/main.css',
    '/static/js/main.js',
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
        if (response) {
            return response;
        }
        try {
            return fetch(event.request);
        } catch (err) {
            window.location.href = '/offline'
        }
    }));
});
