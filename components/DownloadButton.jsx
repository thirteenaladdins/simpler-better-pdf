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
      <div className="basic-button">
        <a
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
        className="basic-button"
        onClick={refreshPage}
      >
        Convert another?
      </button>
    </div>
  );
}

DownloadButton.propTypes = {
  data: PropTypes.string.isRequired,
};
