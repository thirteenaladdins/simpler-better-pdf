// Come back to this, ideally when we update the version in Git
// the value should be updated and displayed in the project

const fs = require('fs');
const { execSync } = require('child_process');

// Get the latest git tag
const version = execSync('git describe --tags --abbrev=0').toString().trim();

const content = `export const version = "${version}";\n`;

// Write to version.js
fs.writeFileSync('./src/version.js', content);
