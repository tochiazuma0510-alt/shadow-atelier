// search/ninfty-nf-lanea-cli.mjs
//
// Thin CLI wrapper around ninfty-searcher-v2.mjs's computeNormalFormLaneA,
// for the third-party crosscheck script (search/ninfty-nf-crosscheck.py) to
// invoke as a subprocess. Deliberately does nothing but load a candidate
// JSON and print the NF report -- no comparison logic lives here (that
// belongs to the crosscheck script alone, per the lane-independence
// discipline: the crosscheck must not import either lane's implementation).
//
// usage: node search/ninfty-nf-lanea-cli.mjs path/to/candidate.json
//        node search/ninfty-nf-lanea-cli.mjs -   (reads candidate JSON from stdin)

import { readFileSync } from 'node:fs';
import { computeNormalFormLaneA } from './ninfty-searcher-v2.mjs';

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
    process.stderr.write('usage: node ninfty-nf-lanea-cli.mjs <candidate.json | ->\n');
    process.exit(2);
  }
  const text = arg === '-' ? await readAll(process.stdin) : readFileSync(arg, 'utf8');
  const candidate = JSON.parse(text);
  const result = computeNormalFormLaneA(candidate);
  process.stdout.write(JSON.stringify(result, null, 0) + '\n');
}

main(process.argv);
