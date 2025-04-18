<script>
	import { getBaseUrl } from '../utils/config';
	import { goto } from '$app/navigation';
	import { sessionData } from '../store/sessionStore.js';
	import { onMount, onDestroy } from 'svelte';
	import { loading } from '../store/loadingStore.js';
	import { duplicateError } from '../store/duplicateErrorStore.js';
	import { errorMessage } from '../store/errorMessageStore.js';
	import SideNav from '../components/SideNav.svelte';
	import DropAreaFileUpload from '../components/DropAreaFileUpload.svelte';
	import { selectedItem } from '../store/selectedItemStore.js';
	import { fileCount } from '../store/fileCountStore.js';
	import { writable } from 'svelte/store';
	import Loading from '../components/Loading.svelte';
	import {
		handleDragEnter,
		handleDragLeave,
		handleDragEnd,
		handleDrop
	} from '../utils/dragAndDrop';
	import {
		setHighlight,
		increaseCounter,
		decreaseCounter,
		resetCounter
	} from '../utils/dragState.js';
	import { isHighlighted } from '../utils/dragState.js';

	let highlighted;

	isHighlighted.subscribe((value) => {
		highlighted = value;
	});

	const baseUrl = getBaseUrl();

	console.log(import.meta.env);
	console.log('Base URL:', baseUrl);

	let uploadSuccessful = false;
	let responseData = null;
	export let serverAwake;
	export let showSuccessMessage;

	let isError;
	let dropArea;

	errorMessage.subscribe((value) => (isError = value));

	let dots = 3;
	let interval;

	if (typeof window != undefined) {
		onMount(() => {
			interval = setInterval(() => {
				if (dots < 3) {
					dots += 1;
				} else {
					dots = 1;
				}
			}, 500);
		});

		// onMount(() => {});
	}

	onDestroy(() => {
		clearInterval(interval);
	});

	if (typeof window != undefined) {
		onMount(async () => {
			try {
				const response = await fetch(`${baseUrl}/ping`);
				const data = await response.json();

				if (data.message === 'pong') {
					console.log(data);
					serverAwake = true;
					showSuccessMessage = true;

					setTimeout(() => {
						showSuccessMessage = false;
					}, 2000);
				} else {
					console.error('Ping failed!');
				}
			} catch (error) {
				console.error('Error pinging server:', error);
			}
		});
	}

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
		console.log('handle success', responseData);

		const elapsedTime = Date.now() - startTime;
		const delay = Math.max(0, 1500 - elapsedTime);

		setTimeout(() => {
			const docId = responseData.docid;
			console.log('Navigating to results page with docId:', docId);

			goto(`/results/${docId}`)
				.then(() => {
					console.log('Navigation successful');
					loading.set(false);
					showLoading = false;
				})
				.catch((error) => {
					console.error('Navigation error:', error);
				});
		}, delay);
	}

	function handleError(event) {
		let error = event.detail.message || 'An error occurred.';
		errorMessage.set(error);
	}

	let showError = writable(false);

	function displayError() {
		$showError = true;
		setTimeout(() => {
			$showError = false;
		}, 3000);
	}

	function highlight(event) {
		event.preventDefault();
		setHighlight(true);
	}
</script>

<!-- Success alert - or error alert that appears at the top of the page -->

{#if showLoading}
	<Loading />
{/if}

<div
	class="outerContainer {highlighted ? 'highlighted' : ''}"
	role="button"
	bind:this={dropArea}
	on:dragenter={() => handleDragEnter(event, increaseCounter, setHighlight)}
	on:dragover={highlight}
	on:dragleave={() => handleDragLeave(event, decreaseCounter, setHighlight)}
	on:dragend={() => handleDragEnd(event, resetCounter, setHighlight)}
	on:drop={() => handleDrop(event, resetCounter, setHighlight)}
	tabindex="0"
>
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
		font-family:
			Open Sans,
			-apple-system,
			BlinkMacSystemFont,
			Segoe UI,
			Roboto,
			Oxygen,
			Ubuntu,
			Cantarell,
			Fira Sans,
			Droid Sans,
			Helvetica Neue,
			sans-serif;
		font-size: 14px;
	}

	/* set this to the selection  */
	.outerContainer.highlighted {
		background-color: var(--accent-color);
		opacity: 0.25;
		/* opacity: inherit; */
		/* Additional styles to indicate highlighting */
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
		font-family:
			system-ui,
			-apple-system,
			BlinkMacSystemFont,
			Segoe UI,
			Roboto,
			Helvetica Neue,
			Arial,
			Noto Sans,
			sans-serif,
			Apple Color Emoji,
			Segoe UI Emoji,
			Segoe UI Symbol,
			Noto Color Emoji; /* now matching the navbar font */
		font-size: 14px; /* adjust if necessary to match navbar text size */
	}

	.error-alert.active {
		transform: translateY(0); /* slide it into view */
	}
</style>
