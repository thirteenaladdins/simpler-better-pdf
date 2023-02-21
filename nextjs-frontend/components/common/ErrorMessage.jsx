import { React, useRef, useEffect } from 'react';
import { PropTypes } from 'prop-types';
import Image from 'next/image';
import FrownIcon from '../../public/frown.svg';

function ErrorMessage() {
  const ref = useRef(null);

  // const { state, setState } = props;

  function startAgain() {
    // setState({ ...state, displayComponent: 'default_component' });
    window.location.reload(false);
  }

  useEffect(() => {
    const wrongFileBox = ref.current;

    function preventDefaults(e) {
      e.preventDefault();
      e.stopPropagation();
      // console.log('Dragged')
    }

    wrongFileBox.addEventListener('click', preventDefaults, false);

    wrongFileBox.addEventListener('click', startAgain, false);

    // remove listeners
  });

  // TODO: add text beneath the icon - come back to this later
  return (
    <div
      ref={ref}
      className="drop-area-full error"
    >
      <Image
        className="pointer-events-none select-none"
        src={FrownIcon}
        priority
        alt="Not a pdf file"
      />
      {/* <div className="pointer-events-none select-none text-sm">
          Pdf files only. Try again.
        </div> */}
    </div>
  );
}

export default ErrorMessage;

ErrorMessage.propTypes = {
  state: PropTypes.shape({
    displayComponent: PropTypes.string,
    // validFile: PropTypes.bool,
  }).isRequired,
  // setState: PropTypes.func.isRequired,
};
