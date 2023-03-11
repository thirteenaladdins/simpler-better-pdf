// import React, { useContext } from 'react';
// import PropTypes from 'prop-types';
// import Image from 'next/image';
// import AppContext from '../context/AppContext';

// // import processAllFiles from '../utils/processAllFiles';
// import processAllFiles from '../utils/processAllFiles';
// import ListFiles from '../utils/listFiles';
// import Spinner from '../public/tail-spin.svg';

// const appContext = useContext(AppContext);

// function LoadingView() {
//   return (
//     <div className="indigo-300">
//       <Image
//         className="fill-indigo-300 spinner"
//         src={Spinner}
//         priority
//         alt="Loading..."
//       />
//     </div>
//   );
// }

// export default function ListView({
//   state, setState, selectedOption, hideInfo,
// }) {
//   return (
//     <div className="item-list-view">
//       <div className="item-list-view">
//         <ul className="p-0">
//           {ListFiles(state)}
//         </ul>
//       </div>
//       <div className="extract-button-container">
//         <button
//           type="button"
//           className="extract-button"
//           onClick={async () => {
//             setState({ ...state, loading: true });
//             const processedFiles = await processAllFiles([
//               // eslint-disable-next-line react/prop-types
//               ...state.selectedFiles,
//             ], selectedOption);

//             setState({
//               ...state,
//               displayComponent: 'download_component',
//               returnedData: processedFiles,
//             });

//             hideInfo(true);
//           }}
//         >

//           {/* ternary operator */}
//           {state.loading === true ? <LoadingView /> : 'Extract'}

//         </button>
//       </div>
//     </div>
//   );
// }

// ListView.propTypes = {
//   state: PropTypes.shape({
//     // selectedFiles: PropTypes.arrayOf(PropTypes.instanceOf(File)),
//     displayComponent: PropTypes.string,
//     loading: PropTypes.bool.isRequired,
//     // validFile: PropTypes.bool,
//   }).isRequired,
//   setState: PropTypes.func.isRequired,
//   selectedOption: PropTypes.string.isRequired,
//   hideInfo: PropTypes.func.isRequired,

// };

import React, { useContext } from 'react';
import Image from 'next/image';

import AppContext from '../context/AppContext';
import AppContextProvider from '../context/AppContext';
import processAllFiles from '../utils/processAllFiles';
import ListFiles from '../utils/listFiles';
import Spinner from '../public/tail-spin.svg';


interface ListViewProps {
  state: {
    displayComponent: string,
    loading: boolean,
    selectedFiles: File[]
  },
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
  state, setState, option
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

