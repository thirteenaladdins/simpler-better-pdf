import {
  React, useState,
} from 'react';
import { PropTypes, string } from 'prop-types';
import Image from 'next/image';
import ListView from './ListView';

import DropArea from './DropArea';
import DownloadButton from './DownloadButton';
import ErrorMessage from './ErrorMessage';
import Spinner from '../public/tail-spin.svg';

const initialState = {
  displayComponent: 'default_component',
  selectedFiles: [],
  returnedData: false,
  loading: false,
  downloadFile: false,
  option: '',
};

// TODO: give this some more CSS properties
// center this component
function LoadingView() {
  return (
    <div className="indigo-300">
      <Image
        className="fill-indigo-300"
        src={Spinner}
        priority
        alt="Loading..."
      />
    </div>
  );
}

// TODO: this should be named main component - or something of the sort
function Extractor({ option, errNotif }) {
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
        return <ListView state={currentState} setState={setState} selectedOption={option} />;
      case 'loading_component':
        return <LoadingView state={currentState} setState={setState} />;
      case 'invalid_file_component':
        return <ErrorMessage />;
      case 'default_component':
        return <DropArea state={currentState} setState={setState} errNotif={errNotif} />;
      default:
        return <DropArea state={currentState} setState={setState} />;
    }
  };

  // // for mobile
  // const [windowDimension, setWindowDimension] = useState(null);

  // useEffect(() => {
  //   setWindowDimension(window.innerWidth);
  // }, []);

  // useEffect(() => {
  //   function handleResize() {
  //     setWindowDimension(window.innerWidth);
  //   }

  //   window.addEventListener('resize', handleResize);
  //   return () => window.removeEventListener('resize', handleResize);
  // }, []);

  // // FIXME: make this more responsive
  // // here we've got the flickering issue
  // const isMobile = windowDimension <= 640;

  // ternary operator for mobile view
  // return (
  //   // ternary operator
  //   <div>
  //     {isMobile ? (
  //       <div
  //         className="mobile-container"
  //       >
  //         {renderSwitch(state)}
  //       </div>
  //     ) : (
  //       <div
  //         className="main-container"
  //       >
  //         {renderSwitch(state)}
  //       </div>
  //     )}
  //   </div>
  // );

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
};

export default Extractor;
