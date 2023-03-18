module.exports = {
  env: {
    browser: true,
    commonjs: true,
    es2021: true,
  },
  extends: [
    // 'plugin:next/recommended',
    'plugin:react/recommended',
    'airbnb-typescript',
  ],
  parser: '@typescript-eslint/parser',
  overrides: [
  ],
  parserOptions: {
    ecmaVersion: 'latest',
    project: 'tsconfig.json',
  },
  plugins: [
    'react',
    'import',
  ],
  rules: {
    'linebreak-style': 'off',
    // '@typescript-eslint/indent': ['error', 2],
    // 'react/jsx-filename-extension': ['error', { extensions: ['.jsx', '.tsx'] }],
  },
  settings: {
    react: {
      version: 'detect'
    },
  }
};
