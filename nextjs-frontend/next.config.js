/** @type {import('next').NextConfig} */

const path = require('path');
require('dotenv').config();

module.exports = {
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
