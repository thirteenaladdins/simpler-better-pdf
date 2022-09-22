import {
  React, useRef, useEffect, useState,
} from 'react';
import { PropTypes, string } from 'prop-types';
import Image from 'next/future/image';
import uploadFile from '../pages/api/uploadFile';

import ListItem from './ListItem';
import DownloadButton from './DownloadButton';
import DownloadIcon from '../public/download.svg';
import FrownIcon from '../public/frown.svg';
import Spinner from '../public/tail-spin.svg';
import parseJsonData from '../utils/parseJsonData';

const initialState = {
  displayComponent: 'default_component',
  selectedFiles: [],
  returnedData: false,
  loading: false,
  downloadFile: false,
  option: 'Siemens',
};

const count = 50;
const formats = ['pdf'];

function DropArea(props) {
  const ref = useRef(null);
  const inputFile = useRef(null);

  const { state, setState } = props;

  useEffect(() => {
    const dropArea = ref.current;

    function handleDrop(e) {
      const { files } = e.dataTransfer;
      const fileList = [...e.dataTransfer.files];

      // TODO: Add this count to the screen
      if (count && count < files.length) {
        console.log(
          `Only ${count} file${count !== 1 ? 's' : ''} can be uploaded at a time`,
        );
        return (
          <div>
            {' '}
            `Only $
            {count}
            {' '}
            file$
            {count !== 1 ? 's' : ''}
            {' '}
            can be uploaded at a time`
          </div>
        );
      }

      if (
        formats
        && fileList.some(
          (file) => !formats.some((format) => file.name
            .toLowerCase().endsWith(format.toLowerCase())),
        )
      ) {
        console.log(
          `Only the following file formats are acceptable: ${formats.join(', ')}`,
        );
        setState({ ...state, displayComponent: 'invalid_file_component' });
        return null;
      }

      setState({
        ...state,
        selectedFiles: files,
        displayComponent: 'list_component',
      });
      return files;
    }

    function preventDefaults(e) {
      e.preventDefault();
      e.stopPropagation();
      // console.log('Dragged')
    }
    // I want to add this class to the drop area only
    function highlight() {
      dropArea.classList.add('bg-indigo-300');
    }

    function unhighlight() {
      dropArea.classList.remove('bg-indigo-300');
    }

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach((eventName) => {
      dropArea.addEventListener(eventName, preventDefaults, false);
    });

    dropArea.addEventListener('drop', handleDrop, false);
    ['dragenter', 'dragover'].forEach((eventName) => {
      dropArea.addEventListener(eventName, highlight, false);
    });
    ['dragleave', 'drop'].forEach((eventName) => {
      dropArea.addEventListener(eventName, unhighlight, false);
    });

    // dropArea.addEventListener('click', chooseFiles, false)

    // function chooseFiles() {
    //   ref.current.click()
    // }

    // const onChangeFile = (event) => {
    //   event.stopPropagation()
    //   event.preventDefault()
    //   var file = event.target.files[0]
    //   console.log(file)
    //   // this.setState({ file }) /// if you want to upload latter
    // }

    // what does this mean and how does it work?
    // TODO: when should I remove listener?
    return () => {
      // dropArea.removeEventListener('dragenter', handleDrag)
      // dropArea.removeEventListener('dragleave', handleDrag)
      // dropArea.removeEventListener('dragover', handleDrag)
      // dropArea.removeEventListener('drop', handleDrag)
      dropArea.removeEventListener('drop', handleDrop, false);
    };
  }, [setState, state]);

  function handleFiles(e) {
    // let files = e.files
    const files = [...e];
    setState({
      ...state,
      selectedFiles: files,
      displayComponent: 'list_component',
    });
    return files;
  }

  // const [files, errors, openFileSelector] = useFilePicker({
  //   multiple: true,
  //   accept: '.ics,.pdf',
  // })

  const onClickHandler = () => {
    inputFile.current.click();
    // handleDrop(e)
  };

  // responsive window width - if it's less than 640px change width
  // const handleResize = () => {
  //   if (window.innerWidth < 640) {
  //     // setState({ ...state, width: '100%' })
  //   } else {
  //     // setState({ ...state, width: '50%' })
  //   }
  // };

  function onKeyDownHandler(e) {
    if (e.key === 'Enter') {
      inputFile.current.click();
    }
  }

  return (
    <div
      ref={ref}
      className="drop-area-full"
      onClick={onClickHandler}
      role="button"
      tabIndex={0}
      onKeyPress={onKeyDownHandler}
    >
      <input
        multiple
        type="file"
        id="file"
        ref={inputFile}
        accept="application/pdf"
        style={{ display: 'none' }}
        onChange={(e) => handleFiles(e.target.files)}
      />

      <div>
        <Image
          className="pointer-events-none select-none"
          src={DownloadIcon}
          priority
          alt="Drop your files here"
          layout="raw"
        />
        <div className="pointer-events-none select-none text-sm">
          Click to choose a file or drag it here
        </div>
      </div>
    </div>
  );
}

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
      className="drop-area flex w-8/12
      cursor-pointer flex-col items-center justify-center break-normal
      border-2 border-dashed border-red-300 bg-red-300
      text-center font-sans"
    >
      <Image
        className="pointer-events-none select-none"
        src={FrownIcon}
        priority
        alt="Not a pdf file"
        layout="raw"
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

