/** @type {import('next').NextConfig} */

const path = require('path');

module.exports = {
  reactStrictMode: true,
  experimental: {
    images: {
      layoutRaw: true,
    },
  },
  sassOptions: {
    includePaths: [path.join(__dirname, 'styles')],
  },
  // extends: [
  //   // ...
  //   'plugin:@next/next/recommended',
  // ],
};
