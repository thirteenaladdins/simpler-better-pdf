import React from 'react';
import PropTypes from 'prop-types';

// TODO: use a state management library instead of
// passing props down the component tree
function InfoComponent({ status, hideInfo }) {
  return (
    <div className={hideInfo === true ? 'info-hidden' : 'info-component'}>
      <span>
        {status}
      </span>
    </div>
  );
}

export default InfoComponent;

InfoComponent.propTypes = {
  status: PropTypes.string.isRequired,
  hideInfo: PropTypes.func.isRequired,
};
