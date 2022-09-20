// import type { NextPage } from 'next';
import Head from 'next/head';
import React from 'react';
import ParentComponent from '../components/ParentComponent';

function Home() {
  return (
    <div className="flex flex-col overflow-hidden ">
      <Head>
        <title>Magic Extractor V2</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>
      {/* <div className="mx-auto pt-8 font-sans">Magic Extractor V2</div> */}
      <main className="home-page">
        <ParentComponent />

      </main>
    </div>
  );
}

export default Home;
