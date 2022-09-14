import { React, useState, setState } from 'react';
import MenuItems from './MenuItems';

// when the item is clicked - update the state of the parent component
// now we should pass the state to the parent component?
// only one can be true at a time

// option
// add selected state / true or false
export default function SideBar({ setOption }) {
  return (
    <div className="sidebar mx-auto pt-8 font-sans">
      {/* list item  */}
      <ul>
        {MenuItems.map((item, index) => (
          <li key={index}>
            <button type="button" className={item.cName} onClick={() => { setOption(item.title); }}>
              {item.title}
            </button>
          </li>
        ))}
      </ul>

    </div>
  );
}
