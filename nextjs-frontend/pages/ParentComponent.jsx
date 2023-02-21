import { React, useState } from 'react';
import Extractor from '../components/Extractor';
import SideBar from '../components/SideBar';
import NavigationBar from '../components/NavigationBar';
import InfoComponent from '../components/InfoComponent';

function ParentComponent() {
  const [state, setState] = useState('Siemens Regex');
  const [errorNotification, setErrorNotification] = useState('');
  const [hideNav, setHideNav] = useState(false);
  const [hideInfo, setHideInfo] = useState(false);

  const setOption = (e) => {
    setState(e);
  };

  // display info message / error message

  // `Selected ${errorNotification} file${errorNotification !== 1 ? 's' : ''} to extract`)
  const displayErrorNotification = () => {
    if (typeof (errorNotification) === 'number') {
      return `Selected ${errorNotification} file${errorNotification !== 1 ? 's' : ''} to extract`;
    }

    if (errorNotification !== '') {
      return errorNotification;
    }

    return `Selected ${state} to extract`;
  };

  const getHideNav = (e) => {
    setHideNav(e);
  };

  const getHideInfo = (e) => {
    setHideInfo(e);
  };

  return (
    <div>
      <NavigationBar />
      <SideBar hideNav={hideNav} setOption={setOption} />
      <div className="center-container">
        <div>
          {/* set the number of files selected up top */}
          {/* count number of api calls at the top - count at the top */}
          <InfoComponent
            hideNav={hideInfo}
            hideInfo={hideInfo}
            status={displayErrorNotification()}
          />
          <Extractor
            option={state}
            hideNav={getHideNav}
            // change name of the prop
            errNotif={setErrorNotification}
            hideInfo={getHideInfo}
            // count={setErrorNotification}
          />
        </div>
      </div>
    </div>
  );
}

export default ParentComponent;
