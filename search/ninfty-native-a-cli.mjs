// search/ninfty-native-a-cli.mjs
//
// Thin CLI wrapper around ninfty-searcher-v2.mjs's buildSearcherNative, for
// EP registry provisioning (search/ninfty-ep-genuine-provisioning.py) to
// invoke as a subprocess -- mirrors search/ninfty-nf-lanea-cli.mjs's
// separation discipline: this file does nothing but load a candidate JSON
// and print buildSearcherNative's own output verbatim, no extra logic.
//
// usage: node search/ninfty-native-a-cli.mjs path/to/candidate.json
//        node search/ninfty-native-a-cli.mjs -   (reads candidate JSON from stdin)

import { readFileSync } from 'node:fs';
import { buildSearcherNative } from './ninfty-searcher-v2.mjs';

function readAll(stream) {
  return new Promise((resolve, reject) => {
    let data = '';
    stream.setEncoding('utf8');
    stream.on('data', (c) => { data += c; });
    stream.on('end', () => resolve(data));
    stream.on('error', reject);
  });
}

async function main(argv) {
  const arg = argv[2];
  if (!arg) {
    process.stderr.write('usage: node ninfty-native-a-cli.mjs <candidate.json | ->\n');
    process.exit(2);
  }
  const text = arg === '-' ? await readAll(process.stdin) : readFileSync(arg, 'utf8');
  const candidate = JSON.parse(text);
  const result = buildSearcherNative(candidate);
  process.stdout.write(JSON.stringify(result, null, 0) + '\n');
}

main(process.argv);
