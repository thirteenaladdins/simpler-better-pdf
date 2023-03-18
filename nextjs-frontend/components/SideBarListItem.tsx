import React, { useContext, useEffect, useMemo } from 'react';
import { useRouter } from 'next/router';
import { AppContext } from '../context/AppContext';

interface ISideBarListItemProps {
  item: {
    title: string;
    url: string;
    cName: string;
  };
  // option: string;
}

export default function SideBarListItem({ item }: ISideBarListItemProps) {
  const { option, setOption } = useContext(AppContext);
  const router = useRouter();

  const handleClick = () => {
    setOption(item.title);
    localStorage.setItem('option', item.title);
    router.push(item.url);
  };

  const selectedClass = useMemo(() => (option === item.title ? 'selected' : ''), [option, item.title]);

  useEffect(() => {
    const storedOption = localStorage.getItem('option');
    if (storedOption) {
      setOption(storedOption);
      // console.log(storedOption);
      // console.log(option);
    }
  }, [setOption, option]);

  useEffect(() => {
    console.log('Option changed:', option);
  }, [option]);

  return (
    <li className={item.cName}>
      <button type="button" className={`sidebar-button ${selectedClass}`} style={{ cursor: 'pointer' }} onClick={handleClick}>
        {item.title}
      </button>
    </li>
  );
}
