import parseJsonData from './parseJsonData';
import uploadFile from '../pages/api/uploadFile';

// may need to change the name
// import Error from '../components/common/Error'

interface ErrorResponse {
  file: File;
  // error: string;
}

// // TODO: instead of console logging errors bring them to the frontend with new component
// COME BACK TO THIS LATER
// SIMPLIFY ALL CODE

const processAllFiles = async (files: File[], option: string): Promise<string> => {
  const responses: any[] = [];

  for (const file of files) {
    try {
      const responseData = await uploadFile(file, option);

      // we need to retrieve the response data and check if there's an error key
      if (responseData.error) {
        console.error(`Error: Something went wrong with file ${file.name}:`, responseData.error);
        throw new Error(responseData.error);
      } else {
        responses.push(responseData.data);
      }
    } catch (error) {
      console.error(`Error: Something went wrong with file ${file.name}:`, error);
      throw error;
    }
  }

  const combinedResponses = responses.flat();
  const csvFormattedData = parseJsonData(combinedResponses);
  return csvFormattedData;
};

export default processAllFiles;

// const processAllFiles = async (files: File[], option: string): Promise<string> => {
//   const responses: any[] = [];
//   const errors: string[] = [];

//   for (const file of files) {
//     try {
//       const responseData = await uploadFile(file, option);

//       // we need to retrieve the response data and check if there's an error key
//       if (responseData.data.error) {
//         console.error(`Error: Something went wrong with file ${file.name}:`, responseData.data.error);
//         errors.push(responseData.data.error);
//       } else {
//         responses.push(responseData.data);
//       }
//     } catch (error) {
//       console.error(`Error: Something went wrong with file ${file.name}:`, error);
//       errors.push(error.message);
//     }
//   }

//   if (errors.length > 0) {
//     return <Error errors={errors} />;
//   }

//   const combinedResponses = responses.flat();
//   const csvFormattedData = parseJsonData(combinedResponses);
//   return csvFormattedData;
// };

// import parseJsonData from './parseJsonData';
// import uploadFile from '../pages/api/uploadFile';

// interface ErrorResponse {
//   file: File;
//   // error: string;
// }

// const processAllFiles = async (files: File[], option: string): Promise<string> => {
//   const responses: any[] = [];
//   const errors: string[] = [];

//   for (const file of files) {
//     try {
//       const responseData = await uploadFile(file, option);

//       // we need to retrieve the response data and check if there's an error key
//       if (responseData.data.error) {
//         console.error(`Error: Something went wrong with file ${file.name}:`, responseData.data.error);
//         errors.push(responseData.data.error);
//       } else {
//         responses.push(responseData.data);
//       }
//     } catch (error) {
//       console.error(`Error: Something went wrong with file ${file.name}:`, error);
//       errors.push(error.message);
//     }
//   }

//   if (errors.length > 0) {
//     return errors.join('\n');
//   }

//   const combinedResponses = responses.flat();
//   const csvFormattedData = parseJsonData(combinedResponses);
//   return csvFormattedData;
// };
