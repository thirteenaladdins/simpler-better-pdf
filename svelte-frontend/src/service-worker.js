// service-worker.js
self.addEventListener('storage', event => {
    if (event.key === 'theme') {
        let newCacheName;

        switch (event.newValue) {
            case 'Dark':
                newCacheName = 'myCacheDark';
                break;
            case 'Light':
                newCacheName = 'myCacheLight';
                break;
            case 'Serpent':
                newCacheName = 'myCacheSerpent';
                break;
            default:
                console.error('Unknown theme:', event.newValue);
                return;
        }

        // Update cache logic here using newCacheName...
    }
});
