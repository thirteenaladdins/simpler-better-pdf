import React from 'react';
// import Image from 'next/image';
import { string } from 'prop-types';
// import closeButton from '../public/x.svg';

function ListItem({ fileName }) {
  return (
    <div className="list-item">
      <li
        className="list-item-text"
        // key={prop.keyName}
      >
        {fileName}
      </li>
      {/* TODO: Button here to remove a file - implement later */}
      {/* <Image className="fill-black" src={closeButton} /> */}
    </div>
  );
}

export default ListItem;

ListItem.propTypes = {
  fileName: string.isRequired,
};
