import React, { useState, useContext } from 'react';
import ListView from './ListView';
import DropArea from './DropArea';
import DownloadButton from './DownloadButton';
import ErrorMessage from './common/ErrorMessage';
import { AppContext } from '../context/AppContext';

export type ExtractorState = {
  displayComponent: 'default_component' | 'download_component' | 'list_component' | 'invalid_file_component';
  selectedFiles: File[];
  // returnedData: BlobPart;
  returnedData: string;
  loading: boolean;
  downloadFile: boolean;
  // hideNav: boolean;
};

// type ExtractorProps = {
//   option: string;
//   // errNotif: (message: string) => void;
//   // hideNav: () => void;
//   // hideInfo: () => void;
// };

const initialState: ExtractorState = {
  displayComponent: 'default_component',
  selectedFiles: [],
  returnedData: '',
  loading: false,
  downloadFile: false,
  // hideNav: false,
};

function Extractor(): JSX.Element {
  const [state, setState] = useState<ExtractorState>(initialState);
  // const { errNotif, hideNav, hideInfo, option } = props;
  // const { option } = props;
  const appContext = useContext(AppContext);

  // const decoder = new TextDecoder('utf-8');
  // const data = decoder.decode(blob);

  const renderSwitch = () => {
    switch (state.displayComponent) {
      case 'download_component':
        return <DownloadButton data={state.returnedData} />;
      case 'list_component':
        return (
          <ListView
            state={state}
            setState={setState}
            // hideInfo={hideInfo}
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
          // errNotif={errNotif}
          // hideNav={hideNav}
          />
        );
    }
  };

  return <div>{renderSwitch()}</div>;
}

export default Extractor;
