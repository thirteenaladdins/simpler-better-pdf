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
	selectedFilesStore.update(() => {
		// Just use the first file if multiple files are dropped
		const newFile = filesFromDrop.length > 0 ? [filesFromDrop[0]] : [];
		fileCount.set(newFile.length); // Update fileCount with 1 or 0
		
		// Check if file is a duplicate with empty array since we're replacing
		const { filesWithDuplicates, duplicatesCount } = markDuplicates(newFile);
		
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
