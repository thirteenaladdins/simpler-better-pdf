<script>
	import TableDataViewer from '../../components/TableDataViewer.svelte';
	import DownloadSection from '../../components/DownloadSection.svelte';
</script>

<div class="container">
	<div class="left-div">
		<TableDataViewer />
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
