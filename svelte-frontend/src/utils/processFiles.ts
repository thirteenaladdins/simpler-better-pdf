import parseJsonData from './parseJsonData';
import uploadFile from '../api/uploadFile';
import axios from 'axios';

// const BASE_URL = process.env.BASE_URL || 'http://localhost:591'

const BASE_URL = import.meta.env.DEV ? import.meta.env.VITE_BASE_URL_DEVELOPMENT : import.meta.env.VITE_BASE_URL_PRODUCTION;


const processFile = async (file: File, option: string) => {
    const responseData = await uploadFile(file, option);

    if (responseData.error) {
        console.error(`Error: Something went wrong with file ${file.name}:`, responseData.error);
        throw new Error(responseData.error);
    }

    const { contentType, dataObject } = responseData;

    if (contentType === 'application/json') {
        const parsedData = parseJsonData(JSON.parse(dataObject.data)).split("\r\n");
        return {
            data: parsedData,
            filetype: 'text/csv'
        };
    } else if (contentType === 'application/pdf') {
        const response = await axios.get(`${BASE_URL}/api/fetch_file/${encodeURIComponent(dataObject)}`, {
            responseType: 'blob',
        });
        return {
            data: response.data,
            filetype: 'application/pdf'
        };
    } else {
        throw new Error(`Unsupported content type: ${contentType}`);
    }
};

const processAllFiles = async (files: File[], option: string) => {
    const responses: any[] = [];
    let filetype: string | undefined = undefined;

    for (const file of files) {
        try {
            const result = await processFile(file, option);
            if (result.filetype === 'text/csv') {
                responses.push(...result.data);
            } else if (result.filetype === 'application/pdf') {
                return result; // If you still want to return immediately for PDFs
            }
            filetype = result.filetype;
        } catch (error) {
            console.error(`Error: Something went wrong with file ${file.name}:`, error);
            // Decide if you want to continue or halt the process
        }
    }

    return {
        data: responses.join("\r\n"),
        filetype: filetype
    };
};

export default processAllFiles;
