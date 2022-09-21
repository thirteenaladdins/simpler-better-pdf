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
      {/* pass the state from passing a callback function -   */}

      {/* pass the setOption function -  */}
      <NavigationBar />

      <div className="parent">
        <div className="column-one">
          <SideBar setOption={setOption} />
        </div>
        <div className="column-two">
          <Extractor option={state} />
        </div>
        {/* <div id="three" /> */}

      </div>
    </div>
  );
}

export default ParentComponent;
