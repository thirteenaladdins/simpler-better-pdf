import React from 'react';
import Image from 'next/image';

// import AppContext from '../context/AppContext';
// import AppContextProvider from '../context/AppContext';
import processAllFiles from '../utils/processAllFiles';
import ListFiles from '../utils/listFiles';
import Spinner from '../public/tail-spin.svg';

interface ListViewProps {
  state: {
    displayComponent: string,
    loading: boolean,
    selectedFiles: File[]
  },
  // TODO: come back and change this
  setState: (state: any) => void,
  option: string,
  // hideInfo: (arg0: boolean) => void
}

function LoadingView() {
  return (
    <div className="indigo-300">
      <Image
        className="fill-indigo-300 spinner"
        src={Spinner}
        priority
        alt="Loading..."
      />
    </div>
  );
}

// const {
//   option,
//   setOption
// } = useContext(AppContext);

export default function ListView({
  state, setState, option,
}: ListViewProps) {
  return (
    // <AppContextProvider value={{ setOption, option }}>
    <div className="item-list-view">
      <div className="item-list-view">
        <ul className="p-0">
          {ListFiles(state)}
        </ul>
      </div>
      <div className="extract-button-container">
        <button
          type="button"
          className="extract-button"
          onClick={async () => {
            setState({ ...state, loading: true });
            const processedFiles = await processAllFiles([
              // eslint-disable-next-line react/prop-types
              ...state.selectedFiles,
            ], option);
            setState({
              ...state,
              displayComponent: 'download_component',
              returnedData: processedFiles,
              // put the file type
              // and file name here.
              // fileType: '',
              // fileName: '',
            });

            // hideInfo(true);
          }}
        >
          {/* ternary operator */}
          {state.loading === true ? <LoadingView /> : 'Extract'}
        </button>
      </div>
    </div>
    // </AppContextProvider >
  );
}
