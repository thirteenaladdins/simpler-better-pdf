import React from 'react';
import MenuItems from '../data/MenuItems';
// @ts-ignore  
import SideBarListItem from './SideBarListItem';

// export default function Sidebar({ setOption, option }: ISidebarProps) {
export default function Sidebar() {
  return (
    <div className="sidebar">
      <ul className="sidebar-list">
        {MenuItems.map((sideBarItem) => (
          <SideBarListItem key={sideBarItem.title} item={sideBarItem} />
        ))}
      </ul>
    </div>
  );
}
