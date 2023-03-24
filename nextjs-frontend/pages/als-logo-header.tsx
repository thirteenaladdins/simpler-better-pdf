import React, { useContext } from 'react';
import Extractor from '../components/Extractor';

import AppContextProvider, { AppContext } from '../context/AppContext';

import Layout from '../layouts/Layout';

const fileType = 'application/pdf';

// TODO: I can set the file name here, come back and fix this later.
// fetch the name from backend
const fileName = 'modified_file.pdf';

export default function ALSHeader(): JSX.Element {
    const {
        option,
        setOption,
    } = useContext(AppContext);

    // 
    return (
        <AppContextProvider value={{
            option, setOption,
        }}
        >
            <Layout setOption={setOption} option={option} >
                <Extractor fileType={fileType} fileName={fileName}
                />

            </Layout>
        </AppContextProvider>
    );
}
