import React, { useRef, useEffect } from 'react';
import Image from 'next/image';
import FrownIcon from '../../public/frown.svg';

function ErrorMessage() {
  const ref = useRef<HTMLDivElement | null>(null);

  function startAgain() {
    window.location.reload();
  }

  useEffect(() => {
    const wrongFileBox = ref.current;

    // TODO: change this from type any to more explicit type checking
    // if possible
    function preventDefaults(e: any) {
      e.preventDefault();
      e.stopPropagation();
    }

    if (wrongFileBox) {
      wrongFileBox.addEventListener('click', preventDefaults, false);
      wrongFileBox.addEventListener('click', startAgain, false);
    }
  }, []);

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
      <div className="pointer-events-none select-none text-sm">
        Pdf files only. Please try again.
      </div>
    </div>
  );
}

export default ErrorMessage;
