import parseJsonData from './parseJsonData';
import uploadFile from '../pages/api/uploadFile';

const processAllFiles = async (files, option) => {
  const responses = [];

  // eslint-disable-next-line no-restricted-syntax
  for (const file of files) {
    try {
      // eslint-disable-next-line no-await-in-loop
      const responseData = await uploadFile(file, option);
      responses.push(responseData.data);
    } catch {
      // FIXME: add proper error handling
      console.log('Error - something went wrong a file');
    }
  }

  // spread doesn't work for this line
  // eslint-disable-next-line prefer-spread
  const combinedResponses = [].concat.apply([], responses);
  // const combinedResponses = [...responses];

  // setState({ ...state, returnedData: true })
  const csvFormattedData = parseJsonData(combinedResponses);
  // console.log(csvFormattedData)
  return csvFormattedData;
};

export default processAllFiles;
