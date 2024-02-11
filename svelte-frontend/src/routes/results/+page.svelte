<script>
	import TableDataViewer from '../../components/TableDataViewer.svelte';
	import DownloadSection from '../../components/DownloadSection.svelte';

	import { sessionData } from '../../store/sessionStore';

	// TODO: render
	import PdfViewer from '../../components/PDFViewer.svelte';

	let sessionResponse;

	sessionData.subscribe((value) => {
		sessionResponse = value;
	});

	// Use reactive statements so these always reflect sessionResponse's current state
	$: fileData = sessionResponse?.data;
	$: fileType = sessionResponse?.filetype;
	// $: fileName = formatFileName(sessionResponse?.filename);
	$: fileName = sessionResponse?.filename;

	console.log(fileType);
</script>

<div class="container">
	<div class="left-div">
		{#if fileType === 'text/csv'}
			<TableDataViewer />
		{:else if fileType === 'pdf'}
			<!-- <PDFViewer /> -->
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
	}

	.container {
		display: flex;
		align-items: start;
		/* margin: 20px; */
		/* width: 100%; */
		/* border: 1px solid black; */
	}

	.left-div,
	.right-div {
		height: 100%;
		margin: 0; /* Reset any potential default margins */
	}

	.left-div {
		flex: 4;
		overflow: auto;
		padding-left: 16px;
	}

	.right-div {
		flex: 1;
	}
</style>
