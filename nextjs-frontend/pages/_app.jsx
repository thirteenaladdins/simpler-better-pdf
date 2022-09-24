// TODO: come back and convert back to TypeScript
import '../styles/globals.css';
import React from 'react';
// import type { AppProps } from 'next/app'

// eslint-disable-next-line react/prop-types
function MyApp({ Component, pageProps }) {
  // eslint-disable-next-line react/jsx-props-no-spreading
  return <Component {...pageProps} />;
}

export default MyApp;
