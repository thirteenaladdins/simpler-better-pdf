import React from 'react';

interface InfoComponentProps {
  status: string;
  hideInfo: boolean;
}

function InfoComponent({ status, hideInfo }: InfoComponentProps) {
  return (
    <div className={hideInfo === true ? 'info-hidden' : 'info-component'}>
      <span>
        {status}
      </span>
    </div>
  );
}

export default InfoComponent;
