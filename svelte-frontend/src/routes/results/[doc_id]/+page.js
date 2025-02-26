// +page.js

// add baseUrls from utils.config

import { getBaseUrl } from '../../../utils/config';

export async function load({ fetch, params }) {
	const baseUrl = getBaseUrl();

	const { doc_id } = params;
	console.log('doc_id:', doc_id);
	const response = await fetch(`${baseUrl}/api/document/${doc_id}`);
	if (!response.ok) {
		throw new Error(`Failed to fetch document: ${response.statusText}`);
	}
	const documentData = await response.json();
	// Return the document data so it becomes available as the `data` prop in +page.svelte.
	return { doc: documentData };
}
