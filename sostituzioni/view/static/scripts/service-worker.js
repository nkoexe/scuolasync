const CACHE_NAME = 'scuolasync_offline_v2.11';
const OFFLINE_URL = '/offline';

// Install event handler (caches the offline page)
self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.add(OFFLINE_URL))
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.add(OFFLINE_URL))
  );
});


self.addEventListener("push", (event) => {
  const data = event.data.json();

  const title = data.title;
  const options = {
    body: data.body,
    tag: title.replace(/ /g, "_"),
    icon: "static/icons/android-chrome-192x192.png",
    data: {
      url: data.url || "/"
    }
  };

  event.waitUntil(
    self.registration.showNotification(title, options)
  );
})

self.addEventListener("notificationclick", (event) => {
  event.notification.close();

  const url = event.notification.data.url;

  const promiseChain = clients.matchAll({
    type: 'window',
    includeUncontrolled: true
  })
    .then((windowClients) => {
      const matchingClient = windowClients.find(
        (client) => client.url.includes(url) && 'focus' in client
      );

      if (matchingClient) {
        return matchingClient.focus();
      } else {
        return clients.openWindow(url);
      }
    });

  event.waitUntil(promiseChain);
});

// Fetch event handler (checks for network, falls back to cache)
self.addEventListener("fetch", (event) => {
  event.respondWith(
    (async () => {
      try {
        const preloadResponse = await event.preloadResponse;
        if (preloadResponse) {
          return preloadResponse;
        }
        const networkResponse = await fetch(event.request);
        return networkResponse;
      } catch (error) {
        const cache = await caches.open(CACHE_NAME);
        const cachedResponse = await cache.match(OFFLINE_URL);
        return cachedResponse;
      }
    })()
  );
});
