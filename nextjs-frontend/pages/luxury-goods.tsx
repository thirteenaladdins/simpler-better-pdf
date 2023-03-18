import React, { useContext } from 'react';
import Extractor from '../components/Extractor';
import AppContextProvider, { AppContext } from '../context/AppContext';
import Layout from '../layouts/Layout';

export default function LuxuryGoods(): JSX.Element {
    const {
        option,
        setOption,
        // errorNotification,
        // setErrorNotification,
        // hideNav,
        // setHideNav,
        // hideInfo,
        // setHideInfo,
    } = useContext(AppContext);

    // const displayErrorNotification = (): string => {
    //     if (typeof errorNotification === 'number') {
    //         return `Selected ${errorNotification} file${errorNotification !== 1 ? 's' : ''} to extract`;
    //     }

    //     if (errorNotification !== '') {
    //         return errorNotification;
    //     }

    //     return `Selected ${option} to extract`;
    // };

    // const getHideNav = (e: boolean): void => {
    //     setHideNav(e);
    // };

    // const getHideInfo = (e: boolean): void => {
    //     setHideInfo(e);
    // };

    return (
        <AppContextProvider
            value={{
                option,
                setOption,
                // errorNotification,
                // setErrorNotification,
                // hideNav,
                // setHideNav,
                // hideInfo,
                // setHideInfo,
            }}
        >
            {/* do I need the setoption here? */}
            <Layout setOption={setOption} option={option} >
                <Extractor
                // option={option}
                // hideNav={getHideNav} 
                // errNotif={setErrorNotification}
                // hideInfo={getHideInfo}
                />
            </Layout>
        </AppContextProvider>
    );
}
