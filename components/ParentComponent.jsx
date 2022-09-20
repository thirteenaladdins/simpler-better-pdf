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
    <div className="parent">
      {/* pass the state from passing a callback function -   */}

      {/* pass the setOption function -  */}
      <NavigationBar />
      <SideBar setOption={setOption} />
      <Extractor option={state} />

    </div>
  );
}

export default ParentComponent;
