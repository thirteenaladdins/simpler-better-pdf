<!-- Add version to the top left and link to github -->
<script>
	import refreshPage from '../utils/refreshPage';
</script>

<div class="navbar font-sans">
	<!-- come back - this should also be a home button and across multiple pages -->
	<div
		role="button"
		tabindex="0"
		on:click={refreshPage}
		on:keydown={refreshPage}
		class="home-button"
	>
		Simpler Better Pdf
	</div>
</div>

<style>
	/* * {
		border: 1px solid red;
	} */

	.font-sans {
		font-family: system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica Neue,
			Arial, Noto Sans, sans-serif, Apple Color Emoji, Segoe UI Emoji, Segoe UI Symbol,
			Noto Color Emoji;
	}
	.navbar {
		border-bottom: 1px solid #d3d3d3;
		padding: 10px;
	}

	.home-button {
		cursor: pointer;
		border-radius: 4px;
		padding: 4px;
		display: inline-block;
	}
</style>
