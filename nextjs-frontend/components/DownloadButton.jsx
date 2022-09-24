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
    <div className="download-component">
      <div className="download-button link">
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
        className="download-button"
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
