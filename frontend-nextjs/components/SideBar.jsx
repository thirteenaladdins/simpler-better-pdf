import { React, useState } from 'react';
import {
  PropTypes,
} from 'prop-types';
import MenuItems from './MenuItems';

function ListItem({
  item, setOption, handleClick, isActive,
}) {
  return (
    <li className={item.cName}>
      <button
        type="button"
        className={`${
          !isActive ? 'basic-button' : 'basic-button selected'
        }`}
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
    <div className="sidebar font-sans">
      <ul>
        {MenuItems.map((sideBarItem) => (
          <ListItem
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

ListItem.propTypes = {
  item: PropTypes.shape({
    title: PropTypes.string.isRequired,
    cName: PropTypes.string.isRequired,
  }),
  setOption: PropTypes.func.isRequired,
  handleClick: PropTypes.func.isRequired,
  isActive: PropTypes.bool.isRequired,
};

ListItem.defaultProps = {
  item: {
    title: 'Siemens',
    cName: 'basic-button',
  },
};

SideBar.propTypes = {
  setOption: PropTypes.func.isRequired,
};
