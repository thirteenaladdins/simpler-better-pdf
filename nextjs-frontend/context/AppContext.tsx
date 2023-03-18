import React, { createContext, useState } from 'react';

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

function AppContextProvider({ children }: AppContextProviderProps) {
  const [option, setOption] = useState('Siemens Regex');
  const [errorNotification, setErrorNotification] = useState('');
  const [hideNav, setHideNav] = useState(false);
  const [hideInfo, setHideInfo] = useState(false);

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
