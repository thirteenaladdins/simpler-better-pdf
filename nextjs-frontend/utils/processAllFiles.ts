import parseJsonData from './parseJsonData';
import uploadFile from '../pages/api/uploadFile';
import axios from 'axios';

const processAllFiles = async (files: File[], option: string): Promise<string> => {
  const responses: any[] = [];
  let isFirstFile = true;

  for (const file of files) {
    try {
      const responseData = await uploadFile(file, option);

      if (responseData.error) {
        console.error(`Error: Something went wrong with file ${file.name}:`, responseData.error);
        throw new Error(responseData.error);
      } else {
        const { contentType, dataObject } = responseData;
        
        if (contentType === 'application/json') {
          const parsedData = parseJsonData(JSON.parse(dataObject.data)).split("\r\n");

          if (isFirstFile) {
              responses.push(...parsedData);
              isFirstFile = false;
          } else {
              responses.push(...parsedData.slice(1));
          }
        } else if (contentType === 'application/pdf') { 
          const baseUrl = process.env.NODE_ENV === 'production'
            ? 'https://magic-extractor-v2.herokuapp.com'
            : 'http://localhost:591';
          const url = `${baseUrl}`;

          const response = await axios.get(`${url}/api/fetch_file/${encodeURIComponent(dataObject)}`, {
            responseType: 'blob',
          });

          return response.data;

        } else {
          throw new Error(`Unsupported content type: ${contentType}`);
        }
      }
    } catch (error) {
      console.error(`Error: Something went wrong with file ${file.name}:`, error);
      throw error;
    }
  }

  console.log(responses);

  const combinedString = responses.join("\r\n"); // Concatenate array elements with newline.

  return combinedString;
};

export default processAllFiles;
