<script>
	import './layout.js'; // This imports and runs the layout.js file
	import '../app.css';
	import Loading from '../components/Loading.svelte';
	import { loading } from '../store/loadingStore.js';
	import NavigationBar from '../components/NavigationBar.svelte';
</script>

<svelte:head>
	<script async src="https://www.googletagmanager.com/gtag/js?id=G-2X85K1KEH5"></script>
	<script>
		window.dataLayer = window.dataLayer || [];
		function gtag() {
			dataLayer.push(arguments);
		}
		gtag('js', new Date());

		gtag('config', 'G-2X85K1KEH5');
	</script>

	<script>
		// Set the initial theme based on local storage
		const theme = localStorage.getItem('theme') || 'Light';
		document.documentElement.setAttribute('data-theme', theme);
	</script>
</svelte:head>

<!-- Add version to the top left and link to github -->
<NavigationBar />

{#if $loading}
	<Loading />
{/if}

<slot />
