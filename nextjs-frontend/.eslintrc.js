module.exports = {
  env: {
    browser: true,
    commonjs: true,
    es2021: true,
  },
  extends: [
    'plugin:@next/next/recommended',
    'plugin:react/recommended',
    'eslint:recommended',
    'airbnb-typescript',
  ],
  parser: '@typescript-eslint/parser',
  overrides: [
  ],
  parserOptions: {
    // ecmaVersion: 'latest',
    project: 'tsconfig.json',
  },
  plugins: [
    'react',
    'react-hooks',
    'import',
    // 'next',
    'jsx-a11y',
  ],
  rules: {
    'linebreak-style': 'off',
    '@typescript-eslint/indent': 'off',
    // 'react/jsx-filename-extension': ['error', { extensions: ['.jsx', '.tsx'] }],
  },
  settings: {
    react: {
      version: 'detect',
    },
  root: true,
  },
};
