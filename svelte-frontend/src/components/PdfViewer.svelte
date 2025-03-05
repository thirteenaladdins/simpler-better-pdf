<!-- PdfViewer.svelte -->
<script>
	import { onMount, createEventDispatcher } from 'svelte';
	import * as pdfjsLib from 'pdfjs-dist'; // or your chosen pdf.js build

	export let pdfFile; // The PDF to display
	export let updatedPdfBytes; // For two-way binding or saving

	let pdfDoc = null;
	let pages = [];
	const dispatch = createEventDispatcher();

	onMount(async () => {
		if (pdfFile) {
			pdfDoc = await pdfjsLib.getDocument(pdfFile).promise;
			for (let i = 1; i <= pdfDoc.numPages; i++) {
				const page = await pdfDoc.getPage(i);
				pages.push(page);
			}
		}
	});

	// Example: function to embed an image overlay
	function addImageOverlay(imgSrc, x, y) {
		// Keep track of overlays in a store or local array
		// For actual PDF editing, you'll eventually call pdf-lib
		// to insert the image. This is just a visual overlay for now.
	}
</script>

{#if pdfDoc}
	{#each pages as page, index}
		<canvas bind:this={canvasEl} on:click={(e) => handleCanvasClick(e, index)} />
		<!-- Could also place absolutely positioned elements here for overlays -->
	{/each}
{/if}

<style>
	canvas {
		border: 1px solid #999;
		margin: 1rem;
	}
</style>
