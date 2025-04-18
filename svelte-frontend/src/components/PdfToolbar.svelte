<script lang="ts">
	import { onMount } from 'svelte';
	import 'pdfjs-dist/web/pdf_viewer.css';

	export let eventBus: any;
	export let viewer: any;
	export let isVisible = true;

	let currentPage = 1;
	let totalPages = 0;

	onMount(() => {
		if (viewer) {
			window.viewer = viewer;
			console.log('Exposed viewer globally:', viewer);
		}
	});

	$: if (eventBus && viewer) {
		setupEventListeners();
	}

	function setupEventListeners() {
		eventBus.on('pagechanging', (evt: any) => {
			currentPage = evt.pageNumber;
		});

		eventBus.on('pagesloaded', (evt: any) => {
			totalPages = viewer.pagesCount;
		});
	}

	function previousPage() {
		if (currentPage > 1) {
			const newPage = currentPage - 1;
			viewer.currentPageNumber = newPage;
			viewer.scrollPageIntoView({
				pageNumber: newPage,
				pageSpot: { top: 0 }
			});
		}
	}

	function nextPage() {
		if (currentPage < totalPages) {
			const newPage = currentPage + 1;
			viewer.currentPageNumber = newPage;
			viewer.scrollPageIntoView({
				pageNumber: newPage,
				pageSpot: { top: 0 }
			});
		}
	}

	function zoomIn() {
		const currentScale = viewer.currentScale;
		viewer.currentScale = currentScale + 0.1;
	}

	function zoomOut() {
		const currentScale = viewer.currentScale;
		if (currentScale > 0.1) {
			viewer.currentScale = currentScale - 0.1;
		}
	}

	function rotateClockwise() {
		viewer.pagesRotation = (viewer.pagesRotation + 90) % 360;
	}

	function rotateCounterClockwise() {
		viewer.pagesRotation = (viewer.pagesRotation - 90) % 360;
	}

	$: isFirstPage = currentPage === 1;
	$: isLastPage = currentPage === totalPages;
</script>

<div class="toolbar-container" class:hidden={!isVisible}>
	<div class="toolbar">
		<div class="toolbar-content">
			<div class="toolbar-group">
				<button
					class="toolbarButton"
					title="Previous Page"
					on:click={previousPage}
					disabled={isFirstPage}
					aria-label="Previous Page"
				>
					<svg viewBox="0 0 24 24" width="20" height="20">
						<path d="M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z" />
					</svg>
				</button>
				<button
					class="toolbarButton"
					title="Next Page"
					on:click={nextPage}
					disabled={isLastPage}
					aria-label="Next Page"
				>
					<svg viewBox="0 0 24 24" width="20" height="20">
						<path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z" />
					</svg>
				</button>
			</div>

			<div class="toolbar-separator"></div>

			<div class="toolbar-group">
				<button class="toolbarButton" title="Zoom Out" on:click={zoomOut} aria-label="Zoom Out">
					<svg viewBox="0 0 24 24" width="20" height="20">
						<path d="M19 13H5v-2h14v2z" />
					</svg>
				</button>
				<button class="toolbarButton" title="Zoom In" on:click={zoomIn} aria-label="Zoom In">
					<svg viewBox="0 0 24 24" width="20" height="20">
						<path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z" />
					</svg>
				</button>
			</div>

			<div class="toolbar-separator"></div>

			<div class="toolbar-group">
				<button
					class="toolbarButton"
					title="Rotate Counterclockwise"
					on:click={rotateCounterClockwise}
					aria-label="Rotate Counterclockwise"
				>
					<svg viewBox="0 0 24 24" width="20" height="20">
						<path
							d="M16.53 2.51C19.8 4.07 22.14 7.24 22.5 11H24c-.51-6.16-5.66-11-11.95-11-.23 0-.44.02-.66.04L15.2 3.85l1.33-1.34zM11.95 24c.23 0 .44-.02.66-.04l-3.81-3.81-1.33 1.33C4.2 19.93 1.86 16.76 1.5 13H0c.51 6.16 5.66 11 11.95 11zM8 10H6V4c0-1.11.9-2 2-2h6v2h-6v6zm8 2h-2v8c0 1.1-.9 2-2 2H6v-2h6v-8h2z"
						/>
					</svg>
				</button>
				<button
					class="toolbarButton"
					title="Rotate Clockwise"
					on:click={rotateClockwise}
					aria-label="Rotate Clockwise"
				>
					<svg viewBox="0 0 24 24" width="20" height="20">
						<path
							d="M7.47 21.49C4.2 19.93 1.86 16.76 1.5 13H0c.51 6.16 5.66 11 11.95 11 .23 0 .44-.02.66-.03L8.8 20.15l-1.33 1.34zM12.05 0c-.23 0-.44.02-.66.04l3.81 3.81 1.33-1.33C19.8 4.07 22.14 7.24 22.5 11H24c-.51-6.16-5.66-11-11.95-11zM16 14h2V8c0-1.11-.9-2-2-2h-6v2h6v6zm-8 2V4H6v2H4v2h2v8c0 1.1.89 2 2 2h8v2h2v-2h2v-2H8z"
						/>
					</svg>
				</button>
			</div>

			<div class="toolbar-separator"></div>

			<div class="toolbar-group page-number">
				<span class="toolbarLabel"
					>Page <span class="current-page">{currentPage}</span> of
					<span class="total-pages">{totalPages}</span></span
				>
			</div>
		</div>
	</div>
