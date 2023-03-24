import axios from 'axios';

interface UploadFileResponseData {
  // data: any; // Change from string to any as response can be anything
  error?: string;
  contentType: string;
  dataObject?: any;
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

    const contentType = response.headers['content-type']; // use brackets instead of get() 
    
    // console.log(contentType)
    // console.log(response.data);

    const dataObject = response.data;
    // console.log(dataObject);

    return {
      contentType,
      dataObject,
    };
  } catch (error) {
    console.error(error);
    throw error;
  }
};

export default uploadFile;
