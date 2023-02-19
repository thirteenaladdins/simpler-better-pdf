import parseJsonData from './parseJsonData';
import uploadFile from '../pages/api/uploadFile';

const processAllFiles = async (files: File[], option: string): Promise<string> => {
  const responses: any[] = [];

  for (const file of files) {
    try {
      const responseData = await uploadFile(file, option);
      responses.push(responseData.data);
    } catch (error) {
      console.error('Error: Something went wrong with a file', error);
    }
  }

  const combinedResponses = responses.flat();

  const csvFormattedData = parseJsonData(combinedResponses);
  return csvFormattedData;
};

export default processAllFiles;
