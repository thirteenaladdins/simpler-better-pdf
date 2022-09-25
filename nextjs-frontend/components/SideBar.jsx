import { React, useState } from 'react';
import {
  PropTypes,
} from 'prop-types';
import MenuItems from './MenuItems';

// new function to decide className
// default to selected on the first item?
function getClassName(isActive) {
  if (!isActive) {
    return 'sidebar-button';
  }
  return 'sidebar-button selected';
}
// !isActive ? 'sidebar-button' : 'sidebar-button selected';

function SidebarListItem({
  item, setOption, handleClick, isActive,
}) {
  return (
    <li className={item.cName}>
      <button
        type="button"
        // className={`${
        //   !isActive ? 'sidebar-button' : 'sidebar-button selected'
        // }`}
        className={`${getClassName(isActive)}`}
        onClick={() => {
          setOption(item.title);
          handleClick(item.title);
        }}
      >
        {item.title}
      </button>
    </li>
  );
}

export default function SideBar({ setOption }) {
  // const [selected, setSelected] = useState(false);
  const [active, setActive] = useState();

  const handleClick = (item) => (active === item ? setActive() : setActive(item));

  return (
    <div className="sidebar">
      <ul className="sidebar-list">
        {MenuItems.map((sideBarItem) => (
          <SidebarListItem
            key={sideBarItem.title}
            item={sideBarItem}
            setOption={setOption}
            handleClick={handleClick}
            isActive={active === sideBarItem.title}
          />
        ))}
      </ul>

    </div>
  );
}

SidebarListItem.propTypes = {
  item: PropTypes.shape({
    title: PropTypes.string.isRequired,
    cName: PropTypes.string.isRequired,
  }),
  setOption: PropTypes.func.isRequired,
  handleClick: PropTypes.func.isRequired,
  isActive: PropTypes.bool.isRequired,
};

// what does this even do here?
SidebarListItem.defaultProps = {
  item: {
    title: 'Siemens Regex',
    cName: 'sidebar-button',
  },
};

SideBar.propTypes = {
  setOption: PropTypes.func.isRequired,
};
