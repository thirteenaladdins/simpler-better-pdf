import React, { ReactNode, useContext } from 'react';
import SideBar from '../components/SideBar';
import NavigationBar from '../components/NavigationBar';
import AppContextProvider from '../context/AppContext'
import { AppContext } from '../context/AppContext'

// import
// import './Layout.css';

// interface ISidebarProps {
//     option: string;
//     hideNav: boolean;
// }

type LayoutProps = {
    children: ReactNode;
};

function Layout({ children }: LayoutProps) {

    const {
        option,
        setOption,
    } = useContext(AppContext);

    // <App

    return (
        <AppContextProvider value={{
            option, setOption
        }} >
            <div className="layout-container">
                <NavigationBar />
                <div className="content-container">
                    <SideBar setOption={setOption} option={option} />

                    <div className="main-container">{children}</div>
                </div>
            </div>
        </AppContextProvider>
    );
}

export default Layout;
