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
		<svg
			xmlns="http://www.w3.org/2000/svg"
			width="24"
			height="24"
			viewBox="0 0 24 24"
			fill="none"
			stroke="currentColor"
			stroke-width="2"
			stroke-linecap="round"
			stroke-linejoin="round"
			class="logo-icon"
		>
			<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
			<polyline points="14 2 14 8 20 8"></polyline>
		</svg>
	</div>
</div>

<style>
	/* * {
		border: 1px solid red;
	} */

	.font-sans {
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
			Noto Color Emoji;
	}
	.navbar {
		border-bottom: 1px solid #d3d3d3;
		padding: 4px 10px;
		height: 30px;
		display: flex;
		align-items: center;
	}

	.home-button {
		cursor: pointer;
		border-radius: 4px;
		padding: 2px;
		display: flex;
		align-items: center;
	}

	.logo-icon {
		color: var(--accent-color, #3b82f6);
	}
</style>
