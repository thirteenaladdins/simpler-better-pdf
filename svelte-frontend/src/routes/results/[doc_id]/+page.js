import { getBaseUrl } from '../../../utils/config';

export async function load({ fetch, params }) {
	const baseUrl = getBaseUrl();
	const { doc_id } = params;
	console.log('doc_id:', doc_id);
	const response = await fetch(`${baseUrl}/api/document/${doc_id}`);
	if (!response.ok) {
		throw new Error(`Failed to fetch document: ${response.statusText}`);
	}
	// Get the PDF as a Blob
	const docBlob = await response.blob();
	return { docBlob };
}
