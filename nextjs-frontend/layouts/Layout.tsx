import React, { ReactNode, useContext } from 'react';
import SideBar from '../components/SideBar';
import NavigationBar from '../components/NavigationBar';
// import { AppContext } from '../context/AppContext';

interface ISidebarProps {
    option: string;
    hideNav: boolean;
}

type LayoutProps = {
    children: ReactNode;
};

//TODO:  add CSS

function Layout({ children }: LayoutProps) {

    // const { errorNotification, setErrorNotification, setOption, hideNav, option } = useContext(AppContext);
    // const { option } = useContext(AppContext);

    return (

        <>
            <NavigationBar />
            {/* I probably won't hide the sidebar anymore */}
            {/* <SideBar hideNav={hideNav} option={option} /> */}
            <SideBar />
            <div className="center-container">
                <div>{children}</div>
            </div>
        </>

    );
}

export default Layout;
