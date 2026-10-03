(function (root) {
  'use strict';

  function calculate({ a, b, g, j, k }) {
    for (const [name, value, max] of [['a', a, 15], ['b', b, 15], ['g', g, 1], ['j', j, 1], ['k', k, 1]]) {
      if (!Number.isInteger(value) || value < 0 || value > max) {
        throw new RangeError(`${name} must be an integer from 0 to ${max}`);
      }
    }
    const xorA = a ^ (j * 15);
    const xorB = b ^ (j * 15);
    const x = xorA & ((k ^ 1) * 15);
    const y = xorB & (k * 15);
    const rows = [];
    let carry = 0;
    let sum = 0;
    for (let bit = 0; bit < 4; bit++) {
      const xi = (x >> bit) & 1;
      const yi = (y >> bit) & 1;
      const cin = carry;
      const sigma = xi ^ yi ^ cin;
      carry = (xi & yi) | (cin & (xi ^ yi));
      sum |= sigma << bit;
      rows.push({ bit: bit + 1, x: xi, y: yi, cin, sigma, cout: carry, g, s: sigma | g });
    }
    const output = sum | (g * 15);
    return { xorA, xorB, x, y, sum, carry, output, rows };
  }

  const api = Object.freeze({ calculate });
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.MultifunctionCircuit = api;
})(typeof globalThis !== 'undefined' ? globalThis : this);
