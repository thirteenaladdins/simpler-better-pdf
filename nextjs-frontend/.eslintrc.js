module.exports = {
  env: {
    browser: true,
    es2021: true,
  },
  extends: [
    'plugin:react/recommended',
    'plugin:react-hooks/recommended',
    'plugin:@next/next/recommended',
    'plugin:@typescript-eslint/recommended',
    // 'plugin:prettier/recommended',
    'airbnb',
  ],
  overrides: [
  ],
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module',
    parser: '@typescript-eslint/parser',
  },
  plugins: [
    '@typescript-eslint',
    'react',
  ],
  rules: {
    // 'linebreak-style': ['error', (process.platform === 'win32' ? 'windows' : 'unix')]
    // 'linebreak-style': ['error', 'windows'],
    'linebreak-style': 'off',
  },
};
