import React, { useMemo } from 'react';
import { useRouter } from 'next/router';

interface ISideBarListItemProps {
  item: {
    title: string;
    url: string;
    cName: string;
  };
}

const translateUrlToTitle = (url: string): string => {
  switch (url) {
    case '/home':
      return 'Siemens Regex';
    case '/luxury-goods':
      return 'Luxury Goods';
    case '/als-logo-header':
      return 'ALS Header';
    default:
      return '';
  }
};

export default function SideBarListItem({ item }: ISideBarListItemProps) {
  const router = useRouter();

  const handleClick = () => {
    localStorage.setItem('option', item.title);
    router.push(item.url);
  };

  const currentTitle = translateUrlToTitle(router.pathname);
  const selectedClass = useMemo(() => (currentTitle === item.title ? 'selected' : ''), [currentTitle, item.title]);

  return (
    <li className={item.cName}>
      <button type="button" className={`sidebar-button ${selectedClass}`} style={{ cursor: 'pointer' }} onClick={handleClick}>
        {item.title}
      </button>
    </li>
  );
}
