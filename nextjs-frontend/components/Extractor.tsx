import React, { useState, useContext } from 'react';
import ListView from './ListView';
import DropArea from './DropArea';
import DownloadButton from './DownloadButton';
import ErrorMessage from './common/ErrorMessage';
import { AppContext } from '../context/AppContext';

export type ExtractorState = {
  displayComponent: 'default_component' | 'download_component' | 'list_component' | 'invalid_file_component';
  selectedFiles: File[];
  returnedData: string | Blob;
  loading: boolean;
  downloadFile: boolean;
  fileType: string;
  fileName: string;
};

const initialState: ExtractorState = {
  displayComponent: 'default_component',
  selectedFiles: [],
  returnedData: '',
  loading: false,
  downloadFile: false,
  fileType: '',
  fileName: '',
};

type ExtractorProps = {
  fileType: string;
  fileName: string;
};

function Extractor({ fileType, fileName }: ExtractorProps): JSX.Element {
  const [state, setState] = useState<ExtractorState>(initialState);
  const appContext = useContext(AppContext);

  // const updateFileDetails = (fileType: string, fileName: string) => {
  //   setState((prevState) => ({
  //     ...prevState,
  //     fileType,
  //     fileName,
  //   }));
  // };

  console.log(state);

  const renderSwitch = () => {
    switch (state.displayComponent) {
      case 'download_component':
        return <DownloadButton data={state.returnedData} fileType={fileType} fileName={fileName} />;
      case 'list_component':
        return (
          <ListView
            state={state}
            setState={setState}
            option={appContext.option}
          />
        );
      case 'invalid_file_component':
        return <ErrorMessage />;
      case 'default_component':
      default:
        return (
          <DropArea
            state={state}
            setState={setState}
          // updateFileDetails={updateFileDetails}
          />
        );
    }
  };

  return <div>{renderSwitch()}</div>;
}

export default Extractor;


