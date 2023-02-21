import React, { useState, useContext } from 'react';
import MenuItems from './MenuItems';
import { AppContext } from '../context/AppContext';
import SidebarListItem from './SideBarListItem';

// TODO: simplify this to use only option to set

// interface ISidebarListItemProps {
//   item: {
//     title: string;
//     cName: string;
//   };
//   handleClick: (item: string) => void;
//   isActive: boolean;
// }

// TODO: reimplment hideNav if
interface ISidebarProps {
  setOption: (option: string) => void;
  option: string;
  // hideNav: boolean;
}

export default function SideBar() {
  const { option } = useContext(AppContext); // use context data

  return (
    // <div className={hideNav ? 'sidebar-hidden' : 'sidebar'}>
    <div>
      <ul className="sidebar-list">
        {MenuItems.map((sideBarItem) => (
          <SidebarListItem
            key={sideBarItem.title}
            item={sideBarItem}
            isActive={option === sideBarItem.title}
          />

        ))}
      </ul>
    </div>
  );
}
