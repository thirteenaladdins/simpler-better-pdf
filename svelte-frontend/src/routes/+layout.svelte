<script>
	import Loading from '../components/Loading.svelte';
	import { loading } from '../store/loadingStore.js';
</script>

<svelte:head>
	<!-- Google tag (gtag.js) -->
	<!-- Google tag (gtag.js) -->
	<!-- Google tag (gtag.js) -->
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

<div class="navbar">
	<!-- come back - this should also be a home button and across multiple pages -->
	<div class="title font-sans">ALS Toolkit</div>
</div>

{#if $loading}
	<Loading />
{/if}

<slot />

<style>
	/* * {
        border: 1px solid red;
    } */

	.font-sans {
		font-family: system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica Neue,
			Arial, Noto Sans, sans-serif, Apple Color Emoji, Segoe UI Emoji, Segoe UI Symbol,
			Noto Color Emoji;
	}

	/* .title {
        
    } */

	.navbar {
		border-bottom: 1px solid #d3d3d3;
		padding: 10px 0px;
	}
</style>
