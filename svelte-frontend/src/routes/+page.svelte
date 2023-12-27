<script>
	import { goto } from '$app/navigation';
	import { sessionData } from '../store/sessionStore.js';
	import { version } from '../utils/version.js';
	import { onMount, onDestroy } from 'svelte';
	import { loading } from '../store/loadingStore.js';
	import { duplicateError } from '../store/duplicateErrorStore.js';

	// this is used for duplicates at the moment should I change this?
	import { errorMessage } from '../store/errorMessageStore.js';

	import SideNav from '../components/SideNav.svelte';
	import DropAreaFileUpload from '../components/DropAreaFileUpload.svelte';
	import { selectedItem } from '../store/selectedItemStore.js';
	// import Footer from "../components/Footer.svelte";

	import { fileCount } from '../store/fileCountStore.js';

	let baseUrl;

	switch (import.meta.env.VITE_ENV) {
		case 'development':
			baseUrl = import.meta.env.VITE_BASE_URL_DEVELOPMENT;
			break;
		case 'test':
			baseUrl = import.meta.env.VITE_BASE_URL_TEST;
			break;
		case 'production':
			baseUrl = import.meta.env.VITE_BASE_URL_PRODUCTION;
			break;
		default:
			// production - default case if environment is not set properly
			baseUrl = 'https://als-toolkit-518aa93f7ddc.herokuapp.com';
	}

	// const baseUrl = import.meta.env.DEV
	// 	? import.meta.env.VITE_BASE_URL_DEVELOPMENT
	// 	: import.meta.env.VITE_BASE_URL_PRODUCTION;

	console.log(import.meta.env);
	console.log('Base URL:', baseUrl);

	let serverAwake = false; // Initially set to false
	let uploadSuccessful = false;
	let responseData = null;
	let isError;

	// let isDuplicate;

	errorMessage.subscribe((value) => (isError = value));

	let dots = 3;
	let interval;

	onMount(() => {
		interval = setInterval(() => {
			if (dots < 3) {
				dots += 1;
			} else {
				dots = 1;
			}
		}, 500); // Change the interval as per your requirement
	});

	onDestroy(() => {
		clearInterval(interval); // Cleanup to avoid memory leaks
	});

	let showSuccessMessage = false;

	onMount(async () => {
		try {
			// const baseUrl =
			// 	process.env.NODE_ENV === 'production'
			// 		? VITE_BASE_URL_PRODUCTION
			// 		: VITE_BASE_URL_DEVELOPMENT;

			const response = await fetch(`${baseUrl}/ping`);
			const data = await response.json();

			if (data.message === 'pong') {
				console.log(data);
				serverAwake = true;
				showSuccessMessage = true;

				setTimeout(() => {
					showSuccessMessage = false;
				}, 2000); // Message will disappear after 2 seconds
			} else {
				console.error('Ping failed!');
			}
		} catch (error) {
			console.error('Error pinging server:', error);
			// handleError(
			// 	'Failed to connect to the server. Please check your internet connection and try again.'
			// );
		}
	});

	let showLoading = false;
	let startTime;

	$: if ($loading && !showLoading) {
		showLoading = true;
		startTime = Date.now();
	}

	function handleSuccess(event) {
		uploadSuccessful = true;
		responseData = event.detail;
		sessionData.set(responseData);

		const elapsedTime = Date.now() - startTime;
		const delay = Math.max(0, 1500 - elapsedTime);
		if ($selectedItem === 'Annotate') {
			setTimeout(() => {
				goto('/pdf').then(() => {
					loading.set(false);
					showLoading = false;
				});
			}, delay);
		} else {
			setTimeout(() => {
				goto('/results').then(() => {
					loading.set(false);
					showLoading = false;
				});
			}, delay);
		}
	}

	function handleError(event) {
		let error = event.detail.message || 'An error occurred.';
		errorMessage.set(error); // This sets the error in the store which should trigger the alert to show
	}

	// import { slide } from 'svelte/transition';

	// function slideRight(node, { delay = 0, duration = 400 }) {
	// 	const style = getComputedStyle(node);
	// 	const transform = style.transform === 'none' ? '' : style.transform;

	// 	return {
	// 		delay,
	// 		duration,
	// 		css: (t) => `
	//         transform: ${transform} translateX(${(1 - t) * 100}%)`
	// 	};
	// }

	import { writable } from 'svelte/store';
	import Loading from '../components/Loading.svelte';
	let showError = writable(false); // store to control if the error is shown or not

	function displayError() {
		$showError = true;
		setTimeout(() => {
			$showError = false;
		}, 3000); // auto-hide after 3 seconds, adjust as needed
	}
</script>

<!-- Success alert - or error alert that appears at the top of the page -->

<!-- {#if  -->

<!-- <button on:click={displayError}>Trigger Error</button> -->
<!-- just an example button to trigger the error -->

<!-- {#if loading}
	<Loading />
{/if} -->

{#if showLoading}
	<Loading />
{/if}

<div class="outerContainer">
	<!-- Left column -->
	<div class="left-column">
		<SideNav />
	</div>

	<!-- Middle column -->
	<div class="middleColumn">
		<!-- Top part of the middle column -->
		<div class="middleTop server-message-wrapper">
			{#if !serverAwake}
				<p>Waking up server, please wait{'.'.repeat(dots)}</p>
			{/if}

			{#if showSuccessMessage}
				<p>Server connection established.</p>
			{/if}

			{#if $duplicateError}
				<p class="duplicate-error">{$duplicateError}</p>
			{/if}

			{#if isError}
				<div class="error-alert active">{$errorMessage}</div>
			{/if}

			{#if $fileCount}
				<p>You have selected {$fileCount} file{$fileCount === 1 ? '' : 's'}</p>
			{/if}
		</div>

		<div class="middle">
			<div class="dropArea uniformWidth">
				<DropAreaFileUpload on:uploadSuccess={handleSuccess} on:uploadFailed={handleError} />
			</div>
		</div>

		<!-- Bottom part of the middle column -->
		<div class="middleBottom" />
	</div>

	<!-- Right column -->
	<div class="right-column" />
</div>

<style>
	/* * {
		margin: 0;
		padding: 0;
	} */

	.outerContainer {
		display: flex;
		height: 90vh;
		background-color: #fafafa;
	}

	.left-column {
		flex: 1; /* This ensures each column takes equal width */
		/* padding: 1rem; */
	}

	.middleColumn {
		display: flex;
		flex-direction: column; /* Divides the middle column horizontally */
	}

	.right-column {
		flex: 1; /* This ensures each column takes equal width */
		/* padding: 1rem; */
	}

	.middleTop,
	.middle,
	.middleBottom {
		flex: 1; /* Each part of the middle column takes equal height */
		padding: 1rem;
	}

	.duplicate-error {
		color: red;
	}

	.server-message-wrapper {
		font-family: Open Sans, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Oxygen, Ubuntu,
			Cantarell, Fira Sans, Droid Sans, Helvetica Neue, sans-serif;
		font-size: 14px;
	}

	.error-alert {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		background-color: #f44336;
		color: white;
		text-align: center;
		padding: 16px 0; /* same as navbar */
		z-index: 1000;
		transform: translateY(-100%);
		transition: transform 0.3s ease-in-out;
		font-family: system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica Neue,
			Arial, Noto Sans, sans-serif, Apple Color Emoji, Segoe UI Emoji, Segoe UI Symbol,
			Noto Color Emoji; /* now matching the navbar font */
		font-size: 14px; /* adjust if necessary to match navbar text size */
	}

	.error-alert.active {
		transform: translateY(0); /* slide it into view */
	}
</style>
