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

<script>
	import { createEventDispatcher } from 'svelte';
	import UploadIcon from '../icons/upload.svg';
	import FileIcon from '../components/FileIcon.svelte';
	import processAllFiles from '../utils/processAllFiles';

	const dispatch = createEventDispatcher();

	// STORE
	import { selectedItem } from '../store/selectedItemStore';
	import { fileCount } from '../store/fileCountStore';
	import { errorMessage } from '../store/errorMessageStore';
	import { duplicateError } from '../store/duplicateErrorStore';
	import { loading } from '../store/loadingStore';

	let currentSelectedItem = $selectedItem;

	selectedItem.subscribe((value) => {
		currentSelectedItem = value;
		// Do something with currentSelectedItem
	});

	function getDuplicateFilenames(files) {
		const filenameCounts = new Map();

		for (const file of files) {
			filenameCounts.set(file.name, (filenameCounts.get(file.name) || 0) + 1);
		}

		const duplicates = new Set();

		for (const [filename, count] of filenameCounts.entries()) {
			if (count > 1) {
				duplicates.add(filename);
			}
		}

		return duplicates;
	}

	async function handleFileUpload(selectedFiles, selectedOption) {
		try {
			loading.set(true);
			const responseData = await processAllFiles(selectedFiles, selectedOption);
			console.log(responseData);

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
	let selectedFiles = [];

	let dropArea;
	let dragCounter = 0;

	function onClickHandler() {
		fileInput.click();
	}

	let isHighlighted = false;

	function highlight(event) {
		event.preventDefault();
		isHighlighted = true;
	}

	function unhighlight(event) {
		if (event) event.preventDefault();
		isHighlighted = false;
	}

	function handleDragEnter(event) {
		event.preventDefault();
		event.stopPropagation();
		dragCounter++;
		if (dragCounter === 1) {
			// Only highlight once
			highlight(event);
		}
	}

	function handleDragLeave(event) {
		event.preventDefault();
		event.stopPropagation();
		dragCounter--;
		if (dragCounter === 0) {
			unhighlight();
		}
	}

	function handleDrop(event) {
		event.preventDefault();
		event.stopPropagation();
		selectedFiles = [...selectedFiles, ...Array.from(event.dataTransfer.files)];

		// add count to variable
		fileCount.set(selectedFiles.length);
		markDuplicates();

		// TODO: finish implementing this
		// validateFileSize(selectedFiles);

		// Reset the counter and unhighlight the drop area
		dragCounter = 0;
		unhighlight();
	}

	function handleDragEnd(event) {
		dragCounter = 0;
		unhighlight();
	}

	function markDuplicates() {
		const seen = new Set();
		const duplicates = new Set();

		for (const file of selectedFiles) {
			if (seen.has(file.name)) {
				duplicates.add(file.name);
			}
			seen.add(file.name);
			file.isDuplicate = false; // Reset the isDuplicate property.
		}

		let encountered = new Set();
		for (const file of selectedFiles) {
			if (duplicates.has(file.name) && !encountered.has(file.name)) {
				encountered.add(file.name);
				continue;
			}
			if (duplicates.has(file.name) && encountered.has(file.name)) {
				file.isDuplicate = true;
			}
		}

		console.log(duplicates.size);
		// Update errorMessage based on the presence of duplicates
		if (duplicates.size > 0) {
			duplicateError.set('One or more files is a duplicate marked in red below.');
		} else {
			duplicateError.set('');
		}
	}

	function validateFileSize(files) {
		if (files.length > 0) {
			// Check if there are any files in the array
			for (let file of files) {
				// Loop through each file in the array
				if (file.size > 0) {
					console.log('file is good');
				} else {
					alert('File contains no data.');
					return false; // Exit the function and indicate a bad file was found
				}
			}
			return true; // All files are good
		}
		return false; // No files to validate
	}

	function handleFiles(event) {
		const filesFromInput = Array.from(event.target.files);
		selectedFiles = [...selectedFiles, ...filesFromInput];

		// add file count to store
		fileCount.set(selectedFiles.length);
		// Mark the duplicates
		markDuplicates();

		// TODO: finish implementing this
		// validateFileSize(selectedFiles);

		// Reset the file input for the next use
		event.target.value = '';
	}

	function removeFile(index) {
		selectedFiles.splice(index, 1);
		selectedFiles = [...selectedFiles]; // Reassign to trigger Svelte's reactivity
		fileCount.set(selectedFiles.length);
		markDuplicates();
	}

	// let file = document.querySelector('input[type="file"]').files[0];
	// if (file && file.size > 0) {
	// 	// Proceed with the upload or processing
	// } else {
	// 	alert('The file is empty or invalid.');
	// }
</script>

<div class="file-upload-container font-sans">
	<p class="title">File Upload</p>
	<button class="upload-button" on:click={onClickHandler}>Browse</button>
	<div
		role="button"
		bind:this={dropArea}
		class="drop-area-full {selectedFiles.length > 0 ? 'file-selected' : ''} {isHighlighted
			? 'highlighted'
			: ''}"
		on:dragenter={handleDragEnter}
		on:dragover={highlight}
		on:dragleave={handleDragLeave}
		on:dragend={handleDragEnd}
		on:drop={handleDrop}
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
		<div class="file-list">
			{#each selectedFiles as file, index (index)}
				<FileIcon
					filename={file.name}
					size={file.size}
					type={file.type}
					isDuplicate={file.isDuplicate}
					on:remove={() => removeFile(index)}
				/>
			{/each}
		</div>
	</div>

	<!-- after success, then load the component -->

	<button
		on:click={handleFileUpload(selectedFiles, $selectedItem)}
		class="upload-button"
		disabled={selectedFiles.length === 0}
	>
		Upload
	</button>
</div>

<!-- when you press upload it transmits the selected files as normal -->
<!-- processAllfiles, pass selectedFiles to this function -->

<!-- elif request.form["option"] == "ALS Header": -->

<!-- TODO -->
<!-- by selecting from the navbar we need to figure out how to pass that information here -->

<!-- TODO: 
  when the
- Add scrollable div 
- Add icons
- Add editing capabilities later on 
  do not reset file list unless explicitely asked to do so
-->

<style>
	.file-upload-container {
		display: flex;
		justify-content: center;
		flex-direction: column;
		align-items: center;
		height: 25rem;
		width: 40rem;
		border: 1px solid black;
		border-radius: 10px;
		background-color: white;
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
		border: 2px dashed #a5b4fc;
		border-radius: 10px; /* Added for rounded borders */
		/* background-color: #f5f7fd;  */
		/* Light background color for better contrast */
		transition: background-color 0.3s; /* Smooth transition for hover effect */
		background-color: white;
	}

	.drop-area-full:hover {
		/* background-color: #a5b4fc; */
		/* cursor: pointer; */
	}

	.drop-area-full.file-selected {
		/* Override or remove certain styles when a file is selected */
		display: flex;
		flex-direction: column; /* Changed to column for vertical alignment of icon and text */
		align-items: flex-start; /* Start items from the left */
		justify-content: flex-start; /* Start items from the top */
		overflow-wrap: normal;
		word-break: normal;
		border: 2px dashed #a5b4fc;

		/* cursor: pointer; */
		border-radius: 10px; /* Added for rounded borders */
		/* background-color: #f5f7fd;  */
		/* Light background color for better contrast */
		transition: background-color 0.3s; /* Smooth transition for hover effect */
	}

	.highlighted {
		background-color: #a5b4fc;
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

	.upload-button {
		margin: 10px;
	}

	.upload-button:disabled {
		background-color: #d1d5db;
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
