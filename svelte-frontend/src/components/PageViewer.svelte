<!-- PageViewer.svelte -->
<script>
	import { onMount } from 'svelte';
	export let pdfFile; // from parent

	let pdfDoc = null;
	let thumbnails = [];

	onMount(async () => {
		if (pdfFile) {
			pdfDoc = await pdfjsLib.getDocument(pdfFile).promise;
			const totalPages = pdfDoc.numPages;

			for (let i = 1; i <= totalPages; i++) {
				const page = await pdfDoc.getPage(i);
				// Render page at small scale to a canvas or an image data URL
				// Push thumbnail data into `thumbnails`
			}
		}
	});

	function goToPage(pageNumber) {
		// dispatch an event or use a store to signal the main PdfViewer to jump to that page
	}
</script>

{#if pdfDoc}
	{#each thumbnails as thumb, i}
		<img src={thumb} on:click={() => goToPage(i + 1)} />
	{/each}
{/if}
