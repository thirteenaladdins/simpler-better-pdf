<script>
	import TableDataViewer from '../../../components/TableDataViewer.svelte';
	import { sessionData } from '../../../store/sessionStore';
	import ShareComponent from '../../../components/ShareComponent.svelte';

	export let data;
	const { docBlob, docUrl } = data;

	// Use the permanent URL for the download link
	let pdfURL = docUrl;

	// (Optional) You can still use sessionData for other file info.
	let sessionResponse;
	sessionData.subscribe((value) => {
		sessionResponse = value;
	});

	$: fileData = sessionResponse?.data;
	$: fileType = sessionResponse?.filetype || 'application/pdf';
	$: fileName = sessionResponse?.filename;
</script>

<div class="container">
	<div class="left-div">
		{#if fileType === 'text/csv'}
			<TableDataViewer />
		{:else if fileType === 'application/pdf'}
			<!-- Pass the blob from the load function to the PDF viewer -->
			<!-- <PdfViewer pdfBlob={docBlob} /> -->
			<embed src={pdfURL} type="application/pdf" width="100%" height="760px" />
		{:else}
			<div class="file-not-supported">File type not supported for viewer.</div>
		{/if}
	</div>

	<div class="right-div">
		<ShareComponent data={fileData} filetype={fileType} filename={fileName} />
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
		height: 750px;
	}
</style>
