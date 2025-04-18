<script lang="ts">
	import { onMount } from 'svelte';
	import 'pdfjs-dist/web/pdf_viewer.css';
	import PdfToolbar from './PdfToolbar.svelte';
	import { editLayerStore } from '../store/editTextStore.js';

	export let file: File | null = null;

	let containerEl: HTMLDivElement;
	let eventBus: any;
	let viewer: any;

	$: if (file && containerEl) {
		renderPdf();
	}

	$: {
		console.log('Edit layer state changed in PdfViewer:', $editLayerStore);
		if (viewer) {
			try {
				// Get the current page view safely
				const pageView = viewer._pages[viewer.currentPageNumber - 1];
				if (pageView && pageView.div) {
					// Remove any existing overlay
					const existingOverlay = pageView.div.querySelector('.customEditableOverlay');
					if (existingOverlay) existingOverlay.remove();

					// Create new overlay if edit mode is active
					if ($editLayerStore.isActive) {
						const textLayerDiv = pageView.div.querySelector('.textLayer');
						if (textLayerDiv) {
							const overlay = document.createElement('div');
							overlay.className = 'customEditableOverlay';
							overlay.style.position = 'absolute';
							overlay.style.inset = '0';
							overlay.style.zIndex = '5000';
							overlay.style.pointerEvents = 'auto';
							overlay.style.transform = getComputedStyle(textLayerDiv).transform;
							overlay.style.transformOrigin = 'top left';

							Array.from(textLayerDiv.children).forEach((originalSpan: Element) => {
								const computed = getComputedStyle(originalSpan);
								const editable = document.createElement('div');
								editable.style.whiteSpace = 'pre';
								editable.style.fontFamily = '"Courier New", Courier, monospace';

								editable.textContent = (originalSpan as HTMLElement).textContent;
								editable.setAttribute('contenteditable', 'true');
								Object.assign(editable.style, {
									position: 'absolute',
									left: computed.left,
									top: computed.top,
									width: computed.width,
									height: computed.height,
									fontSize: computed.fontSize,
									fontWeight: computed.fontWeight,
									whiteSpace: computed.whiteSpace,
									lineHeight: computed.lineHeight,
									letterSpacing: computed.letterSpacing,
									wordSpacing: computed.wordSpacing,
									transform: computed.transform,
									transformOrigin: computed.transformOrigin,
									color: 'red',
									background: 'rgba(255, 255, 255, 0.1)',
									outline: 'none',
									cursor: 'text'
								});

								editable.addEventListener('blur', () => {
									console.log('Edited:', editable.textContent);
								});

								overlay.appendChild(editable);
							});

							pageView.div.appendChild(overlay);
						}
					}
				}
			} catch (err) {
				console.error('Error updating edit layer:', err);
			}
		}
	}

	async function renderPdf() {
		try {
			const { pdfjsLib, PDFViewer, EventBus } = await import('../pdfjs-client');

			const arrayBuffer = await file!.arrayBuffer();
			const loadingTask = pdfjsLib.getDocument({ data: arrayBuffer });
			const pdf = await loadingTask.promise;

			eventBus = new EventBus();
			viewer = new PDFViewer({
				container: containerEl,
				eventBus,
				textLayerMode: 2 // Enable selectable text
			});

			viewer.setDocument(pdf);
			viewer.currentScaleValue = 'auto';

			eventBus.on('textlayerrendered', ({ pageNumber }) => {
				const pageEl = containerEl.querySelector(`.page[data-page-number="${pageNumber}"]`);
				const textLayerDiv = pageEl?.querySelector('.textLayer');

				if (!textLayerDiv || !pageEl) return;

				// Remove previous overlay if it exists
				const existingOverlay = pageEl.querySelector('.customEditableOverlay');
				if (existingOverlay) existingOverlay.remove();

				// Only create editable overlay if edit mode is active
				if ($editLayerStore.isActive) {
					// Create editable overlay
					const overlay = document.createElement('div');
					overlay.className = 'customEditableOverlay';
					overlay.style.position = 'absolute';
					overlay.style.inset = '0';
					overlay.style.zIndex = '5000';
					overlay.style.pointerEvents = 'auto';
					overlay.style.transform = getComputedStyle(textLayerDiv).transform;
					overlay.style.transformOrigin = 'top left';

					Array.from(textLayerDiv.children).forEach((originalSpan: Element) => {
						const computed = getComputedStyle(originalSpan);
						const editable = document.createElement('div');
						editable.style.whiteSpace = 'pre';
						editable.style.fontFamily = '"Courier New", Courier, monospace';

						editable.textContent = (originalSpan as HTMLElement).textContent;
						editable.setAttribute('contenteditable', 'true');
						Object.assign(editable.style, {
							position: 'absolute',
							left: computed.left,
							top: computed.top,
							width: computed.width,
							height: computed.height,
							fontSize: computed.fontSize,
							fontWeight: computed.fontWeight,
							whiteSpace: computed.whiteSpace,
							lineHeight: computed.lineHeight,
							letterSpacing: computed.letterSpacing,
							wordSpacing: computed.wordSpacing,
							transform: computed.transform,
							transformOrigin: computed.transformOrigin,
							color: 'red',
							background: 'rgba(255, 255, 255, 0.1)',
							outline: 'none',
							cursor: 'text'
						});

						editable.addEventListener('blur', () => {
							console.log('Edited:', editable.textContent);
						});

						overlay.appendChild(editable);
					});

					pageEl.appendChild(overlay);
				}
			});
		} catch (err) {
			console.error('Error initializing PDF viewer:', err);
		}
	}
</script>

<div class="viewer-container">
	{#if eventBus && viewer}
		<PdfToolbar {eventBus} {viewer} />
	{/if}
	<div bind:this={containerEl} class="pdf-wrapper">
		<div class="pdfViewer"></div>
	</div>
</div>

<style>
	.viewer-container {
		position: relative;
		width: 100%;
		height: 100%;
		overflow: auto;
	}

	.pdf-wrapper {
		position: absolute;
		top: 36px;
		left: 0;
		right: 0;
		bottom: 0;
		overflow: auto;
		background: var(--background-color, #fff);
	}

	:global(.pdfViewer) {
		position: relative;
		width: auto;
		height: auto;
		margin: 0 auto;
	}

	:global(.pdfViewer .page) {
		margin: 1px auto;
		border: 9px solid transparent;
		background-clip: content-box;
		position: relative;
	}

	:global(.textLayer span[contenteditable]) {
		vertical-align: top;
		display: inline-block;
		transform-origin: top left;
		white-space: pre;
		line-height: 1;
		user-select: text;
		/* font-smoothing: antialiased; */
	}

	/* :global(.pdfViewer .page canvas) {
		opacity: 0; 
	} */

	:global(.textLayer span[contenteditable]) {
		vertical-align: top;
		line-height: 1;
		white-space: pre;
		transform-origin: top left;
	}

	:global(.customEditableOverlay) {
		pointer-events: auto;
		position: absolute;
		inset: 0;
		transform-origin: top left;
		user-select: text;
		z-index: 5000;
	}

	:global(.customEditableOverlay div[contenteditable]) {
		pointer-events: auto;
		display: inline-block;
		white-space: pre;
		line-height: 1;
	}
</style>
