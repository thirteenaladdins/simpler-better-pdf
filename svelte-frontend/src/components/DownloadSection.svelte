<script>
	import { goto } from '$app/navigation';

	// universal button component?

	import DownloadButton from './DownloadButton.svelte';
	import RefreshIcon from '../icons/refresh-cw.svelte';
	import SendIcon from '../icons/send.svelte';
	import { sessionData } from '../store/sessionStore';
	import refreshPage from '../utils/refreshPage';

	let sessionResponse;

	sessionData.subscribe((value) => {
		sessionResponse = value;
	});

	// Use reactive statements so these always reflect sessionResponse's current state
	$: fileData = sessionResponse?.data;
	$: fileType = sessionResponse?.filetype;
	// $: fileName = formatFileName(sessionResponse?.filename);
	$: fileName = sessionResponse?.filename;
	$: presignedUrl = sessionResponse?.presignedurl;

	// function formatFileName2(originalFileName) {
	// 	// check if the file
	// 	// split the file name based on the extension,
	// 	// anything after the dot is kept

	// 	// Get current date and time
	// 	const now = new Date();
	// 	const formattedDateTime = now.toISOString().replace(/[-:T]/g, '').slice(0, 15); // 'YYYYMMDDHHMMSS'

	// 	return formattedFileName;
	// }
</script>

<!-- TODO: move this to the right side  -->
<div class="download-section">
	<!-- <DownloadButton data={fileData} filename={fileName} filetype={fileType} /> -->
	<DownloadButton
		data={fileData}
		filename={fileName}
		filetype={fileType}
		presignedurl={presignedUrl}
	/>

	<button class="refresh" on:click={() => refreshPage()}>
		<RefreshIcon /> Start Over
	</button>
</div>

<style>
	.download-section {
		display: flex;
		align-items: center;
		flex-direction: column;
		justify-content: flex-start; /* Align items from the top */
		height: 100vh;
		padding-top: 20vh; /* Push buttons roughly a third of the way down */
		border-left: 1px solid #d3d3d3;
	}

	.refresh {
		display: inline-flex;
		align-items: center;
		box-sizing: border-box;
		margin-top: 50px; /* Adjust this to increase the gap as desired */
		/* margin: 4px; */
		height: 36px;
		gap: 10px;
		background: none; /* Remove background */
		/* color: #6366f1; */
		font-family: 'Arial', sans-serif;
		font-size: 14px;
		font-weight: 500;
		border: none;
		border-radius: 4px;
		overflow: hidden;
		outline: none;
		cursor: pointer;
		transition: transform 0.2s, box-shadow 0.2s;
	}

	.send {
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
		background: linear-gradient(145deg, #ff8db4, #e6007a); /* Complementary pink gradient */
		transition: background 0.3s; /* Smooth transition for the background */
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

	.send:hover {
		background: linear-gradient(145deg, #e678a2, #d0006b); /* Slightly darkened pink gradient */
	}

	/* .refresh-icon:hover {
		transform: translateY(-2px);
	} */

	/* .refresh-icon:active {
		transform: translateY(1px);
	} */
</style>
