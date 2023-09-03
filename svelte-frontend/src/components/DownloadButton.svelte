<script>
	import DownLoadIcon from '../icons/download.svelte';

	export let data;
	export let filetype;
	export let filename;

	// This will run whenever `data`, `fileType`, or `fileName` changes
	$: downloadURL = getDownloadURL();

	function getDownloadURL() {
		console.log(filetype);
		const downloadBlob = data instanceof Blob ? data : new Blob([data], { type: filetype });
		console.log(downloadBlob);
		return URL.createObjectURL(downloadBlob);
	}
</script>

<div class="download-component">
	<a download={filename} href={downloadURL} class="download-button-link">
		<div class="download-button">
			<DownLoadIcon />
			Download
		</div>
	</a>
</div>

<style>
	.download-button-link {
		text-decoration: none; /* Remove underline from links */
		display: inline-flex;
		align-items: center;
		border-radius: 5px;
		overflow: hidden;
	}

	.download-button {
		display: inline-flex; /* set the button's content to be a flexible box */
		align-items: center; /* vertically align icon and text */
		justify-content: center; /* horizontally center icon and text */
		gap: 14px;
		box-sizing: border-box;
		padding: 0 16px;
		margin: 4px;
		height: 36px;
		width: 200px;
		text-overflow: ellipsis;
		background: linear-gradient(145deg, #6366f1, #0156d0); /* Modern gradient */
		color: #fff;
		font-family: 'Arial', sans-serif;
		font-size: 14px;
		font-weight: 500;
		border: none;
		border-radius: 4px;
		overflow: hidden;
		outline: none;
		cursor: pointer;
		transition: transform 0.2s, box-shadow 0.2s;
		box-shadow: 0px 4px 6px rgba(0, 85, 255, 0.1);
	}

	.download-button:hover {
		transform: translateY(-2px);
		box-shadow: 0px 6px 8px rgba(0, 85, 255, 0.15);
	}

	.download-button:active {
		transform: translateY(1px);
		box-shadow: 0px 2px 4px rgba(0, 85, 255, 0.15);
	}
</style>
