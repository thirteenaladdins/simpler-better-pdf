import {
  React, useRef, useEffect,
} from 'react';
import { PropTypes } from 'prop-types';
import Image from 'next/image';
import DownloadIcon from '../public/download.svg';

const count = 50;
const formats = ['pdf'];

// TODO: add limit to the normal file selection
function DropArea(props) {
  const ref = useRef(null);
  const inputFile = useRef(null);

  const {
    state, setState, errNotif, hideNav,
  } = props;

  //   set the state with the new message
  //   display it at the top of the screen
  useEffect(() => {
    const dropArea = ref.current;

    function handleDrop(e) {
      const { files } = e.dataTransfer;
      const fileList = [...e.dataTransfer.files];

      // TODO: Add this count to the screen
      if (count && count < files.length) {
        // console.log(
        //   `Only ${count} file${count !== 1 ? 's' : ''} can be uploaded at a time`,
        // );
        setState({ ...state, displayComponent: 'invalid_file_component' });
        errNotif(`Only ${count} file${count !== 1 ? 's' : ''} can be uploaded at a time`);
        return null;
      }

      if (
        formats
          && fileList.some(
            (file) => !formats.some((format) => file.name
              .toLowerCase().endsWith(format.toLowerCase())),
          )
      ) {
        // console.log(
        //   `Only the following file formats are acceptable: ${formats.join(', ')}`,
        // );
        setState({ ...state, displayComponent: 'invalid_file_component' });
        errNotif(`Only the following file formats are acceptable: ${formats.join(', ')}`);
        return null;
      }

      setState({
        ...state,
        selectedFiles: files,
        displayComponent: 'list_component',
      });
      hideNav(true);
      // TODO: return number of files to display on screen
      // setting the error notification here doesn't work
      // stringify
      // errNotif(files.length.toString());
      errNotif(files.length.toString());
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
  }, [setState, state, errNotif, hideNav]);

  function handleFiles(e) {
    // let files = e.files
    const files = [...e];
    setState({
      ...state,
      selectedFiles: files,
      displayComponent: 'list_component',
    });
    hideNav(true);
    errNotif(files.length.toString());
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
        />
        <div className="pointer-events-none select-none text-sm">
          Click to choose a file or drag it here
        </div>
      </div>
    </div>
  );
}

export default DropArea;

DropArea.propTypes = {
  state: PropTypes.shape({
    // selectedFiles: PropTypes.arrayOf(PropTypes.instanceOf(File)),
    displayComponent: PropTypes.string.isRequired,
    // validFile: PropTypes.bool.isRequired,
  }),
  setState: PropTypes.func.isRequired,
  errNotif: PropTypes.func.isRequired,
  hideNav: PropTypes.func.isRequired,
};

DropArea.defaultProps = {
  state: PropTypes.shape({
    selectedFiles: [],
  }),
};