// instead of dealing with json we're using json array
// const processAllFiles = async (files, option) => {
//   const responses = [];

//   // TODO:
//   // I'm sure I had to do this because I could only process
//   // one file at a time
//   // Likely need to support multiple requests on the backend -

//   // eslint-disable-next-line no-restricted-syntax
//   for (const file of files) {
//     try {
//       // eslint-disable-next-line no-await-in-loop
//       const responseData = await uploadFile(file, option);
//       responses.push(responseData.data);
//       // FIXME: add proper error handling
//     } catch {
//       console.log('Error');
//     }
//   }

//   console.log(responses);

//   // do i really need to spread the responses here?

//   console.log(combinedResponses);
//   const csvFormattedData = parseJsonData(combinedResponses);

//   return csvFormattedData;
// };

const processAllFiles = async (files, option) => {
  const responses = [];

  // eslint-disable-next-line no-restricted-syntax
  for (const file of files) {
    try {
      // eslint-disable-next-line no-await-in-loop
      const responseData = await uploadFile(file, option);
      responses.push(responseData.data);
    } catch {
      // FIXME: add proper error handling
      console.log('Error - something went wrong a file');
    }
  }

  // spread doesn't work for this line
  // eslint-disable-next-line prefer-spread
  const combinedResponses = [].concat.apply([], responses);
  // const combinedResponses = [...responses];

  // setState({ ...state, returnedData: true })
  const csvFormattedData = parseJsonData(combinedResponses);
  // console.log(csvFormattedData)
  return csvFormattedData;
};

function ListFiles(state) {
  const items = [...state.selectedFiles].map((file) => (
    // FIXME: it's unlikely that the user will have the same file twice
    // but should I change this just in case?
    <ListItem key={file.name} fileName={file.name} />
  ));
  return items;
}

function ListView(props) {
  const { state, setState, selectedOption } = props;

  return (
    <div className="flex w-64 flex-col items-center rounded-lg shadow">
      <div className="scrollbar overflow-auto border border-2">
        <ul className="p-0">
          {ListFiles(state)}
        </ul>
      </div>
      <div>
        <button
          type="button"
          className="bottom-0 mt-auto rounded border-none
            bg-indigo-500 py-2 px-4 font-bold
            text-white hover:bg-indigo-300"
          onClick={async () => {
            setState({ ...state, displayComponent: 'loading_component' });
            const processedFiles = await processAllFiles([
              // eslint-disable-next-line react/prop-types
              ...state.selectedFiles,
            ], selectedOption);

            setState({
              ...state,
              displayComponent: 'download_component',
              returnedData: processedFiles,
            });
          }}
        >
          Extract
        </button>
      </div>
    </div>
  );
}

function Extractor(props) {
  const [state, setState] = useState(initialState);

  const { option } = props;
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

  const isMobile = windowDimension <= 640;

  return (
    // ternary operator
    <div>
      {isMobile ? (
        <div
          className="mobile-container
        flex h-72 items-center justify-center font-sans"
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

DropArea.propTypes = {
  state: PropTypes.shape({
    // selectedFiles: PropTypes.arrayOf(PropTypes.instanceOf(File)),
    displayComponent: PropTypes.string.isRequired,
    validFile: PropTypes.bool.isRequired,
  }),

  setState: PropTypes.func.isRequired,
};

DropArea.defaultProps = {
  state: PropTypes.shape({
    selectedFiles: [],
  }),
};

ListView.propTypes = {
  state: PropTypes.shape({
    // selectedFiles: PropTypes.arrayOf(PropTypes.instanceOf(File)),
    displayComponent: PropTypes.string,
    validFile: PropTypes.bool,
  }).isRequired,
  setState: PropTypes.func.isRequired,
  selectedOption: PropTypes.string.isRequired,
};

WrongFileMessage.propTypes = {
  state: PropTypes.shape({
    displayComponent: PropTypes.string,
    validFile: PropTypes.bool,
  }).isRequired,
  setState: PropTypes.func.isRequired,
};

export default Extractor;
