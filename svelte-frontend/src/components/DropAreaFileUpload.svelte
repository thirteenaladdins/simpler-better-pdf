<!-- 
TODO: change this page slightly - 

remove border
make the drop area full size of the container
drop area should change to pdf viewer after upload with new tools
should apply the als logo with old view
remove file viewer 



-->
<script>
	import { createEventDispatcher } from 'svelte';
	import UploadIcon from '../icons/upload.svg';
	import FileIcon from '../components/FileIcon.svelte';
	import PdfViewer from './PdfViewer.svelte';
	import processAllFiles from '../utils/processAllFiles';

	const dispatch = createEventDispatcher();

	// STORE
	import { selectedItem } from '../store/selectedItemStore';
	import { fileCount } from '../store/fileCountStore';
	import { errorMessage } from '../store/errorMessageStore';
	import { loading } from '../store/loadingStore';
	import { duplicateError } from '../store/duplicateErrorStore';
	import { selectedFilesStore } from '../utils/dragAndDrop';

	// New props to handle PDF viewing state
	export let showPdfViewer = false;
	export let uploadedPdfFile = null;

	// UTILITY FUNCTIONS
	import { markDuplicates } from '../utils/markDuplicates';

	let currentSelectedItem = $selectedItem;

	selectedItem.subscribe((value) => {
		currentSelectedItem = value;
		// Do something with currentSelectedItem
	});

	// FILE UPLOAD
	// TODO: change this so it only uploads a single file and not multiple
	async function handleFileUpload(selectedFiles, selectedOption) {
		try {
			loading.set(true);

			// Just get the first file (there should only be one now)
			const fileToUpload = selectedFiles[0]?.file;

			if (!fileToUpload) {
				dispatch('uploadFailed', { message: 'No file selected for upload' });
				loading.set(false);
				return;
			}

			// Validate file type
			if (fileToUpload.type !== 'application/pdf') {
				dispatch('uploadFailed', { message: 'Please upload a valid PDF file' });
				loading.set(false);
				return;
			}

			// Validate file size (8MB limit)
			if (fileToUpload.size > 8 * 1024 * 1024) {
				dispatch('uploadFailed', { message: 'File size must be less than 8MB' });
				loading.set(false);
				return;
			}

			// Store the file for display and show it immediately
			uploadedPdfFile = fileToUpload;
			showPdfViewer = true;

			// Process the file in the background
			try {
				const responseData = await processAllFiles([fileToUpload], selectedOption);
				if (responseData) {
					dispatch('uploadSuccess', {
						...responseData,
						pdfFile: uploadedPdfFile
					});
				}
			} catch (error) {
				// Don't show error to user if background processing fails
				console.error('Background processing failed:', error);
			} finally {
				// Always clear loading state
				loading.set(false);
			}
		} catch (error) {
			dispatch('uploadFailed', error);
			loading.set(false);
		}
	}

	let fileInput;

	let selectedFiles = [];
	// Subscribe to selectedFiles store

	// this wiill be the single source of
	selectedFilesStore.subscribe((files) => {
		console.log(files);
		selectedFiles = files;
	});

	let dropArea;

	function onClickHandler(event) {
		// Stop propagation to prevent parent handlers from also triggering
		if (event) event.stopPropagation();
		fileInput.click();
	}

	let isHighlighted = false;

	// Does this work for all cases?
	function handleFiles(event) {
		const filesFromInput = Array.from(event.target.files);
		selectedFilesStore.update(() => {
			// Replace with new file instead of appending
			const newFiles = filesFromInput.map((file) => ({
				file,
				metadata: {
					/* Initial metadata setup */
				}
			}));
			return markDuplicates(newFiles).filesWithDuplicates;
		});
		event.target.value = ''; // Reset the file input

		// Automatically upload the file
		if (filesFromInput.length > 0) {
			handleFileUpload([{ file: filesFromInput[0] }], $selectedItem);
		}
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

{#if !showPdfViewer}
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
			on:click={(event) => {
				// Only trigger file input if clicking directly on the drop area (not on child elements)
				if (event.currentTarget === event.target) {
					onClickHandler(event);
				}
			}}
			on:keydown={(e) => e.key === 'Enter' && onClickHandler(e)}
		>
			<input
				bind:this={fileInput}
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
	</div>
{:else}
	<div class="pdf-viewer-container">
		{#if uploadedPdfFile}
			<PdfViewer pdfFile={uploadedPdfFile} />
		{:else}
			<div class="loading-pdf">Loading PDF viewer...</div>
		{/if}
	</div>
{/if}

<style>
	.file-upload-container {
		display: flex;
		justify-content: center;
		flex-direction: column;
		align-items: center;
		height: 25rem;
		width: 40rem;
		/* border: 2px solid var(--accent-color); */
		border-radius: 10px;
		/* background-color: var(--secondary-color); */
	}

	.pdf-viewer-container {
		width: 100%;
		height: 100%;
		display: flex;
		justify-content: center;
		align-items: center;
	}

	.pdf-embed {
		border-radius: 5px;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
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
		/* border: 2px dashed var(--accent-color); */
		border-radius: 10px; /* Added for rounded borders */
		/* background-color: #f5f7fd;  */
		/* Light background color for better contrast */
		transition: background-color 0.3s; /* Smooth transition for hover effect */
		cursor: pointer; /* Indicate the area is clickable */
		position: relative; /* For proper pointer-events handling */
		z-index: 1;
	}

	.drop-area-full > * {
		pointer-events: none; /* Make all direct children ignore pointer events */
	}

	/* Allow pointer events for specific elements that need interaction */
	.file-list {
		pointer-events: auto;
	}

	/* Ensure remove buttons in FileIcon work */
	:global(.file-list button) {
		pointer-events: auto;
	}

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
		display: none;
	}

	.title {
		font-weight: 500;
	}

	.font-sans {
		font-family:
			Open Sans,
			-apple-system,
			BlinkMacSystemFont,
			Segoe UI,
			Roboto,
			Oxygen,
			Ubuntu,
			Cantarell,
			Fira Sans,
			Droid Sans,
			Helvetica Neue,
			sans-serif;
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
