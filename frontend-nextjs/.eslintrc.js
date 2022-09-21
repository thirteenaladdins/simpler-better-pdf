module.exports = {
  env: {
    browser: true,
    es2021: true,
  },
  extends: [
    'plugin:react/recommended',
    'plugin:react-hooks/recommended',
    // "standard-with-typescript",
    'airbnb',
  ],
  overrides: [
  ],
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module',
  },
  plugins: [
    'react',
  ],
  rules: {
    // 'linebreak-style': ['error', (process.platform === 'win32' ? 'windows' : 'unix')]
    'linebreak-style': ['error', 'windows'],
  },
};
