import React, { useContext } from 'react';
import Extractor from '../components/Extractor';
import AppContextProvider, { AppContext } from '../context/AppContext';

import Layout from '../layouts/Layout';

const fileType = 'text/csv';
const fileName = 'extracted_data.csv';

export default function SiemensRegex(): JSX.Element {
  const {
    option,
    setOption,
  } = useContext(AppContext);

  return (
    <AppContextProvider value={{
      option, setOption,
    }}
    >
      <Layout setOption={setOption} option={option} >
        <Extractor fileType={fileType} fileName={fileName} />
      </Layout>
    </AppContextProvider>
  );
}
