const fs = require('fs');
const packageJson = require('./package.json');

// Update these mappings based on the warnings you received
const replacementMap = {
  "@babel/plugin-proposal-async-generator-functions": "@babel/plugin-transform-async-generator-functions",
  "@babel/plugin-proposal-optional-catch-binding": "@babel/plugin-transform-optional-catch-binding",
  "@hapi/joi": "joi",
  "uuid": "^9.0.0",
  "core-js": "^3.30.0",
  "fsevents": "^2.3.2",
  "@babel/plugin-proposal-object-rest-spread": "@babel/plugin-transform-object-rest-spread",
  "@babel/plugin-proposal-dynamic-import": "@babel/plugin-transform-dynamic-import"
};

// Safely update dependencies
if (packageJson.dependencies) {
  Object.keys(packageJson.dependencies).forEach(dep => {
    if (replacementMap[dep]) {
      console.log(`Updating dependency: ${dep} → ${replacementMap[dep]}`);
      packageJson.dependencies[dep] = replacementMap[dep];
    }
  });
}

// Safely update devDependencies
if (packageJson.devDependencies) {
  Object.keys(packageJson.devDependencies).forEach(dep => {
    if (replacementMap[dep]) {
      console.log(`Updating devDependency: ${dep} → ${replacementMap[dep]}`);
      packageJson.devDependencies[dep] = replacementMap[dep];
    }
  });
}

// Add react-scripts update if it exists
if (packageJson.dependencies?.['react-scripts'] || packageJson.devDependencies?.['react-scripts']) {
  const scriptsKey = packageJson.dependencies?.['react-scripts'] ? 'dependencies' : 'devDependencies';
  console.log(`Updating react-scripts to latest version`);
  packageJson[scriptsKey]['react-scripts'] = "latest";
}

fs.writeFileSync('./package.json', JSON.stringify(packageJson, null, 2));
console.log('✅ package.json updated successfully!');
