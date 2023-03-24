import React, { useContext } from 'react';
import AppContextProvider, { AppContext } from '../context/AppContext';
import Extractor from '../components/Extractor';
import Layout from '../layouts/Layout';

const fileType = 'export/csv';
const fileName = 'extracted_data.csv';

export default function LuxuryGoods() {
    const { option, setOption } = useContext(AppContext);

    return (
        <AppContextProvider value={{ option, setOption }}>
            <Layout setOption={setOption} option={option}>
                <Extractor fileType={fileType} fileName={fileName} />
            </Layout>
        </AppContextProvider>
    );
}
