import React from 'react'
import closeButton from '../public/x.svg'
import Image from 'next/image'

function ListItem(prop) {
  return (
    <div className="flex rounded-md hover:bg-indigo-300">
      <li
        className="cursor-pointer list-none
       p-4"
        // key={prop.keyName}
      >
        {prop.fileName}
      </li>
      <Image className="fill-white" src={closeButton} />
    </div>
  )
}

export default ListItem
