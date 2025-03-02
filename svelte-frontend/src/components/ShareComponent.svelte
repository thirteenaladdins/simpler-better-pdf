<script>
	import { onMount } from 'svelte';
	import DownLoadIcon from '../icons/download.svelte';

	// --- Download Functionality Props ---
	export let data;
	export let filetype;
	export let filename;
	// export let presignedurl;

	// --- Share Functionality ---
	let shareURL = '';
	let copied = false;

	onMount(() => {
		shareURL = window.location.href;
	});

	function copyLink() {
		navigator.clipboard
			.writeText(shareURL)
			.then(() => {
				copied = true;
				setTimeout(() => (copied = false), 2000);
			})
			.catch((err) => console.error('Error copying link:', err));
	}

	async function shareLink() {
		if (navigator.share) {
			try {
				await navigator.share({
					title: 'Share Document',
					url: shareURL
				});
			} catch (error) {
				console.error('Sharing failed:', error);
			}
		} else {
			copyLink();
		}
	}
	function getDownloadURL() {
		const downloadBlob = data instanceof Blob ? data : new Blob([data], { type: filetype });
		return URL.createObjectURL(downloadBlob);
	}

	// --- Download URL Computation ---
	// $: downloadURL = presignedurl || getDownloadURL();
	$: downloadURL = getDownloadURL();
</script>

<div class="action-container">
	<!-- Share Section -->
	<div class="share-section">
		<div class="share-buttons">
			<button on:click={shareLink} class="share-button">Share</button>
			<button on:click={copyLink} class="copy-button">Copy Link</button>
		</div>
		{#if copied}
			<span class="copy-feedback">Link copied!</span>
		{/if}
	</div>

	<!-- Download Section -->
	<!-- <div class="download-section">
		<a download={filename} href={downloadURL} class="download-button-link">
			<div class="download-button">
				<DownLoadIcon />
				<span>Download</span>
			</div>
		</a>
	</div> -->
</div>

<style>
	.action-container {
		display: flex;
		flex-direction: column;
		gap: 20px;
		align-items: center;
		margin-top: 20px;
	}

	/* Share Section Styling */
	.share-section {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 10px;
	}

	.share-buttons {
		display: flex;
		gap: 10px;
		width: 200px; /* Fixed width matching the download button */
	}

	.share-button,
	.copy-button,
	.download-button {
		padding: 8px 16px;
		font-size: 1rem;
		cursor: pointer;
		border: 1px solid #000;
		background: #f0f0f0;
		border-radius: 4px;
		transition: background 0.3s, color 0.3s;
		font-family: Arial, sans-serif;
	}

	.share-button,
	.copy-button {
		flex: 1; /* Equal width for both buttons */
	}

	.share-button:hover,
	.copy-button:hover,
	.download-button:hover {
		background: #000;
		color: #fff;
	}

	.copy-feedback {
		font-size: 0.9rem;
		color: #000;
	}

	/* Download Section Styling */
	.download-button-link {
		text-decoration: none;
		background: none;
		display: inline-flex;
		align-items: center;
		border-radius: 5px;
		overflow: hidden;
	}

	.download-button {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		gap: 14px;
		box-sizing: border-box;
		padding: 0 16px;
		height: 36px;
		width: 200px;
		background: #f0f0f0;
		border-radius: 4px;
		color: #000;
		font-size: 1rem;
		font-weight: 500;
		cursor: pointer;
		transition: background 0.3s, transform 0.2s, box-shadow 0.2s;
	}
</style>
