import {
  React, useState,
} from 'react';
import { PropTypes, string } from 'prop-types';

import ListView from './ListView';

import DropArea from './DropArea';
import DownloadButton from './DownloadButton';
import ErrorMessage from './ErrorMessage';

const initialState = {
  displayComponent: 'default_component',
  selectedFiles: [],
  returnedData: false,
  loading: false,
  downloadFile: false,
  hideNav: false,
  option: '',
};

// TODO: this should be named main component - or something of the sort
function Extractor({ option, errNotif, hideNav }) {
  const [state, setState] = useState(initialState);

  // setState({ ...state, option });
  // console.log(option);

  // FIXME: methods for rendering state shoud be reworked
  // also looks a bit confusing
  const renderSwitch = (currentState) => {
    switch (currentState.displayComponent) {
      case 'download_component':
        return <DownloadButton data={state.returnedData} />;
      case 'list_component':
        return (
          <ListView
            state={currentState}
            setState={setState}
            selectedOption={option}
          />
        );
      // case 'loading_component':
      //   return <LoadingView state={currentState} setState={setState} />;
      case 'invalid_file_component':
        return <ErrorMessage />;
      case 'default_component':
        return (
          <DropArea
            state={currentState}
            setState={setState}
            errNotif={errNotif}
            hideNav={hideNav}
          />
        );
      default:
        return <DropArea state={currentState} setState={setState} />;
    }
  };

  return (
    <div
      className="main-container"
    >
      {renderSwitch(state)}
    </div>

  );
}

// TODO: copilot used - come back and fix this
Extractor.propTypes = {
  option: string.isRequired,
  errNotif: PropTypes.func.isRequired,
  hideNav: PropTypes.func.isRequired,
};

export default Extractor;
