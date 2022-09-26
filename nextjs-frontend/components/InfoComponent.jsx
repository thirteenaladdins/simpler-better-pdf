import React from 'react';
import PropTypes from 'prop-types';

// if nothing selected
function InfoComponent({ status }) {
  return (
    <div className="info-component">
      <span>
        {status}
      </span>
    </div>
  );
}

export default InfoComponent;

InfoComponent.propTypes = {
  status: PropTypes.string.isRequired,
};
