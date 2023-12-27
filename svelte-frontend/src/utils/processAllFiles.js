import parseJsonData from './parseJsonData';
import uploadFile from '../api/uploadFile';
import axios from 'axios';
import encodedPdf from './10735004.js';

const processAllFiles = async (files, option) => {
	const responses = [];
	let isFirstFile = true;
	let filetype; // Initialize variable without a type

	for (const file of files) {
		try {
			const responseData = await uploadFile(file, option);

			console.log(responseData.processType);

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
					filetype = 'text/csv'; // Assume CSV for JSON data
				} else if (processType === 'ALS Header') {
					const baseUrl = import.meta.env.DEV
						? import.meta.env.VITE_BASE_URL_DEVELOPMENT
						: import.meta.env.VITE_BASE_URL_PRODUCTION;

					const response = await axios.get(
						`${baseUrl}/api/fetch_file/${encodeURIComponent(dataObject.url)}`,
						{
							responseType: 'blob'
						}
					);

					return {
						data: response.data, // This would be the blob
						filetype: 'application/pdf'
					};
				} else if (processType === 'ALS Header New') {
					let encodedPdf = responseData.dataObject.url;
					// let encoded = encodedPdf;
					let decodedPdf = atob(encodedPdf);

					const uint8Array = new Uint8Array(decodedPdf.length);
					for (let i = 0; i < decodedPdf.length; i++) {
						uint8Array[i] = decodedPdf.charCodeAt(i);
					}

					const blob = new Blob([uint8Array], { type: 'application/pdf' });

					return {
						data: blob,
						filetype: 'application/pdf',
						filename: dataObject.fileName
					};
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

	console.log(responses);

	const combinedString = responses.join('\r\n');

	return {
		data: combinedString,
		filetype: filetype
	};
};

export default processAllFiles;
