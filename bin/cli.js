#!/usr/bin/env node
"use strict";

const { execSync } = require("child_process");
const path = require("path");
const fs = require("fs");

const CACHE = path.join(require("os").homedir(), ".plagiarism-checker-cli");
const REPO  = "https://github.com/irgifebry/plagiarism-checker.git";
const VENV  = path.join(CACHE, "venv");
const PYTHON = path.join(VENV, "bin", "python3");
const ANALYZE = path.join(CACHE, "scripts", "analyze.py");
const EXTRACT = path.join(CACHE, "scripts", "extract_text.py");

/**
 * Lazy bootstrap: clones repo and creates venv on first run.
 */
function bootstrap() {
  if (fs.existsSync(ANALYZE)) return;

  console.error(">> Setting up plagiarism-checker (one-time)…");

  // Clone repo
  if (!fs.existsSync(CACHE)) {
    execSync(`git clone --depth 1 ${REPO} "${CACHE}"`, { stdio: "inherit" });
  } else {
    console.error(">> Repo already cached, pulling latest…");
    execSync(`git -C "${CACHE}" pull`, { stdio: "inherit" });
  }

  // Create venv if missing
  if (!fs.existsSync(PYTHON)) {
    execSync(`python3 -m venv "${VENV}"`, { stdio: "inherit" });
  }

  // Install pip deps
  execSync(`"${PYTHON}" -m pip install --quiet pymupdf python-docx requests beautifulsoup4`, { stdio: "inherit" });

  console.error(">> Setup complete.");
}

function usage() {
  console.error("");
  console.error("  npx plagiarism-checker <path/to/file.docx|.pdf|.txt>");
  console.error("");
  process.exit(1);
}

function main() {
  const file = process.argv[2];
  if (!file) usage();

  bootstrap();

  // Extract text first
  const text = execSync(`"${PYTHON}" "${EXTRACT}" "${file}"`, { encoding: "utf-8" });

  // Analyze
  const report = execSync(`"${PYTHON}" "${ANALYZE}"`, { input: text, encoding: "utf-8" });

  process.stdout.write(report);
}

main();
