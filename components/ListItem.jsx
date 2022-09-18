import React from 'react';
import Image from 'next/image';
import { string } from 'prop-types';
import closeButton from '../public/x.svg';

function ListItem({ fileName }) {
  return (
    <div className="flex rounded-md hover:bg-indigo-300">
      <li
        className="cursor-pointer list-none
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
