import parseJsonData from './parseJsonData';
import uploadFile from '../pages/api/uploadFile';
import axios from 'axios';

// instead of parsing this data, we write the file to the disk, 
// then we fetch the data and send it to the frontend and allow that file to be downloaded

const processAllFiles = async (files: File[], option: string): Promise<string> => {
  const responses: any[] = [];

  for (const file of files) {
    try {
      const responseData = await uploadFile(file, option);

      if (responseData.error) {
        console.error(`Error: Something went wrong with file ${file.name}:`, responseData.error);
        throw new Error(responseData.error);
      } else {
        const { contentType, dataObject } = responseData;
        // console.log(contentType)
        
        if (contentType === 'application/json') {
          
          // get a key using square brackets?
          
          responses.push(parseJsonData(JSON.parse(dataObject.data)));
        
        // this here will be only if there's a single file
        } else if (contentType === 'application/pdf') { 
          
          // this is the file path - this needs to be a url
          const baseUrl = process.env.NODE_ENV === 'production'
            ? 'https://magic-extractor-v2.herokuapp.com'
            : 'http://localhost:591';
          const url = `${baseUrl}`;

          const response = await axios.get(`${url}/api/fetch_file/${encodeURIComponent(dataObject)}`, {
            responseType: 'blob',
          });
          
          // Send the delete request after the file has been fetched successfully
          try {
            await axios.get(`${url}/api/delete_file/${encodeURIComponent(dataObject)}`);
            console.log('File deleted successfully');
          } catch (error) {
            console.error('Error deleting file:', error);
          }
          
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


  
  const combinedResponses = responses.flat();
  console.log(combinedResponses);
  
  // Handle combinedResponses appropriately
  // e.g., convert it to CSV or combine JSON and PDF data, depending on your requirements
  const combinedString = combinedResponses.join(','); // concatenate array elements with a comma separator
  
  // return combinedResponses;
  return combinedString;

};

export default processAllFiles;
