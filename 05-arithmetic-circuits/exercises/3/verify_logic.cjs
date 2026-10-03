'use strict';
const assert = require('node:assert/strict');
const { calculate } = require('./circuit.js');

// The reference follows the five required outputs, independently of gate equations.
function expected(a, b, g, j, k) {
  if (g === 1) return 15;
  const data = k === 0 ? a : b;
  return j === 0 ? data : 15 - data;
}

let cases = 0;
for (let a = 0; a < 16; a++) {
  for (let b = 0; b < 16; b++) {
    for (let g = 0; g < 2; g++) {
      for (let j = 0; j < 2; j++) {
        for (let k = 0; k < 2; k++) {
          const input = { a, b, g, j, k };
          const r = calculate(input);
          const description = JSON.stringify(input);
          assert.equal(r.output, expected(a, b, g, j, k), description);
          assert.equal(r.x + r.y, r.sum, description);
          assert.equal(r.x & r.y, 0, description);
          assert.equal(r.carry, 0, description);
          assert.ok(r.rows.every((row) => row.cin === 0 && row.cout === 0), description);
          assert.equal(r.rows.reduce((word, row) => word | (row.s << (row.bit - 1)), 0), r.output, description);
          assert.equal(r.rows.reduce((word, row) => word | (row.sigma << (row.bit - 1)), 0), r.sum, description);
          cases++;
        }
      }
    }
  }
}

for (const field of ['a', 'b', 'g', 'j', 'k']) {
  for (const value of [-1, 16, 1.5, NaN, '1']) {
    assert.throws(() => calculate({ a: 10, b: 3, g: 0, j: 1, k: 0, [field]: value }), RangeError);
  }
}
console.log(`PASS: ${cases} input combinations match Figure 5.36; all carries are zero; invalid inputs rejected.`);
