import parseJsonData from './parseJsonData';
import uploadFile from '../api/uploadFile';
import axios from 'axios';
import { getBaseUrl } from './config';
import JSZip from 'jszip';

// Add an example object at the top or somewhere
// JSDoc annotations

function handleLuxuryGoods(responseData, responses, isFirstFile) {
	// ... code for Luxury Goods ...
}

// decode PDF
function handleALSHeader(dataObject) {
	try {
		let encodedPdf = dataObject.url;
		let decodedPdf = atob(encodedPdf);
		const uint8Array = new Uint8Array(decodedPdf.length);
		for (let i = 0; i < decodedPdf.length; i++) {
			uint8Array[i] = decodedPdf.charCodeAt(i);
		}
		const blob = new Blob([uint8Array], { type: 'application/pdf' });

		return {
			success: true,
			data: blob,
			filetype: 'application/pdf',
			filename: dataObject.fileName
		};
	} catch (error) {
		console.error(`Error in handleALSHeader: ${error}`);
		return {
			success: false,
			errorMessage: `Failed to process ALS Header: ${error.message}`
		};
	}
}

function handleReSavePdf(dataObject) {
	try {
		let encodedPdf = dataObject.url;
		let decodedPdf = atob(encodedPdf);
		const uint8Array = new Uint8Array(decodedPdf.length);
		for (let i = 0; i < decodedPdf.length; i++) {
			uint8Array[i] = decodedPdf.charCodeAt(i);
		}
		const blob = new Blob([uint8Array], { type: 'application/pdf' });

		return {
			success: true,
			data: blob,
			filetype: 'application/pdf',
			filename: dataObject.fileName
		};
	} catch (error) {
		console.error(`Error in Re-Save PDF: ${error}`);
		return {
			success: false,
			errorMessage: `Failed to re-save PDF : ${error.message}`
		};
	}
}

const processAllFiles = async (files, option) => {
	const responses = [];
	const pdfFiles = [];
	const errors = [];

	let isFirstFile = true;
	let filetype; // Initialize variable without a type

	for (const file of files) {
		try {
			const responseData = await uploadFile(file, option);

			console.log(responseData.processType);

			if (responseData.error) {
				errors.push(`Error with file ${file.name}: ${responseData.error}`);
				continue; // Skip to next file
			}
			if (responseData.error) {
				console.error(`Error: Something went wrong with file ${file.name}:`, responseData.error);
				throw new Error(responseData.error);
			} else {
				const { contentType, dataObject, processType } = responseData;

				if (processType === 'Luxury Goods') {
					const parsedData = parseJsonData(JSON.parse(responseData.dataObject.data)).split('\r\n');

					if (isFirstFile) {
						responses.push(...parsedData);
						isFirstFile = false;
					} else {
						responses.push(...parsedData.slice(1));
					}
					filetype = 'text/csv';
				} else if (processType === 'ALS Header New') {
					// Example of handling the return value
					const result = handleALSHeader(dataObject);
					if (result.success) {
						// Process the successful result
						return result;
					} else {
						// Handle the error case
						console.error(result.errorMessage);
						// Continue with other files or handle error
					}
				} else if (processType === 'Re-Save PDF') {
					const result = handleReSavePdf(dataObject);

					if (result.success) {
						// Process the successful result
						// TODO: add suffix such as - "resaved" on the file?
						pdfFiles.push({ blob: result.data, filename: result.filename });
					} else {
						// Handle the error case
						console.error(result.errorMessage);
						// Continue with other files or handle error
					}
				} else if (processType === 'Annotate') {
					return dataObject;
				} else {
					throw new Error(`Unsupported content type: ${processType}`);
				}
			}
		} catch (error) {
			console.error(`Error: Something went wrong with file ${file.name}:`, error);
			throw error;
		}
	}

	if (errors.length > 0) {
		// Handle accumulated errors here
		console.error('Errors occurred:', errors);
	}

	// After processing all files
	if (option === 'Re-Save PDF' && pdfFiles.length > 0) {
		const zip = new JSZip();
		for (const pdfFile of pdfFiles) {
			zip.file(pdfFile.filename, pdfFile.blob);
		}

		const zipBlob = await zip.generateAsync({ type: 'blob' });
		// saveAs(zipBlob, 'processed_files.zip');

		return {
			data: zipBlob,
			filetype: 'application/zip',
			filename: 'processed_files.zip'
		};
	}

	console.log(responses);

	const combinedString = responses.join('\r\n');

	return {
		data: combinedString,
		filetype: filetype
	};
};

export default processAllFiles;
