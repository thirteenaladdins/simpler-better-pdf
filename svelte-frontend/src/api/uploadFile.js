import axios from 'axios';

// dev, test, prod
const uploadFile = async (file, option) => {
	let baseUrl;

	switch (import.meta.env.VITE_ENV) {
		case 'development':
			baseUrl = import.meta.env.VITE_BASE_URL_DEVELOPMENT;
			break;
		case 'test':
			baseUrl = import.meta.env.VITE_BASE_URL_TEST;
			break;
		case 'production':
			baseUrl = import.meta.env.VITE_BASE_URL_PRODUCTION;
			break;
		default:
			// default case if environment is not set properly
			baseUrl = 'https://als-toolkit-518aa93f7ddc.herokuapp.com';
	}

	let endpoint = '/api/process_file';
	if (option === 'ALS Header' || option === 'ALS Header New') {
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
