import { React, useState } from 'react';
import Extractor from './Extractor';
import SideBar from './SideBar';

function ParentComponent() {
  const [state, setState] = useState('Siemens');

  const setOption = (e) => {
    setState(e);
  };

  return (
    <div>
      {/* pass the state from passing a callback function -   */}

      {/* pass the setOption function -  */}
      <SideBar setOption={setOption} />
      <Extractor option={state} />

    </div>
  );
}

export default ParentComponent;
