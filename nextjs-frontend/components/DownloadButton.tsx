import React from 'react';

interface DownloadButtonProps {
  data: string;
}

export default function DownloadButton(props: DownloadButtonProps) {
  function refreshPage() {
    // reload?
    window.location.reload();
  }

  const { data } = props;

  return (
    <div className="download-component">
      <a
        download="export.csv"
        href={`data:text/csv;charset=utf-8,%EF%BB%BF${encodeURIComponent(data)}`}
        className="download-button-link"
      >
        <div className="download-button">
          Download
        </div>
      </a>

      <button
        type="submit"
        className="convert-button"
        onClick={refreshPage}
      >
        Convert another?
      </button>
    </div>
  );
}
