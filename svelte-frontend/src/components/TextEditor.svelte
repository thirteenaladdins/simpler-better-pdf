<!-- TextEditor.svelte -->
<script>
	import { createEventDispatcher, onMount } from 'svelte';

	export let id;
	export let pageIndex;
	export let x;
	export let y;
	export let text;
	export let width;
	export let height;
	export let fontSize;

	const dispatch = createEventDispatcher();
	let isEditing = false;
	let editorElement;

	onMount(() => {
		console.log('TextEditor mounted:', { id, x, y, text });
	});

	function handleClick(event) {
		console.log('TextEditor clicked:', { id, x, y, text });
		// Only stop propagation if we're entering edit mode
		if (!isEditing) {
			event.stopPropagation();
			isEditing = true;
			// Focus the editor after a small delay to ensure it's rendered
			setTimeout(() => {
				if (editorElement) {
					editorElement.focus();
					// Place cursor at the end of the text
					const range = document.createRange();
					const sel = window.getSelection();
					range.selectNodeContents(editorElement);
					range.collapse(false);
					sel.removeAllRanges();
					sel.addRange(range);
				}
			}, 0);
		}
	}

	function handleDoubleClick(event) {
		// Allow default text selection behavior
		// Don't stop propagation to allow natural text selection
	}

	function handleBlur() {
		console.log('TextEditor blur:', { id, x, y, text });
		isEditing = false;
		dispatch('update', { text, pageIndex, x, y });
	}

	function handleKeyDown(event) {
		if (event.key === 'Enter' && !event.shiftKey) {
			event.preventDefault();
			editorElement.blur();
		}
	}

	function handleMouseDown(event) {
		// Only stop propagation if we're in edit mode
		if (isEditing) {
			event.stopPropagation();
		}
	}

	function handleMouseMove(event) {
		// Only stop propagation if we're in edit mode
		if (isEditing) {
			event.stopPropagation();
		}
	}

	function handleMouseUp(event) {
		// Only stop propagation if we're in edit mode
		if (isEditing) {
			event.stopPropagation();
		}
	}

	function handleSelect(event) {
		// Allow text selection to propagate
	}
</script>

<div
	class="text-editor {isEditing ? 'editing' : ''}"
	style="left: {x}px; top: {y}px; width: {width}px; height: {height}px; font-size: {fontSize}px;"
	on:click={handleClick}
	on:dblclick={handleDoubleClick}
	on:blur={handleBlur}
	on:keydown={handleKeyDown}
	on:mousedown={handleMouseDown}
	on:mousemove={handleMouseMove}
	on:mouseup={handleMouseUp}
	on:select={handleSelect}
>
	{#if isEditing}
		<div
			class="editor-content"
			contenteditable="true"
			bind:this={editorElement}
			bind:textContent={text}
		/>
	{:else}
		<div class="text-content" on:mousedown|stopPropagation>{text}</div>
	{/if}
</div>

<style>
	.text-editor {
		position: absolute;
		background-color: transparent;
		border: none;
		padding: 0;
		margin: 0;
		outline: none;
		cursor: text;
		pointer-events: auto;
	}

	.text-editor.editing {
		background-color: rgba(255, 255, 255, 0.8);
		border: 1px solid #ccc;
		padding: 2px;
	}

	.editor-content {
		width: 100%;
		height: 100%;
		outline: none;
		white-space: pre-wrap;
		word-wrap: break-word;
		user-select: text;
		-webkit-user-select: text;
		-moz-user-select: text;
		-ms-user-select: text;
	}

	.text-content {
		width: 100%;
		height: 100%;
		white-space: pre-wrap;
		word-wrap: break-word;
		user-select: text;
		-webkit-user-select: text;
		-moz-user-select: text;
		-ms-user-select: text;
	}

	.text-content:hover {
		background-color: rgba(255, 255, 255, 0.5);
	}

	/* Add selection highlight color */
	.text-content::selection,
	.editor-content::selection {
		background-color: rgba(0, 123, 255, 0.3);
	}
</style>
