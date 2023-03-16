import React, { useRef } from 'react';
import Image from 'next/image';
import DownloadIcon from '../public/download.svg';
import { ExtractorState } from './Extractor';

// interface Props {
//   state: {
//     selectedFiles: File[] | null;
//     displayComponent: string;
//   };
//   setState: React.Dispatch<React.SetStateAction<{
//     selectedFiles: File[] | null;
//     displayComponent: string;
//   }>>;
//   errNotif: (arg: string | number) => void;
//   // hideNav: (arg: boolean) => void;
// }

interface Props {
  state: ExtractorState;
  setState: React.Dispatch<React.SetStateAction<ExtractorState>>;
  // errNotif: (arg: string | number) => void;
  // hideNav: (arg: boolean) => void;
}

// type DropAreaProps = {
//   state: ExtractorState;
//   setState: React.Dispatch<React.SetStateAction<{ selectedFiles: File[] | null; displayComponent: string; }>>;
// };

const count = 50;
const formats = ['pdf'];

function DropArea(props: Props): JSX.Element {
  const ref = useRef<HTMLDivElement>(null);
  const inputFile = useRef<HTMLInputElement>(null);

  const {
    state, setState,
  } = props;

  const dropArea = ref.current;

  function handleDrop(e: DragEvent): File[] | null {
    e.preventDefault();
    const files: FileList | null = e.dataTransfer?.files ?? null;

    const fileList: File[] = [];
    if (files) {
      fileList.push(...Array.from(files));
    }

    if (count && files && count < files.length) {
      setState({ ...state, displayComponent: 'invalid_file_component' });

      // TODO: reimplement this using a notification function defined elsewhere.
      // errNotif(`Only ${count} file${count !== 1 ? 's' : ''} can be uploaded at a time`);
      return null;
    }

    if (
      formats
      && fileList.some(
        (file) => !formats.some((format) => file.name
          .toLowerCase().endsWith(format.toLowerCase())),
      )
    ) {
      setState({ ...state, displayComponent: 'invalid_file_component' });

      // TODO: reimplement this using a notification function defined elsewhere.
      // errNotif(`Only the following file formats are acceptable: ${formats.join(', ')}`);
      return null;
    }

    return fileList;
  }

  function preventDefaults(e: Event) {
    e.preventDefault();
    e.stopPropagation();
  }

  function highlight() {
    dropArea?.classList.add('bg-indigo-300');
  }

  function unhighlight() {
    dropArea?.classList.remove('bg-indigo-300');
  }

  ['dragenter', 'dragover', 'dragleave', 'drop'].forEach((eventName) => {
    dropArea?.addEventListener(eventName, (e: Event) => preventDefaults(e as DragEvent), false);
  });

  dropArea?.addEventListener('drop', (e: Event) => handleDrop(e as DragEvent), false);

  ['dragenter', 'dragover'].forEach((eventName) => {
    dropArea?.addEventListener(eventName, highlight, false);
  });

  ['dragleave', 'drop'].forEach((eventName) => {
    dropArea?.addEventListener(eventName, unhighlight, false);
  });

  const onClickHandler = () => {
    inputFile.current?.click();
  };

  const onKeyDownHandler = (e: React.KeyboardEvent<HTMLDivElement>) => {
    if (e.key === 'Enter') {
      inputFile.current?.click();
    }
  };

  const handleFiles = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { files } = e.target;
    if (files) {
      const fileList = [...files];
      setState({
        ...state,
        selectedFiles: fileList,
        displayComponent: 'list_component',
      });
    }
    return files;
  };

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
        onChange={handleFiles}
      />
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
  );
}
export default DropArea;
