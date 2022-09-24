import React from 'react';
import { string } from 'prop-types';

function CustomButton(props) {
  const { text } = props;
  return <div>{text}</div>;
}

export default CustomButton;

CustomButton.propTypes = {
  text: string.isRequired,
};
