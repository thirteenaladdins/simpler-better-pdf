import React from 'react';
import Image from 'next/image';
import { string } from 'prop-types';
import closeButton from '../public/x.svg';

function ListItem({ fileName }) {
  return (
    <div className="list-view">
      <li
        className="list-none
       p-4"
        // key={prop.keyName}
      >
        {fileName}
      </li>
      <Image className="fill-white" src={closeButton} />
    </div>
  );
}

export default ListItem;

ListItem.propTypes = {
  fileName: string.isRequired,
};
