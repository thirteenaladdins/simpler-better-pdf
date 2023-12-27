// src/utils/refreshPage.js
import { goto } from '$app/navigation';

async function refreshPage() {
	await goto('/');
	location.reload();
}

export default refreshPage;
