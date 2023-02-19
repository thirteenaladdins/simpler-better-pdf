import '../styles/globals.css';
import '../styles/sidebar.css';
import '../styles/download.css';
import '../styles/listview.css';
import '../styles/infocomponent.css';
import '../styles/404.css';

import React from 'react';
import type { AppProps } from 'next/app';

function MyApp({ Component, pageProps }: AppProps) {
  return <Component {...pageProps} />;
}

export default MyApp;
