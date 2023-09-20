import parseJsonData from './parseJsonData';
import uploadFile from '../api/uploadFile';
import axios from 'axios';

// TODO: FIX THIS

// Adjust the return type to accommodate for the new return format
const processAllFiles = async (files: File[], option: string): Promise<{ data: string | Blob, filetype?: string }> => {
    const responses: any[] = [];
    let isFirstFile = true;
    let filetype: string | undefined = undefined; // Add this to capture the filetype

    for (const file of files) {
        try {
            const responseData = await uploadFile(file, option);
            // const headers = responseData.headers
            // console.log(responseData)
            // console.log(headers)
            console.log(responseData.processType)
            
            if (responseData.error) {
                console.error(`Error: Something went wrong with file ${file.name}:`, responseData.error);
                throw new Error(responseData.error);
            } else {
                // const { contentType, dataObject, headers } = await uploadFile(file, option);
                // const processType = headers['x-process-type'];
                const { contentType, dataObject, processType } = responseData;

                // instead read content header 
                if (processType === 'Luxury Goods') {
                    const parsedData = parseJsonData(JSON.parse(responseData.dataObject.data)).split("\r\n");

                    if (isFirstFile) {
                        responses.push(...parsedData);
                        isFirstFile = false;
                    } else {
                        responses.push(...parsedData.slice(1));
                    }
                    filetype = 'text/csv'; // Assume CSV for JSON data
                } else if (processType === 'ALS Header') {
                    const baseUrl = process.env.NODE_ENV === 'production'
                        ? 'https://als-toolkit-518aa93f7ddc.herokuapp.com/'
                        : 'http://localhost:591';
                    const url = `${baseUrl}`;
                    
                    // instead of fetching the file we want to return the blob
                    // const response = await axios.get(`${url}/api/fetch_file/${encodeURIComponent(dataObject.url)}`, {
                    //     responseType: 'blob',
                    // });

                    const response = await axios.get(`${url}/api/fetch_file/${encodeURIComponent(dataObject.url)}`, {
                        responseType: 'blob',
                    });

                    return {
                        data: response.data, // This would be the blob
                        filetype: 'application/pdf'
                    };
                } else if (processType === 'ALS Header New') {
                    // this shouldn't be called url
                    let encodedPdf = responseData.dataObject.url;
                    let decodedPdf = atob(encodedPdf);  // Decode Base64 string to character string
                
                    // Convert character string to Uint8Array
                    const uint8Array = new Uint8Array(decodedPdf.length);
                    for (let i = 0; i < decodedPdf.length; i++) {
                        uint8Array[i] = decodedPdf.charCodeAt(i);
                    }
                
                    // Convert Uint8Array to Blob
                    const blob = new Blob([uint8Array], { type: 'application/pdf' });
                
                    return {
                        data: blob, // This would be the blob
                        filetype: 'application/pdf'
                    };
                }
                  else {
                    throw new Error(`Unsupported content type: ${processType}`);
                }
            }
        } catch (error) {
            console.error(`Error: Something went wrong with file ${file.name}:`, error);
            throw error;
        }
    }

    console.log(responses);

    const combinedString = responses.join("\r\n"); // Concatenate array elements with newline.

    return {
        data: combinedString,
        filetype: filetype
    };
};

export default processAllFiles;
