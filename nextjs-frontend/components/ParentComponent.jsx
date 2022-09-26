import { React, useState } from 'react';
import Extractor from './Extractor';
import SideBar from './SideBar';
import NavigationBar from './NavigationBar';
import InfoComponent from './InfoComponent';

function ParentComponent() {
  const [state, setState] = useState('Siemens Regex');
  const [errorNotification, setErrorNotification] = useState('');

  const setOption = (e) => {
    setState(e);
  };

  const getErrorNotification = () => {
    if (errorNotification !== '') {
      return errorNotification;
    }
    return `Selected ${state} to extract`;
  };

  return (
    <div>
      <NavigationBar />
      <SideBar setOption={setOption} />

      <div className="center-container">
        <div>
          {/* <InfoComponent status={state} /> */}
          {/* if errnotif == some error - set to error else - set to state */}
          <InfoComponent status={getErrorNotification()} />
          <Extractor option={state} errNotif={setErrorNotification} />
        </div>
      </div>
    </div>
  );
}

export default ParentComponent;
