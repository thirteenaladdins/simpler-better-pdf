export default {
  env: {
    browser: true,
    es2021: true,
  },
  extends: [
    'plugin:react/recommended',
    'plugin:react-hooks/recommended',
    'plugin:@next/next/recommended',
    'plugin:@typescript-eslint/recommended',
    'airbnb-typescript',
  ],
  overrides: [],
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module',
    parser: '@typescript-eslint/parser',
    project: './nextjs-frontend/tsconfig.json'
  },
  plugins: [
    '@typescript-eslint',
    'react',
    'import'
  ],
  rules: {
    'linebreak-style': 'off',
    'react/jsx-filename-extension': ['error', { extensions: ['.jsx', '.tsx'] }],
  },
};
