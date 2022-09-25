import {
  React, useRef, useEffect, useState,
} from 'react';
import { PropTypes, string } from 'prop-types';
import Image from 'next/image';
import ListView from './ListView';

import DropArea from './DropArea';
import DownloadButton from './DownloadButton';

import FrownIcon from '../public/frown.svg';
import Spinner from '../public/tail-spin.svg';

const initialState = {
  displayComponent: 'default_component',
  selectedFiles: [],
  returnedData: false,
  loading: false,
  downloadFile: false,
  option: '',
};

function WrongFileMessage(props) {
  const ref = useRef(null);

  const { state, setState } = props;

  function startAgain() {
    setState({ ...state, displayComponent: 'default_component' });
  }

  useEffect(() => {
    const wrongFileBox = ref.current;

    function preventDefaults(e) {
      e.preventDefault();
      e.stopPropagation();
      // console.log('Dragged')
    }

    wrongFileBox.addEventListener('click', preventDefaults, false);

    wrongFileBox.addEventListener('click', startAgain, false);

    // remove listeners
  });

  return (
    <div
      ref={ref}
      className="drop-area-full error"
    >
      <Image
        className="pointer-events-none select-none"
        src={FrownIcon}
        priority
        alt="Not a pdf file"
      />
      <div className="pointer-events-none select-none text-sm">
        Pdf files only. Try again.
      </div>
    </div>
  );
}

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

function Extractor({ option }) {
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
        return <WrongFileMessage state={currentState} setState={setState} />;
      case 'default_component':
        return <DropArea state={currentState} setState={setState} />;
      default:
        return <DropArea state={currentState} setState={setState} />;
    }
  };

  // for mobile
  const [windowDimension, setWindowDimension] = useState(null);

  useEffect(() => {
    setWindowDimension(window.innerWidth);
  }, []);

  useEffect(() => {
    function handleResize() {
      setWindowDimension(window.innerWidth);
    }

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  // FIXME: make this more responsive
  const isMobile = windowDimension <= 640;

  return (
    // ternary operator
    <div>
      {isMobile ? (
        <div
          className="mobile-container"
        >
          {renderSwitch(state)}
        </div>
      ) : (
        <div
          className="main-container"
        >
          {renderSwitch(state)}
        </div>
      )}
    </div>
  );
}

// TODO: copilot used - come back and fix this
Extractor.propTypes = {
  option: string.isRequired,
};

WrongFileMessage.propTypes = {
  state: PropTypes.shape({
    displayComponent: PropTypes.string,
    // validFile: PropTypes.bool,
  }).isRequired,
  setState: PropTypes.func.isRequired,
};

export default Extractor;
