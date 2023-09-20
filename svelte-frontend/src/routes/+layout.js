import { loading } from '../store/loadingStore.js';


function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

export async function _handleLoad(fetchLogic) {
    loading.set(true);

    const dataPromise = fetchLogic();
    const delayPromise = delay(2000);

    const data = await dataPromise;
    await delayPromise;

    loading.set(false);

    return data;
}
// Ensure we're in a browser environment
if (typeof window !== 'undefined') {
    // Check if the browser supports service workers and then register the service worker.
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', function() {
            navigator.serviceWorker.register('/service-worker.js').then(function(registration) {
                // Registration was successful
                console.log('ServiceWorker registration successful with scope: ', registration.scope);
            }, function(err) {
                // registration failed :(
                console.log('ServiceWorker registration failed: ', err);
            });
        });
    }
}
