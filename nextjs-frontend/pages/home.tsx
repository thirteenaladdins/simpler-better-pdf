import { useContext } from 'react';
import Extractor from '../components/Extractor';
import SideBar from '../components/SideBar';
import NavigationBar from '../components/NavigationBar';
import InfoComponent from '../components/InfoComponent';
import AppContextProvider from '../context/AppContext'
import { AppContext } from '../context/AppContext'
import Layout from '../layouts/Layout';

export default function LuxuryGoods(): JSX.Element {

    // ??
    const {
        option,
        setOption,
        errorNotification,
        setErrorNotification,
        hideNav,
        setHideNav,
        hideInfo,
        setHideInfo,
    } = useContext(AppContext);

    // const appContext = useContext(AppContext);

    const displayErrorNotification = (): string => {
        if (typeof errorNotification === 'number') {
            return `Selected ${errorNotification} file${errorNotification !== 1 ? 's' : ''
                } to extract`;
        }

        if (errorNotification !== '') {
            return errorNotification;
        }

        return `Selected ${option} to extract`;
    };

    const getHideNav = (e: boolean): void => {
        setHideNav(e);
    };

    const getHideInfo = (e: boolean): void => {
        setHideInfo(e);
    };

    return (
        <AppContextProvider value={{
            option, setOption
        }} >
            {/* what about here?  */}
            <Layout>
                {/*<Layout hideNav={getHideNav} hideInfo={getHideInfo} setOption={setOption} option={option} >*/}
                {/* move this to the  */}
                {/* <InfoComponent
                            hideNav={hideInfo}
                            hideInfo={hideInfo}
                            status={displayErrorNotification()}
                        /> */}
                <Extractor
                    option={option}
                // hideNav={getHideNav}
                // errNotif={setErrorNotification}
                // hideInfo={getHideInfo}
                />

            </Layout>
        </AppContextProvider >
    )
};
