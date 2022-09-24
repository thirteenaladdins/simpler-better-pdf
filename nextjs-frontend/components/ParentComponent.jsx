import { React, useState } from 'react';
import Extractor from './Extractor';
import SideBar from './SideBar';
import NavigationBar from './NavigationBar';
import InfoComponent from './InfoComponent';

function ParentComponent() {
  const [state, setState] = useState('Siemens Regex');

  const setOption = (e) => {
    setState(e);
  };

  return (
    <div>
      <NavigationBar />

      <SideBar setOption={setOption} />

      <div className="center-container">
        <div>
          <InfoComponent status={state} />
          <Extractor option={state} />
        </div>
      </div>
    </div>
  );
}

export default ParentComponent;
