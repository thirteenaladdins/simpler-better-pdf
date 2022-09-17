import {
  React, useRef, useEffect, useState,
} from 'react';
// import { useFilePicker } from 'use-file-picker';
import Image from 'next/image';
import axios from 'axios';
import ListItem from './ListItem';
import DownloadButton from './DownloadButton';
import DownloadIcon from '../public/download.svg';
import FrownIcon from '../public/frown.svg';
import Spinner from '../public/tail-spin.svg';

// const { Parser } = require('json2csv');

// come back and sort out all the design

const initialState = {
  displayComponent: null,
  selectedFile: 'default_component',
  returnedData: false,
  loading: false,
  downloadFile: false,
  // option: 'Siemens',
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

      // Add this count to the screen
      if (count && count < files.length) {
        console.log(
          `Only ${count} file${count !== 1 ? 's' : ''} can be uploaded at a time`,
        );
        return;
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
        return;
      }

      setState({
        ...state,
        selectedFile: files,
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
  }, []);

  function handleFiles(e) {
    console.log(e);
    // let files = e.files
    const files = [...e];
    setState({
      ...state,
      selectedFile: files,
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
  const handleResize = () => {
    if (window.innerWidth < 640) {
      // setState({ ...state, width: '100%' })
    } else {
      // setState({ ...state, width: '50%' })
    }
  };

  return (
    <div
      ref={ref}
      className="drop-area-full"
      onClick={onClickHandler}
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

// TODO: what difference does this make?

const parseJsonData = (jsonData) => {
  try {
    console.log(jsonData);
    const replacer = (key, value) => (value === null ? '' : value); // specify how you want to handle null values here
    const headers = Object.keys(jsonData[0]);
    // console.log(headers)

    let csv = jsonData.map((row) => headers
      .map((fieldName) => JSON.stringify(row[fieldName], replacer))
      .join(','));
    csv.unshift(headers);
    csv = csv.join('\r\n');
    // console.log(csv)
    return csv;
  } catch {
    // add file name here?
    // TODO - add error message to screen
    console.log('Something went wrong with a file.');
  }

  // return <Download fileName={filename} csv={csv} />
};

function Extractor(props) {
  const [state, setState] = useState(initialState);

  const { option } = props;
  // setState({ ...state, option });
  // console.log(option);

  const uploadFile = async (file) => {
    const url = 'http://localhost:8080/api/processfile';
    // for production
    // const url = 'https://luxury-goods-backend.herokuapp.com/api/processfile';
    // eslint-disable-next-line no-undef
    const formData = new FormData();

    formData.append('file', file);
    formData.append('option', option);

    const response = await axios.post(url, formData, {
      headers: {
        'Access-Control-Allow-Origin': '*',
      },
    });
    // .catch((err) => {
    //   if (err.response.status === 500) {
    //     console.log('Something went wrong')
    //   }
    // })

    return response;
  };

  // instead of dealing with json we're using json array
  const processAllFiles = async (files) => {
    const responses = [];

    // files.map(async (file) => {
    //   try {
    //     const responseData = await uploadFile(file).catch((err) => console.log(err));
    //     responses.push(responseData);
    //   } catch {
    //     // console.log('Something went wrong');
    //     (error) => {
    //       if (error.response.status === 500) {
    //         console.log(err);
    //         return error;
    //       }
    //     };
    //   }
    // });

    // TODO: does this need to be fixed?
    for (const file of files) {
      try {
        const responseData = await uploadFile(file).catch((err) => {});
        responses.push(responseData.data);
      } catch {
        (error) => {
          if (error.response.status === 500) {
            console.log(err);
            return error;
          }
        };
      }
    }

    const combinedResponses = [...responses][0];
    const csvFormattedData = parseJsonData(combinedResponses);

    return csvFormattedData;
  };

  // FIXME: methods for rendering state shoud be reworked
  // also looks a bit confusing
  const renderSwitch = (currentState) => {
    switch (currentState.displayComponent) {
      case 'download_component':
        return <DownloadButton data={state.returnedData} />;
      case 'list_component':
        return <ListView state={currentState} setState={setState} />;
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

  // const DropSwitcher = () => {
  //   return state.validFile ? <DropArea /> : <WrongFileMessage />
  // }

  // I want this to last for a couple of seconds
  // and should it be ternary operator?

  function ListView() {
    return (
      <div className="flex w-64 flex-col items-center rounded-lg shadow">
        <div className="scrollbar overflow-auto border border-2">
          <ul className="p-0">
            {[...state.selectedFile].map((file, index) => (
              // here we should import the custom style component
              <ListItem key={index} fileName={file.name} />
            ))}
          </ul>
        </div>
        <div>
          <button
            className="bottom-0 mt-auto rounded border-none
              bg-indigo-500 py-2 px-4 font-bold
              text-white hover:bg-indigo-300"
            onClick={async () => {
              setState({ ...state, displayComponent: 'loading_component' });
              const processFiles = await processAllFiles([
                ...state.selectedFile,
              ]);
              setState({
                ...state,
                displayComponent: 'download_component',
                returnedData: processFiles,
              });
            }}
          >
            Extract
          </button>
        </div>
      </div>
    );
  }

  //   for mobile
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
          className="main-container flex
          h-72 w-full justify-center
          break-normal font-sans"
        >
          {renderSwitch(state)}
        </div>
      )}
    </div>
  );
}

export default Extractor;
