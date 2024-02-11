import axios from 'axios';

import { getBaseUrl } from '../utils/config';

// dev, test, prod,
const uploadFile = async (file, option) => {
	const baseUrl = getBaseUrl();

	let endpoint = '/api/process_file';

	if (option === 'ALS Header' || option === 'ALS Header New' || option === 'Re-Save PDF') {
		endpoint = '/api/process_pdf';
	} else if (option === 'Annotate') {
		endpoint = '/ocr/upload';
	}

	const url = `${baseUrl}${endpoint}`;

	const formData = new FormData();
	formData.append('file', file);
	formData.append('option', option);

	try {
		const response = await axios.post(url, formData, {
			headers: {
				'Access-Control-Allow-Origin': '*'
			}
		});

		const contentType = response.headers['content-type'];
		const dataObject = response.data;
		const processType = response.data.processType;

		return {
			contentType,
			dataObject,
			processType
		};
	} catch (error) {
		console.error(error);
		throw error;
	}
};

export default uploadFile;
