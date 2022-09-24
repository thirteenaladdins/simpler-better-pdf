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
      <div className="parent">
        <SideBar setOption={setOption} />
        {/* <div className="column-one">
        </div> */}
        <div>
          <Extractor option={state} />
        </div>
      </div>
    </div>
  );
}

export default ParentComponent;
