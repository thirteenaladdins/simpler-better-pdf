import React from 'react';
import MenuItems from '../data/MenuItems';
import SidebarListItem from './SidebarListItem';

// interface ISidebarProps {
//   setOption: (option: string) => void;
//   option: string;
// }

// type SidebarProps = {
//   setOption: (e: string) => void;
//   option: string;
// }


// export default function Sidebar({ setOption, option }: ISidebarProps) {
export default function Sidebar() {
  return (
    <div className="sidebar">
      <ul className="sidebar-list">
        {MenuItems.map((sideBarItem) => (
          <SidebarListItem key={sideBarItem.title} item={sideBarItem} />
        ))}
      </ul>
    </div>
  );
}
