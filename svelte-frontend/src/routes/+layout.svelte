<script>
	// import './+layout.js'; // This imports and runs the layout.js file
	import '../app.css';
	import Loading from '../components/Loading.svelte';
	import { loading } from '../store/loadingStore.js';
	import NavigationBar from '../components/NavigationBar.svelte';
	// import { theme } from '../store/themeStore';
	import { theme } from '../store/themeStore';

	$: if (typeof window !== 'undefined' && $theme) {
		document.documentElement.setAttribute('data-theme', $theme.actual);
	}
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
</svelte:head>

<!-- Add version to the top left and link to github -->
<NavigationBar />

{#if $loading}
	<Loading />
{/if}

<slot />
