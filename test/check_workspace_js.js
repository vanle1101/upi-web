"use strict";

const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..");
const sourcePath = path.join(root, "web", "static", "workspace.js");
const source = fs.readFileSync(sourcePath, "utf8");

try {
  new Function(source);
  process.stdout.write("[PASS] workspace.js syntax is valid\n");
} catch (error) {
  process.stderr.write(`[FAIL] workspace.js syntax error: ${error.message}\n`);
  process.exitCode = 1;
}
