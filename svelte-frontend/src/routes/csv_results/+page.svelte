<script>
	import TableDataViewer from '../../components/TableDataViewer.svelte';
	import DownloadSection from '../../components/DownloadSection.svelte';
	import { sessionData } from '../../store/sessionStore';

	// Use the data returned from the load function.
	export let data;
	const { docBlob } = data;

	// If needed, create an object URL for preview or downloading.
	let pdfURL = '';
	if (docBlob) {
		pdfURL = URL.createObjectURL(docBlob);
	}

	// (Optional) You can still use sessionData for other file info.
	let sessionResponse;
	sessionData.subscribe((value) => {
		sessionResponse = value;
	});

	$: fileData = sessionResponse?.data;
	$: fileType = sessionResponse?.filetype;
	$: fileName = sessionResponse?.filename;
</script>

<div class="container">
	<div class="left-div">
		{#if fileType === 'text/csv'}
			<TableDataViewer />
		{:else}
			<div class="file-not-supported">File type not supported for viewer.</div>
		{/if}
	</div>

	<div class="right-div">
		<DownloadSection />
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
		flex-direction: column;
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
