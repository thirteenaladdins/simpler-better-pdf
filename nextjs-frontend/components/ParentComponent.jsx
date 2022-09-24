import { React, useState } from 'react';
import Extractor from './Extractor';
import SideBar from './SideBar';
import NavigationBar from './NavigationBar';

function ParentComponent() {
  const [state, setState] = useState('Siemens');

  const setOption = (e) => {
    setState(e);
  };

  return (
    <div>
      <NavigationBar />
      <div className="overlay">
        <SideBar setOption={setOption} />
      </div>
      <div className="center-container">
        <div>
          <Extractor option={state} />
        </div>
      </div>
    </div>
  );
}

export default ParentComponent;
