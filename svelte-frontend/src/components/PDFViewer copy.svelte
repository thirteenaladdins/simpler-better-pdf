<script>
	import { onMount } from 'svelte';
	import * as pdfjsLib from 'pdfjs-dist/build/pdf';
	import pdfWorkerUrl from 'pdfjs-dist/build/pdf.worker.min.js?url';

	// Set the worker URL for PDF.js
	pdfjsLib.GlobalWorkerOptions.workerSrc = pdfWorkerUrl;

	export let pdfBlob; // Expect a Blob containing the PDF data
	export let targetWidth = 600; // desired display width in pixels

	let canvas;

	onMount(async () => {
		if (!pdfBlob) return;

		// Convert Blob to ArrayBuffer
		const arrayBuffer = await pdfBlob.arrayBuffer();

		// Load the PDF from the ArrayBuffer
		const loadingTask = pdfjsLib.getDocument({ data: arrayBuffer });
		const pdf = await loadingTask.promise;

		// Get the first page of the PDF
		const page = await pdf.getPage(1);

		// Get the original page dimensions (scale 1)
		const origViewport = page.getViewport({ scale: 1 });
		const dpr = window.devicePixelRatio || 1;
		// Compute a scale factor so that the displayed width is targetWidth
		const computedScale = (targetWidth * dpr) / origViewport.width;
		const viewport = page.getViewport({ scale: computedScale });

		// Set the internal canvas resolution to the high-res dimensions
		canvas.width = viewport.width;
		canvas.height = viewport.height;
		// Set the CSS display size to the target width (height adjusts proportionally)
		canvas.style.width = `${targetWidth}px`;
		canvas.style.height = `${viewport.height / dpr}px`;

		const context = canvas.getContext('2d');

		// Render the PDF page onto the canvas using the computed viewport
		const renderContext = {
			canvasContext: context,
			viewport: viewport
		};
		await page.render(renderContext).promise;
	});
</script>

<canvas bind:this={canvas} />
