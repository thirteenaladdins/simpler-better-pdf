<!-- loading page -->
<script>
	import { onDestroy, onMount } from 'svelte';

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
</script>

<!-- TODO: the text shouldn't move.  -->
<div class="loading">
	<p>Processing{'.'.repeat(dots)}</p>
</div>

<style>
	.loading {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background-color: rgba(255, 255, 255, 0.8);
		display: flex;
		justify-content: center;
		align-items: center;
		z-index: 9999; /* to make sure it appears on top of other content */
	}
</style>
