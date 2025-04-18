<!-- PdfEditor.svelte -->
<script>
	import { onMount } from 'svelte';
	import PageViewer from './PageViewer.svelte';
	import PdfViewer from './PdfViewer.svelte';
	import ToolsAndTemplates from './ToolsAndTemplates.svelte';
	import DropAreaFileUpload from './DropAreaFileUpload.svelte';
	import Loading from '../components/Loading.svelte';
	import { loading } from '../store/loadingStore.js';
	import { errorMessage } from '../store/errorMessageStore.js';
	import { sessionData } from '../store/sessionStore.js';
	import {
		handleDragEnter,
		handleDragLeave,
		handleDragEnd,
		handleDrop
	} from '../utils/dragAndDrop';
	import {
		setHighlight,
		increaseCounter,
		decreaseCounter,
		resetCounter
	} from '../utils/dragState.js';
	import { isHighlighted } from '../utils/dragState.js';

	let highlighted;
	let dropArea;

	isHighlighted.subscribe((value) => {
		highlighted = value;
	});

	let pdfFile; // store the loaded PDF file (File object or ArrayBuffer)
	let updatedPdfBytes = null; // store updated PDF bytes if needed

	let uploadSuccessful = false;
	let responseData = null;
	let showLoading = false;
	let startTime;
	let showPdfViewer = false;

	// Reactively track the loading state
	$: if ($loading && !showLoading) {
		showLoading = true;
		startTime = Date.now();
	}

	// Add a reactive statement to clear loading state
	$: if (!$loading && showLoading) {
		showLoading = false;
	}

	function handleUploadSuccess(event) {
		uploadSuccessful = true;
		responseData = event.detail;
		sessionData.set(responseData);
		console.log('handle success', responseData);

		// Set the PDF file for viewing
		if (responseData.pdfFile) {
			pdfFile = responseData.pdfFile;
			showPdfViewer = true;
		}

		// Ensure loading state is cleared
		loading.set(false);
		showLoading = false;
	}

	function handleUploadFailed(event) {
		let error = event.detail.message || 'An error occurred.';
		errorMessage.set(error);
		// Ensure loading state is cleared on error
		loading.set(false);
		showLoading = false;
	}

	function highlight(event) {
		event.preventDefault();
		setHighlight(true);
	}

	function handleInsertLogo(logoDetails) {
		// This function will handle logo insertion
		console.log('Logo insertion requested:', logoDetails);
		// Future implementation would modify PDF content
	}

	// Set up a dynamic viewport height custom property (--vh)
	onMount(() => {
		const setVh = () => {
			// Multiply by 0.01 to convert innerHeight to a single vh unit
			document.documentElement.style.setProperty('--vh', `${window.innerHeight * 0.01}px`);
		};
		setVh();
		window.addEventListener('resize', setVh);
		return () => window.removeEventListener('resize', setVh);
	});
</script>

<!-- Show a loading component when showLoading is true -->
{#if showLoading}
	<Loading />
{/if}

<div
	class="editor-container"
	bind:this={dropArea}
	on:dragenter={(event) => handleDragEnter(event, increaseCounter, setHighlight)}
	on:dragover={(event) => highlight(event)}
	on:dragleave={(event) => handleDragLeave(event, decreaseCounter, setHighlight)}
	on:dragend={(event) => handleDragEnd(event, resetCounter, setHighlight)}
	on:drop={(event) => handleDrop(event, resetCounter, setHighlight)}
	role="region"
>
	<!-- {isHighlighted ? 'highlighted' : ''}" -->
	<!-- Left Pane: Thumbnails / Page Navigation -->
	<div class="left-pane">
		<PageViewer {pdfFile} />
	</div>

	<!-- Center Pane: Main PDF Viewer and Upload Area -->
	<div
		class="center-pane {highlighted ? 'highlighted' : ''} {showPdfViewer
			? 'pdf-mode'
			: 'upload-mode'}"
		on:click={(event) => {
			if (!showPdfViewer && event.currentTarget === event.target) {
				// Only trigger when clicking directly on the center pane background
				// Find the file input in DropAreaFileUpload and click it
				const fileInput = document.querySelector('.center-pane input[type="file"]');
				if (fileInput) fileInput.click();
			}
		}}
		on:keydown={(e) => {
			if (!showPdfViewer && e.key === 'Enter') {
				const fileInput = document.querySelector('.center-pane input[type="file"]');
				if (fileInput) fileInput.click();
			}
		}}
		tabindex="0"
		role={showPdfViewer ? 'region' : 'button'}
	>
		{#if showPdfViewer}
			<PdfViewer file={pdfFile} />
		{:else}
			<DropAreaFileUpload
				on:uploadSuccess={handleUploadSuccess}
				on:uploadFailed={handleUploadFailed}
				{showPdfViewer}
				uploadedPdfFile={pdfFile}
			/>
		{/if}
	</div>

	<!-- Right Pane: Tools & Templates -->
	<div class="right-pane">
		<ToolsAndTemplates
			{updatedPdfBytes}
			on:insertLogo={(event) => handleInsertLogo(event.detail)}
		/>
	</div>
</div>

<style>
	/* Use the dynamically calculated --vh to fill the entire viewport */
	.editor-container {
		display: flex;
		height: calc(100vh - 40px); /* Subtract both top and bottom margins from the total height */
		width: 100vw;
		position: fixed;
		top: 20px; /* Add 20px gap at the top */
		left: 0;
		box-sizing: border-box;
		overflow: hidden;
		background-color: transparent;
		transition: background-color 0.3s ease-in-out;
	}

	.left-pane {
		width: 200px;
		overflow-y: auto;
		border-right: 1px solid var(--accent-color);
		padding-right: 10px;
		height: 100%;
	}

	.center-pane {
		flex: 1;
		display: flex;
		justify-content: center;
		align-items: center;
		border: 2px solid var(--accent-color);
		border-radius: 5px;
		margin: 0 10px;
		height: 100%;
	}

	.center-pane.upload-mode:hover {
		background-color: var(--accent-color);
		cursor: pointer;
		transition: background-color 0.3s ease-in-out;
	}

	.center-pane.pdf-mode {
		cursor: default;
		border: none;
		align-items: stretch;
		height: 100%;
		padding: 0;
		position: relative;
		overflow: hidden;
		display: flex;
		flex-direction: column;
	}

	.right-pane {
		width: 300px;
		overflow-y: auto;
		border-left: 1px solid var(--accent-color);
		padding-left: 10px;
		height: 100%;
	}

	.highlighted {
		background-color: var(--accent-color);
		transition: background-color 0.3s ease-in-out;
	}
</style>
