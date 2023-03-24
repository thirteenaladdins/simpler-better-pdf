import { useContext, useState, useEffect } from 'react';
import { AppContext } from '../context/AppContext';

export function useAppContext() {
  const appContext = useContext(AppContext);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (typeof window !== 'undefined') {
      const storedOption = localStorage.getItem('option');
      if (storedOption) {
        appContext.setOption(storedOption);
      }
      setLoading(false);
    }
  }, []);

  return { ...appContext, loading };
}
