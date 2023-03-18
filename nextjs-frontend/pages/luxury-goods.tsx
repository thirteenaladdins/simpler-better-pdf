import React, { useContext } from 'react';
import Extractor from '../components/Extractor';
import AppContextProvider, { AppContext } from '../context/AppContext';
import Layout from '../layouts/Layout';

export default function LuxuryGoods(): JSX.Element {
    const {
        option,
        setOption,
    } = useContext(AppContext);

    // const displayErrorNotification = (): string => {
    //     if (typeof errorNotification === 'number') {
    //         return `Selected ${errorNotification} file${errorNotification !== 1 ? 's' : ''} to extract`;
    //     }

    //     if (errorNotification !== '') {
    //         return errorNotification;
    //     }

    return (
        <AppContextProvider
            value={{
                option,
                setOption,
            }}
        >
            {/* do I need the setoption here? */}
            <Layout setOption={setOption} option={option} >
                <Extractor />
            </Layout>
        </AppContextProvider>
    );
}
