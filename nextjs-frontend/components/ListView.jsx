import React from 'react';
import PropTypes from 'prop-types';
import processAllFiles from '../utils/processAllFiles';
import ListFiles from '../utils/listFiles';

export default function ListView(props) {
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
          className="extract-button"
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

ListView.propTypes = {
  state: PropTypes.shape({
    // selectedFiles: PropTypes.arrayOf(PropTypes.instanceOf(File)),
    displayComponent: PropTypes.string,
    // validFile: PropTypes.bool,
  }).isRequired,
  setState: PropTypes.func.isRequired,
  selectedOption: PropTypes.string.isRequired,
};
