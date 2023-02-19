import axios from 'axios';

let failedRequests = 0;

const uploadFile = async (file: File, option: string) => {
  const baseUrl = process.env.NODE_ENV === 'production'
    ? 'https://magic-extractor-v2.herokuapp.com'
    : 'http://localhost:8008';
  const url = `${baseUrl}/api/processfile`;

  const formData = new FormData();
  formData.append('file', file);
  formData.append('option', option);

  try {
    const response = await axios.post(url, formData, {
      headers: {
        'Access-Control-Allow-Origin': '*',
      },
    });
    return response;
  } catch (error) {
    console.error(error);
    failedRequests += 1;
    throw error;
  }
};

export default uploadFile;
