import React from 'react';
import PropTypes from 'prop-types';

// TODO: use button component?

export default function DownloadButton(props) {
  function refreshPage() {
    window.location.reload(false);
  }

  // TODO: ESLINT ME
  const { data } = props;

  return (
    <div className="w-64 items-center shadow">
      <div className="download-button">
        <a
            // tabIndex="0"
          className="mb-4 mt-4 box-border inline-block rounded bg-indigo-500
            px-4 text-center text-sm
            font-normal uppercase leading-5 text-white
            no-underline hover:bg-indigo-300 "
            // generate name file
          download="export.csv"
            // here we're passing the json data returned from the function
            // encode uri component
          href={
              `data:text/csv;charset=utf-8,%EF%BB%BF${
                encodeURIComponent(data)}`
            }
        >
          {/* <img src={DownloadIcon} className="download-icon" /> */}
          <i className="fas fa-arrow-down" />
          {' '}
          Download
        </a>
      </div>

      {/* instead of resetting page - refresh */}
      <button
        type="submit"
        className="refresh-button"
        onClick={refreshPage}
      >
        Convert another?
      </button>
    </div>
  );
}

// DownloadButton.propTypes = {
//   data: PropTypes.string.isRequired,
// };
