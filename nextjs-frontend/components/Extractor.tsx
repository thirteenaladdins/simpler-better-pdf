import React, { useState } from 'react';
import ListView from './ListView';
import DropArea from './DropArea';
import DownloadButton from './DownloadButton';
import ErrorMessage from '../components/common/ErrorMessage';


type ExtractorState = {
  displayComponent: 'default_component' | 'download_component' | 'list_component' | 'invalid_file_component';
  selectedFiles: File[];
  returnedData: BlobPart;
  loading: boolean;
  downloadFile: boolean;
  hideNav: boolean;
};

type ExtractorProps = {
  option: string;
  errNotif: (message: string) => void;
  hideNav: () => void;
  hideInfo: () => void;
};

const initialState: ExtractorState = {
  displayComponent: 'default_component',
  selectedFiles: [],
  returnedData: '',
  loading: false,
  downloadFile: false,
  hideNav: false,
};

function Extractor(props: ExtractorProps) {
  const [state, setState] = useState(initialState);
  const { errNotif, hideNav, hideInfo, option } = props;

  const renderSwitch = (currentState: ExtractorState) => {
    switch (currentState.displayComponent) {
      case 'download_component':
        return <DownloadButton data={state.returnedData} />;
      case 'list_component':
        return (
          <ListView
            state={currentState}
            setState={setState}
            hideInfo={hideInfo}
            option={option}
          />
        );
      case 'invalid_file_component':
        return <ErrorMessage />;
      case 'default_component':
      default:
        return (
          <DropArea
            state={currentState}
            setState={setState}
            errNotif={errNotif}
            hideNav={hideNav}
          />
        );
    }
  };

  return (
    <div className="main-container">
      {renderSwitch(state)}
    </div>
  );
}

export default Extractor;
