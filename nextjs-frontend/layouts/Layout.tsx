import React, { ReactNode, useContext } from 'react';
import SideBar from '../components/SideBar';
import NavigationBar from '../components/NavigationBar';
import AppContextProvider, { AppContext } from '../context/AppContext';

// import
// import './Layout.css';

// interface ISidebarProps {
//     option: string;
//     hideNav: boolean;
// }

type LayoutProps = {
  children: ReactNode;
  setOption: (e: string) => void;
  option: string;
};


function Layout({ children }: LayoutProps) {
  return (
    <div className="layout-container">
      <NavigationBar />
      <div className="content-container">
        {/* what were we doing with the option here? */}
        {/* <SideBar setOption={setOption} option={option} /> */}
        <SideBar />
        <div className="main-container">{children}</div>
      </div>
    </div>
  );
}

export default Layout;


// import React, { ReactNode, useContext } from 'react';
// import SideBar from '../components/SideBar';
// import NavigationBar from '../components/NavigationBar';
// import AppContextProvider, { AppContext } from '../context/AppContext';

// type LayoutProps = {
//   children: ReactNode;
// };

// function Layout({ children }: LayoutProps) {
//   const {
//     option,
//     setOption,
//   } = useContext(AppContext);

//   return (
//     <div className="layout-container">
//       <NavigationBar />
//       <div className="content-container">
//         <SideBar setOption={setOption} option={option} />
//         <div className="main-container">{children}</div>
//       </div>
//     </div>
//   );
// }

// function LayoutWithProvider({ children }: LayoutProps) {
//   return (
//     <AppContextProvider>
//       <Layout>{children}</Layout>
//     </AppContextProvider>
//   );
// }

// export default LayoutWithProvider;
