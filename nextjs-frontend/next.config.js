/** @type {import('next').NextConfig} */

const path = require('path');

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
};
