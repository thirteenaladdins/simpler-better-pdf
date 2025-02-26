<script>
	// Import necessary components
	import TableDataViewer from '../../../components/TableDataViewer.svelte';
	import DownloadSection from '../../../components/DownloadSection.svelte';
	import PdfViewer from '../../../components/PDFViewer copy.svelte';
	import { sessionData } from '../../../store/sessionStore';
	import ShareComponent from '../../../components/ShareComponent.svelte';

	// Export the data prop containing document details
	export let data;
	const { doc } = data;

	// Subscribe to sessionData for file information
	let sessionResponse;
	sessionData.subscribe((value) => {
		sessionResponse = value;
	});

	// Reactive statements to keep file details in sync
	$: fileData = sessionResponse?.data;
	$: fileType = sessionResponse?.filetype;
	$: fileName = sessionResponse?.filename;
</script>

<div class="container">
	<!-- Left Section: Viewer -->
	<div class="left-div">
		{#if doc.presignedUrl}
			<iframe
				src={doc.presignedUrl}
				width="100%"
				height="100%"
				title="Document Viewer"
				frameborder="0"
			/>
		{:else if fileType === 'text/csv'}
			<TableDataViewer />
		{:else if fileType === 'application/pdf'}
			<PdfViewer pdfBlob={fileData} />
		{:else}
			<div class="file-not-supported">File type not supported for viewer.</div>
		{/if}
	</div>

	<!-- Right Section: Share Component -->
	<div class="right-div">
		<!-- <ShareComponent shareURL={doc.presignedUrl} /> -->
		<ShareComponent
			data={fileData}
			filetype={fileType}
			filename={fileName}
			presignedurl={doc.presignedUrl}
		/>
	</div>
</div>

<style>
	:global(body),
	:global(html) {
		margin: 0;
		padding: 0;
		overflow-y: hidden;
		height: 100%;
		font-family: Arial, sans-serif;
	}

	.container {
		display: flex;
		align-items: stretch;
		gap: 16px;
		background-color: #323639;
	}

	.left-div {
		flex: 4;
		display: flex;
		justify-content: center;
		overflow: auto;
		height: 750px;
		overflow-y: auto;
	}

	.right-div {
		flex: 1;
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		/* Optionally, match the left-div height */
		height: 750px;
	}
</style>
