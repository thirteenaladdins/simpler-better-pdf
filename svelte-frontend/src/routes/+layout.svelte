<script>
	// import './+layout.js'; // This imports and runs the layout.js file
	import '../app.css';
	import Loading from '../components/Loading.svelte';
	import { loading } from '../store/loadingStore.js';
	// import { theme } from '../store/themeStore';
	import { theme } from '../store/themeStore';

	import { onMount } from 'svelte';

	// Body is initially hidden in app.css and unhidden here to avoid FOUC
	onMount(() => {
		// This code runs when the component is mounted in the DOM
		document.body.style.visibility = 'visible';
	});

	$: if (typeof window !== 'undefined' && $theme) {
		document.documentElement.setAttribute('data-theme', $theme.actual);
	}
</script>

<svelte:head>
	<!-- <script async src="https://www.googletagmanager.com/gtag/js?id=G-2X85K1KEH5"></script>
	<script>
		window.dataLayer = window.dataLayer || [];
		function gtag() {
			dataLayer.push(arguments);
		}
		gtag('js', new Date());

		gtag('config', 'G-2X85K1KEH5');
	</script> -->
</svelte:head>

{#if $loading}
	<Loading />
{/if}

<slot />
