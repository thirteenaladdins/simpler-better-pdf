import React, { createContext, useState, useEffect } from 'react';

type AppContextProps = {
  option: string;
  setOption: (e: string) => void;
  errorNotification: string;
  setErrorNotification: (e: string) => void;
  hideNav: boolean;
  setHideNav: (e: boolean) => void;
  hideInfo: boolean;
  setHideInfo: (e: boolean) => void;
};

export const AppContext = createContext<AppContextProps>({
  option: 'Siemens Regex',
  setOption: () => { },
  errorNotification: '',
  setErrorNotification: () => { },
  hideNav: false,
  setHideNav: () => { },
  hideInfo: false,
  setHideInfo: () => { },

});

type AppContextProviderProps = {
  value: {
    option: string;
    setOption: (e: string) => void;
  };
  children: React.ReactNode;
};

function AppContextProvider({ value, children }: AppContextProviderProps) {
  const [option, setOption] = useState(value.option);
  const [errorNotification, setErrorNotification] = useState('');
  const [hideNav, setHideNav] = useState(false);
  const [hideInfo, setHideInfo] = useState(false);

  useEffect(() => {
    if (typeof window !== 'undefined') {
      const storedOption = localStorage.getItem('option');
      if (storedOption) {
        setOption(storedOption);
      }
    }
  }, []);

  return (
    <AppContext.Provider
      value={{
        option,
        setOption,
        errorNotification,
        setErrorNotification,
        hideNav,
        setHideNav,
        hideInfo,
        setHideInfo,
      }}
    >
      {children}
    </AppContext.Provider>
  );
}

export default AppContextProvider;
