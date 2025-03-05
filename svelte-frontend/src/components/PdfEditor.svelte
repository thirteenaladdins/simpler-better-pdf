<!-- PdfEditor.svelte -->
<script>
	import PageViewer from './PageViewer.svelte';
	import PdfViewer from './PdfViewer.svelte';
	import ToolsAndTemplates from './ToolsAndTemplates.svelte';

	let pdfFile; // store the loaded PDF file (File object or ArrayBuffer)
	let updatedPdfBytes; // store updated PDF bytes if needed
</script>

<div class="editor-container">
	<!-- Left Pane: Thumbnails / Page Navigation -->
	<div class="left-pane">
		<PageViewer {pdfFile} />
	</div>

	<!-- Center Pane: Main PDF Viewer -->
	<div class="center-pane">
		<PdfViewer {pdfFile} bind:updatedPdfBytes />
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
	.editor-container {
		display: flex;
		height: 100vh;
	}
	.left-pane {
		width: 200px;
		border-right: 1px solid #ccc;
		overflow-y: auto;
	}
	.center-pane {
		flex: 1;
		display: flex;
		justify-content: center;
		align-items: center;
		background: #222; /* or your theme color */
	}
	.right-pane {
		width: 300px;
		border-left: 1px solid #ccc;
		overflow-y: auto;
	}
</style>
