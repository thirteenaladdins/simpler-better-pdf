import React, { ReactNode } from 'react';
import SideBar from '../components/SideBar';
import NavigationBar from '../components/NavigationBar';

// type LayoutProps = {
//   children: ReactNode;
// };

interface LayoutProps {
  children: ReactNode;
  setOption: (option: string) => void;
  option: string;
}

function Layout({ children }: LayoutProps) {
  return (
    <div className="layout-container">
      <NavigationBar />
      <div className="content-container">
        <SideBar />
        <div className="main-container">{children}</div>
      </div>
    </div>
  );
}

export default Layout;
