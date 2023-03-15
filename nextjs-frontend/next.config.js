/** @type {import('next').NextConfig} */

const path = require('path');
require('dotenv').config();

module.exports = {
  async redirects() {
    return [
      {
        source: '/',
        destination: '/home',
        permanent: true,
      },
    ];
  },
  reactStrictMode: true,
  // experimental: {
  //   images: {
  //     layoutRaw: true,
  //     allowFutureImage: true,
  //   },
  // },
  // experimental: {
  //   outputStandalone: true,
  // },
  output: 'standalone',
  sassOptions: {
    includePaths: [path.join(__dirname, 'styles')],
  },
  // env: {
  //   ENV_URL: 'http://localhost:8080',
  // },
};
