<script>
	// import FileIcon from '../icons/file.svg';
	import { createEventDispatcher } from 'svelte';

	export let filename = '';
	export let size = 0;
	export let isDuplicate = false; // Default value indicating whether it's a duplicate or not

	let isHovering = false;

	let tooltip;
	let filenameDiv;

	const dispatch = createEventDispatcher();

	function handleRemove() {
		dispatch('remove');
	}

	function adjustTooltipPosition() {
		if (tooltip && filenameDiv) {
			const rect = filenameDiv.getBoundingClientRect();

			if (rect.right + tooltip.offsetWidth > window.innerWidth) {
				tooltip.style.left = 'auto';
				tooltip.style.right = '0';
			} else {
				tooltip.style.left = '50%';
				tooltip.style.transform = 'translateX(-50%)';
			}
		}
	}
</script>

<div class={isDuplicate ? 'drop-icon duplicate' : 'drop-icon'}>
	<button on:click={handleRemove} class="remove-button">x</button>
	<svg
		xmlns="http://www.w3.org/2000/svg"
		width="24"
		height="24"
		viewBox="0 0 24 24"
		fill="none"
		stroke={isDuplicate ? 'red' : 'currentColor'}
		stroke-width="2"
		stroke-linecap="round"
		stroke-linejoin="round"
		class="feather feather-file"
		><path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z" />
		<polyline points="13 2 13 9 20 9" />
	</svg>

	<div
		bind:this={filenameDiv}
		class="filename"
		on:mouseover={() => {
			isHovering = true;
			adjustTooltipPosition();
		}}
		on:mouseout={() => (isHovering = false)}
	>
		{filename}
	</div>
	{#if isHovering}
		<div bind:this={tooltip} class="tooltip">{filename}</div>
	{/if}
	<div class="filesize">{Math.round(size / 1000)} KB</div>
</div>

<style>
	button[title] {
		cursor: pointer !important;
	}

	.drop-icon {
		width: 100px;
		border: 1px solid black;
		border-radius: 4px;
		margin: 4px;
		padding-bottom: 8px;
		display: flex;
		flex-direction: column;
		align-items: center;
		text-align: center;
		position: relative;
		/* padding: 4px; */
	}

	.drop-icon:hover > .remove-button {
		visibility: visible;
	}

	.remove-button {
		visibility: hidden;
		background-color: transparent;
		border: 1px solid transparent;
		cursor: pointer;
		font-size: 16px;
		color: black;
		position: relative;
		top: -2px; /* adjust these to position the "x" correctly */
		left: 32px;
	}

	.filename {
		width: 80%;
		font-size: 0.8rem;
		font-weight: 500;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
		margin-top: 0.5rem;
	}

	.filesize {
		font-size: 0.8rem;
		margin-top: 0.2rem;
	}

	.tooltip {
		position: absolute;
		top: 100%;
		left: 50%;
		transform: translateX(-50%);
		background-color: #333;
		color: white;
		padding: 0.2rem 0.5rem;
		border-radius: 4px;
		font-size: 0.8rem;
		white-space: nowrap;
		z-index: 10;
	}

	.duplicate {
		color: red;
		border: 1px solid red;
		border-radius: 4px;
	}

	/* .drop-icon:hover .tooltip {
        display: block;
    } */
</style>
