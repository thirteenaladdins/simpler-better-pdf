import type { NextPage } from 'next'
import Head from 'next/head'
import Extractor from '../components/Extractor'

const Home: NextPage = () => {
  return (
    <div className="flex flex-col overflow-hidden ">
      <Head>
        <title>Luxury Goods Invoice Extractor</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <div className="mx-auto pt-8 font-sans">Luxury Goods Extractor</div>
      <main className="mx-auto flex flex-1 flex-col justify-center px-10 pt-20">
        <Extractor />
      </main>
    </div>
  )
}

export default Home
