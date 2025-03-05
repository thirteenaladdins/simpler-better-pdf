<!-- change the UI - the upload button should be separate -->
<!-- 
removing any of the duplicates should make remove the red colour when no duplicates remain
start backwards from the list 

space all icons evenly in the box
fit five icons in the view
check file types on drag and drop - limit to only pdf
add file count at the top as well
when the duplicate is removed then remove the notification from the top
-->

<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import UploadIcon from '../icons/upload.svg';
	import FileIcon from '../components/FileIcon.svelte';
	import processAllFiles from '../utils/processAllFiles';

	const dispatch = createEventDispatcher();

	// STORE
	import { selectedItem } from '../store/selectedItemStore';
	import { fileCount } from '../store/fileCountStore';
	import { errorMessage } from '../store/errorMessageStore';
	import { loading } from '../store/loadingStore';
	import { duplicateError } from '../store/duplicateErrorStore';
	import { selectedFilesStore } from '../utils/dragAndDrop';

	// UTILITY FUNCTIONS
	import { markDuplicates } from '../utils/markDuplicates';

	let currentSelectedItem = $selectedItem;

	selectedItem.subscribe((value) => {
		currentSelectedItem = value;
		// Do something with currentSelectedItem
	});

	// FILE UPLOAD
	async function handleFileUpload(selectedFiles, selectedOption) {
		try {
			loading.set(true);

			const filesToUpload = selectedFiles.map((wrapper) => wrapper.file);

			const responseData = await processAllFiles(filesToUpload, selectedOption);

			// const responseData = await processAllFiles(selectedFiles, selectedOption);

			console.log('upload success, final hurdle?', responseData);

			if (responseData) {
				dispatch('uploadSuccess', responseData);
			} else {
				dispatch('uploadFailed', { message: 'Unexpected response from server' });
			}
		} catch (error) {
			dispatch('uploadFailed', error);
		}
	}

	let fileInput;

	let selectedFiles: any[] = [];
	// Subscribe to selectedFiles store

	// this wiill be the single source of
	selectedFilesStore.subscribe((files) => {
		console.log(files);
		selectedFiles = files;
	});

	let dropArea;

	function onClickHandler() {
		fileInput.click();
	}

	let isHighlighted = false;

	// Does this work for all cases?
	function handleFiles(event) {
		const filesFromInput = Array.from(event.target.files);
		selectedFilesStore.update((currentFiles) => {
			const updatedFiles = [
				...currentFiles,
				...filesFromInput.map((file) => ({
					file,
					metadata: {
						/* Initial metadata setup */
					}
				}))
			];
			return markDuplicates(updatedFiles).filesWithDuplicates;
		});
		event.target.value = ''; // Reset the file input
	}

	function removeFile(index) {
		selectedFilesStore.update((currentFiles) => {
			// Filter out the file at the specified index
			const updatedFiles = currentFiles.filter((_, i) => i !== index);

			// Recheck duplicates with the updated list of files
			const { filesWithDuplicates } = markDuplicates(updatedFiles.map((wrapper) => wrapper.file));
			fileCount.set(filesWithDuplicates.length);
			// Update duplicate error message
			if (filesWithDuplicates.some((wrapper) => wrapper.metadata.isDuplicate)) {
				duplicateError.set('One or more files is a duplicate marked in red below.');
			} else {
				duplicateError.set('');
			}
			// Return the updated list with recalculated duplicate status
			return filesWithDuplicates;
		});
	}
</script>

