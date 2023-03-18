import axios from 'axios';

// let failedRequests = 0;

interface UploadFileResponseData {
  data: string;
  error?: string;
}

const uploadFile = async (file: File, option: string): Promise<UploadFileResponseData> => {
  const baseUrl = process.env.NODE_ENV === 'production'
    ? 'https://magic-extractor-v2.herokuapp.com'
    : 'http://localhost:591';
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
    // FIXME: remove this
    console.log(response);
    return response;
  } catch (error) {
    console.error(error);
    // failedRequests += 1;
    throw error;
  }
};

export default uploadFile;
