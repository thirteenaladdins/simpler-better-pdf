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
	// import Footer from "../components/Footer.svelte";

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
			// const response = await fetch('https://als-toolkit-518aa93f7ddc.herokuapp.com/ping');

			const baseUrl =
				process.env.NODE_ENV === 'production'
					? 'https://als-toolkit-518aa93f7ddc.herokuapp.com/'
					: 'http://localhost:591';

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

	// this actually runs after the thing has processed
	// maybe loading should start immediately and then error or success after
	function handleSuccess(event) {
		uploadSuccessful = true;
		responseData = event.detail;
		sessionData.set(responseData);
		loading.set(true);

		// Add a delay of 2 seconds before navigating to the results page
		// TODO: add results/UUID.
		setTimeout(() => {
			goto('/results').then(() => {
				loading.set(false);
			});
		}, 2500);
	}

	function handleError(event) {
		let error = event.detail.message || 'An error occurred.';
		errorMessage.set(error); // This sets the error in the store which should trigger the alert to show
	}

	// import { slide } from 'svelte/transition';

	function slideRight(node, { delay = 0, duration = 400 }) {
		const style = getComputedStyle(node);
		const transform = style.transform === 'none' ? '' : style.transform;

		return {
			delay,
			duration,
			css: (t) => `
            transform: ${transform} translateX(${(1 - t) * 100}%)`
		};
	}
</script>

<!-- Success alert - or error alert that appears at the top of the page -->

<div class="outerContainer">
	<!-- Left column -->
	<div class="column">
		<div class="side-nav">
			<SideNav />
		</div>
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
				<div transition:slideRight class="error-alert">
					{$errorMessage}
				</div>
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
	<div class="column" />
</div>

<style>
	body {
		background: #fafafa;
	}

	body,
	html {
		margin: 0;
		padding: 0;
		height: 100%;
		overflow-y: auto;
	}

	.outerContainer {
		display: flex;
		height: 80vh;
	}

	.column {
		flex: 1; /* This ensures each column takes equal width */
		/* padding: 1rem; */
	}

	.middleColumn {
		display: flex;
		flex-direction: column; /* Divides the middle column horizontally */
	}

	.middleTop,
	.middle,
	.middleBottom {
		flex: 1; /* Each part of the middle column takes equal height */
		padding: 1rem;
	}

	.side-nav {
		width: 120px;
	}

	/* message-wrapper {

    } */

	.duplicate-error {
		color: red;
	}

	.server-message-wrapper {
		font-family: Open Sans, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Oxygen, Ubuntu,
			Cantarell, Fira Sans, Droid Sans, Helvetica Neue, sans-serif;
		font-size: 14px;
	}
</style>
