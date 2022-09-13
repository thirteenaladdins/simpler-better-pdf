import type { NextPage } from 'next'
import Head from 'next/head'
import Extractor from '../components/Extractor'
import SideBar from '../components/SideBar'

const Home: NextPage = () => {
  return (
    <div className="flex flex-col overflow-hidden ">
      <Head>
        <title>Magic Extractor</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <div className="mx-auto pt-8 font-sans">Magic Extractor V2</div>
      <main className="home-page">
        <SideBar  />
        <Extractor />
      </main>
    </div>
  )
}

export default Home
