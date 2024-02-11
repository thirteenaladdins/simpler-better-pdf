// export function markDuplicates(files) {
// 	const seen = new Set();
// 	const duplicates = new Set();

// 	// we want to update the metadata instead we're creating a new property here
// 	const filesWithDuplicatesMarked = files.map((file) => {
// 		// Explicitly copy each property
// 		return {
// 			file,
// 			// metadata: {
// 			name: file.name,
// 			lastModified: file.lastModified,
// 			size: file.size,
// 			type: file.type,
// 			// Add any other properties you need
// 			isDuplicate: false
// 			// }
// 		};
// 	});

// 	for (const file of filesWithDuplicatesMarked) {
// 		// console.log('isDuplicate', file);
// 		if (seen.has(file.name)) {
// 			duplicates.add(file.name);
// 		}
// 		seen.add(file.name);
// 	}

// 	let encountered = new Set();
// 	for (const file of filesWithDuplicatesMarked) {
// 		if (duplicates.has(file.name) && !encountered.has(file.name)) {
// 			encountered.add(file.name);
// 			continue;
// 		}
// 		if (duplicates.has(file.name) && encountered.has(file.name)) {
// 			// file.isDuplicate = true;
// 		}
// 	}

// 	return { filesWithDuplicates: filesWithDuplicatesMarked, duplicatesCount: duplicates.size };
// }

export function markDuplicates(files) {
	const seen = new Set();
	const duplicates = new Set();

	const filesWithDuplicatesMarked = files.map((fileWrapper) => {
		// Check if the file is already wrapped
		if (fileWrapper.metadata) {
			// File is already processed, so just return it
			return fileWrapper;
		} else {
			// Wrap the raw File object
			return {
				file: fileWrapper, // Assuming fileWrapper is a raw File object here
				metadata: {
					isDuplicate: false
				}
			};
		}
	});

	for (const fileWrapper of filesWithDuplicatesMarked) {
		const fileName = fileWrapper.file.name;
		if (seen.has(fileName)) {
			duplicates.add(fileName);
			fileWrapper.metadata.isDuplicate = true; // Mark as duplicate
		} else {
			seen.add(fileName);
		}
	}

	return { filesWithDuplicates: filesWithDuplicatesMarked, duplicatesCount: duplicates.size };
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
