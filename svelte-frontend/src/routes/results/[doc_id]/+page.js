import { getBaseUrl } from '../../../utils/config';

export async function load({ fetch, params }) {
	const baseUrl = getBaseUrl();
	const { doc_id } = params;
	const docUrl = `${baseUrl}/api/document/${doc_id}`;

	// Optionally, fetch the PDF for an in-app preview:
	const response = await fetch(docUrl);
	if (!response.ok) {
		throw new Error(`Failed to fetch document: ${response.statusText}`);
	}
	const docBlob = await response.blob();

	// Return both the blob and the permanent URL
	return { docBlob, docUrl };
}
