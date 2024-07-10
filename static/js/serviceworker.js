self.addEventListener('install', (event) => {
    console.log('Service worker installed');
});

self.addEventListener('fetch', (event) => {
    console.log('Fetch event for ', event.request.url);
});
