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
                    filetype = 'text/csv'; // Assume CSV for JSON data
                } else if (contentType === 'application/pdf') {
                    const baseUrl = process.env.NODE_ENV === 'production'
                        ? 'https://als-toolkit-518aa93f7ddc.herokuapp.com/'
                        : 'http://localhost:591';
                    const url = `${baseUrl}`;

                    const response = await axios.get(`${url}/api/fetch_file/${encodeURIComponent(dataObject)}`, {
                        responseType: 'blob',
                    });

                    return {
                        data: response.data, // This would be the blob
                        filetype: 'application/pdf'
                    };
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

    return {
        data: combinedString,
        filetype: filetype
    };
};

export default processAllFiles;
