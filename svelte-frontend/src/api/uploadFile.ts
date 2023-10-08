import axios from 'axios';

interface UploadFileResponseData {
  error?: string;
  contentType: string;
  dataObject?: any;
  processType: string;
  json?: any;
  // json
}

// ocr extraction

const uploadFile = async (file: File, option: string): Promise<UploadFileResponseData> => {
  const baseUrl = process.env.NODE_ENV === 'production'
    ? 'https://als-toolkit-518aa93f7ddc.herokuapp.com/'
    : 'http://localhost:591';

  // Dynamically select the endpoint based on the processing option
  let endpoint = '/api/process_file';
  if (option === 'ALS Header' || option === 'ALS Header New') {
    endpoint = '/api/process_pdf';
  }
  else if (option == 'Annotate' ) {
    endpoint = '/ocr/upload'
  }

  const url = `${baseUrl}${endpoint}`;

  const formData = new FormData();
  formData.append('file', file);
  formData.append('option', option);

  try {
    const response = await axios.post(url, formData, {
      headers: {
        'Access-Control-Allow-Origin': '*',
      },
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
