import { createContext, useState, useEffect } from 'react';

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
    option: 'Luxury Goods',
    setOption: () => { },
    errorNotification: '',
    setErrorNotification: () => { },
    hideNav: false,
    setHideNav: () => { },
    hideInfo: false,
    setHideInfo: () => { },

});

const AppContextProvider = ({ children }: { children: React.ReactNode }) => {
    const [option, setOption] = useState('Luxury Goods');
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
};

export default AppContextProvider;
