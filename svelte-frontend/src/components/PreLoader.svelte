<!-- PreLoader.svelte -->
<script>
	export let loading = true;
</script>

{#if loading}
	<div class="preloader">Loading...</div>
{/if}

<style>
	.preloader {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		display: flex;
		align-items: center;
		justify-content: center;
		background-color: white;
		z-index: 1000;
	}
</style>
