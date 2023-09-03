import { loading } from '../stores/loading.js';

function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

export async function handleLoad(fetchLogic) {
    loading.set(true);

    const dataPromise = fetchLogic();
    const delayPromise = delay(2000);

    const data = await dataPromise;
    await delayPromise;

    loading.set(false);

    return data;
}