<div class="file-upload-container font-sans">
	<p class="title">File Upload</p>
	<button class="browse-button" on:click={onClickHandler}>Browse</button>
	<div
		role="button"
		bind:this={dropArea}
		class="drop-area-full {selectedFiles.length > 0 ? 'file-selected' : ''} {isHighlighted
			? 'highlighted'
			: ''}"
		tabindex="0"
	>
		<input
			bind:this={fileInput}
			multiple
			type="file"
			accept="application/pdf"
			style="display: none;"
			on:change={handleFiles}
		/>

		{#if selectedFiles.length === 0}
			<img
				src={UploadIcon}
				alt="Drop your files here"
				class="pointer-events-none select-none drop-icon"
			/>
			<div class="pointer-events-none select-none text-sm">
				Click to choose a file or drag it here
			</div>
		{/if}

		<!-- so here check the list for isDuplicate if the file name already exists -->
		<!-- <div class="file-list">
			{#each selectedFiles as file, index (index)}
				<FileIcon
					filename={file.name}
					size={file.size}
					type={file.type}
					isDuplicate={file.isDuplicate}
					on:remove={() => removeFile(index)}
				/>
			{/each}
		</div> -->

		<div class="file-list">
			{#each selectedFiles as fileWrapper, index (index)}
				<FileIcon
					filename={fileWrapper.file.name}
					size={fileWrapper.file.size}
					type={fileWrapper.file.type}
					isDuplicate={fileWrapper.metadata.isDuplicate}
					on:remove={() => removeFile(index)}
				/>
			{/each}
		</div>
	</div>

	<!-- after success, then load the component -->

	<button
		on:click={() => handleFileUpload(selectedFiles, $selectedItem)}
		class="upload-button"
		disabled={selectedFiles.length === 0}
	>
		Upload
	</button>
</div>

<style>
	.file-upload-container {
		display: flex;
		justify-content: center;
		flex-direction: column;
		align-items: center;
		height: 25rem;
		width: 40rem;
		border: 2px solid var(--accent-color);
		border-radius: 10px;
		background-color: var(--secondary-color);
	}

	.drop-area-full {
		display: flex;
		flex-direction: column; /* Changed to column for vertical alignment of icon and text */
		text-align: center;
		align-items: center;
		justify-content: center;
		overflow: hidden;
		height: 20rem;
		width: 36rem;
		padding: 1rem;
		font-size: 0.9rem;
		overflow-y: auto;
		overflow-wrap: normal;
		word-break: normal;
		border: 2px dashed var(--accent-color);
		border-radius: 10px; /* Added for rounded borders */
		/* background-color: #f5f7fd;  */
		/* Light background color for better contrast */
		transition: background-color 0.3s; /* Smooth transition for hover effect */
	}

	/* .drop-area-full:hover {
		background-color: var(--selection-background); 
		cursor: pointer;
	} */

	.drop-area-full.file-selected {
		/* Override or remove certain styles when a file is selected */
		display: flex;
		flex-direction: column; /* Changed to column for vertical alignment of icon and text */
		align-items: flex-start; /* Start items from the left */
		justify-content: flex-start; /* Start items from the top */
		overflow-wrap: normal;
		word-break: normal;

		/* background-color: var(--primary-color); */
		/* cursor: pointer; */
		border-radius: 10px; /* Added for rounded borders */
		/* background-color: #f5f7fd;  */
		/* Light background color for better contrast */
		transition: background-color 0.3s; /* Smooth transition for hover effect */
	}

	.highlighted {
		background-color: var(--selection-background);
	}

	.drop-icon {
		margin-bottom: 1rem; /* Spacing between the icon and text */
	}

	.file-list {
		display: flex;
		flex-direction: row;
		flex-wrap: wrap;
		align-items: flex-start; /* Start items from the top */
		justify-content: flex-start; /* Start items from the left */
		/* max-height: 200px; */
		/* overflow-y: auto; */
		margin-top: 1rem;
		width: 100%;
	}

	.browse-button {
		margin: 10px;
		border-radius: 2px;
		padding: 2px 6px;
		font-weight: 400;
		cursor: pointer;
	}

	.upload-button {
		margin: 10px;
		border-radius: 2px;
		padding: 2px 6px;
		font-weight: 400;
		cursor: pointer;
	}

	.upload-button:disabled {
		cursor: not-allowed;
	}

	.title {
		font-weight: 500;
	}

	.font-sans {
		font-family: Open Sans, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Oxygen, Ubuntu,
			Cantarell, Fira Sans, Droid Sans, Helvetica Neue, sans-serif;
	}

	:global(body[data-theme='Serpent'] .drop-area-full) {
		position: relative;
	}

	:global(body[data-theme='Serpent'] .drop-area-full .hidden-photo) {
		position: absolute;
		top: 0;
		left: 0;
		opacity: 0;
		transition: opacity 0.3s;
	}

	:global(body[data-theme='Serpent'] .drop-area-full:hover .hidden-photo) {
		opacity: 1;
	}
</style>
