import Head from 'next/head';

const Home: React.FC = () => {
  return (
    <div>
      <Head>
        <title>Welcome to my site</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <main>
        <h1>Welcome</h1>
      </main>
    </div>
  );
};

export default Home;
