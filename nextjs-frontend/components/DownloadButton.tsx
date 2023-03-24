import React from 'react';

interface DownloadButtonProps {
  data: Blob | string;
  fileType: string;
  fileName: string;
}

export default function DownloadButton(props: DownloadButtonProps) {
  function refreshPage() {
    // reload?
    window.location.reload();
  }

  const { data, fileType, fileName } = props;

  // Generate download URL using a Blob
  const downloadURL = () => {
    const downloadBlob = data instanceof Blob ? data : new Blob([data], { type: fileType });
    return URL.createObjectURL(downloadBlob);
  };

  return (
    <div className="download-component">
      <a
        download={fileName}
        href={downloadURL()}
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

// <div className="download-component">
{/* <a
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
</button> */}