</div>

<style>
	.toolbar-container {
		position: fixed;
		top: 0;
		left: 0;
		right: 0;
		z-index: 1000;
		background: #f5f5f5;
		box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
		font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell,
			'Open Sans', 'Helvetica Neue', sans-serif;
	}

	.hidden {
		display: none;
	}

	.toolbar {
		height: 36px;
		width: 100%;
		display: flex;
		justify-content: center;
		background: #f5f5f5;
	}

	.toolbar-content {
		display: flex;
		align-items: center;
		max-width: 1200px;
		width: 100%;
		padding: 0 12px;
	}

	.toolbar-group {
		display: flex;
		align-items: center;
		gap: 2px;
	}

	.toolbar-separator {
		width: 1px;
		height: 20px;
		background-color: #d0d0d0;
		margin: 0 6px;
	}

	.toolbarButton {
		width: 28px;
		height: 28px;
		padding: 2px;
		border: none;
		background: none;
		cursor: pointer;
		display: flex;
		align-items: center;
		justify-content: center;
		border-radius: 4px;
		transition: background-color 0.2s ease;
	}

	.toolbarButton:hover:not(:disabled) {
		background-color: rgba(0, 0, 0, 0.08);
	}

	.toolbarButton:active:not(:disabled) {
		background-color: rgba(0, 0, 0, 0.12);
	}

	.toolbarButton:disabled {
		opacity: 0.5;
		cursor: not-allowed;
	}

	.toolbarButton svg {
		fill: #333;
		transition: fill 0.2s ease;
	}

	.toolbarButton:hover:not(:disabled) svg {
		fill: #000;
	}

	.toolbarButton:disabled svg {
		fill: #666;
	}

	.page-number {
		margin-left: 6px;
	}

	.toolbarLabel {
		font-size: 12px;
		color: #333;
		display: flex;
		align-items: center;
		gap: 2px;
	}

	.current-page {
		font-weight: 500;
		color: #000;
	}

	.total-pages {
		color: #666;
	}

	@media (max-width: 480px) {
		.toolbar {
			height: 40px;
		}

		.toolbar-content {
			padding: 0 8px;
		}

		.toolbarButton {
			width: 32px;
			height: 32px;
		}

		.toolbar-separator {
			margin: 0 4px;
		}

		.page-number {
			display: none;
		}
	}
</style>
