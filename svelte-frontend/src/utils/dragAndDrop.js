//  In utility file

import { writable } from 'svelte/store';

export const selectedFilesStore = writable([]);

import { markDuplicates } from './markDuplicates';

import { fileCount } from '../store/fileCountStore';
import { duplicateError } from '../store/duplicateErrorStore';

// Do we moduarlise this further?
export function handleDrop(event, resetCounter, setHighlight) {
	event.preventDefault();
	event.stopPropagation();

	console.log('handle drop');
	const filesFromDrop = Array.from(event.dataTransfer.files);

	// Update the Svelte store with the new files and update file count
	selectedFilesStore.update((currentFiles) => {
		const updatedFiles = [...currentFiles, ...filesFromDrop];
		fileCount.set(updatedFiles.length); // Update fileCount store with the length of updatedFiles
		const { filesWithDuplicates, duplicatesCount } = markDuplicates(updatedFiles);
		if (duplicatesCount > 0) {
			duplicateError.set('One or more files is a duplicate marked in red below.');
		} else {
			duplicateError.set('');
		}

		return filesWithDuplicates;
	});

	// Reset the counter and unhighlight the drop area
	resetCounter();
	setHighlight(false);
}

export function handleDragEnter(event, increaseCounter, setHighlight) {
	event.preventDefault();
	event.stopPropagation();
	increaseCounter(); // Increases the dragCounter
	setHighlight(true); // Set isHighlighted to true
}

export function handleDragLeave(event, decreaseCounter, setHighlight) {
	event.preventDefault();
	event.stopPropagation();
	decreaseCounter(); // Decreases the dragCounter
	setHighlight(false); // Set isHighlighted to false if dragCounter is 0
}

export function handleDragEnd(event, resetCounter, setHighlight) {
	resetCounter();
	setHighlight(false);
}
