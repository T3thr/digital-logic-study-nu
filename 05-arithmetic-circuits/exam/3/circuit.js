/**
 * 305241 Digital Logic Design · Exam 03 Interactive Circuit Simulator
 * Synchronous 3-bit Arbitrary Sequence Counter (2 -> 3 -> 5 -> 1 -> 7 -> 2)
 * Unused States (0, 4, 6 -> 2)
 */

(function () {
  'use strict';

  // State: QC (MSB, Bit 2), QB (Bit 1), QA (LSB, Bit 0)
  let qc = 0;
  let qb = 1;
  let qa = 0; // Default starts at 2 (010)
  let timerId = null;

  // DOM Elements
  const numDisplay = document.getElementById('lab-num');
  const chipC = document.getElementById('bit-c');
  const chipB = document.getElementById('bit-b');
  const chipA = document.getElementById('bit-a');
  const logBox = document.getElementById('state-log');
  const btnClock = document.getElementById('btn-clock');
  const btnAuto = document.getElementById('btn-auto');
  const btnReset = document.getElementById('btn-reset');
  const stateSelect = document.getElementById('select-state');

  // Compute logic gate equations for JK inputs based on present state
  function computeInputs(c, b, a) {
    const notC = c === 0 ? 1 : 0;
    const notB = b === 0 ? 1 : 0;
    const notA = a === 0 ? 1 : 0;

    // JC = QA
    const jc = a;

    // KC = 1 (Tied to High)
    const kc = 1;

    // JB = QC' + QA'
    const jb = (notC || notA) ? 1 : 0;

    // KB = QC' · QA
    const kb = (notC && a) ? 1 : 0;

    // JA = QC' · QB
    const ja = (notC && b) ? 1 : 0;

    // KA = QC · QB
    const ka = (c && b) ? 1 : 0;

    return { jc, kc, jb, kb, ja, ka };
  }

  // Update UI displays
  function updateUI() {
    const dec = (qc << 2) | (qb << 1) | qa;
    if (numDisplay) {
      numDisplay.textContent = dec;
    }

    if (chipC) chipC.textContent = qc;
    if (chipB) chipB.textContent = qb;
    if (chipA) chipA.textContent = qa;

    // Update bit active classes
    [
      { el: chipC, val: qc },
      { el: chipB, val: qb },
      { el: chipA, val: qa }
    ].forEach(item => {
      if (item.el) {
        if (item.val === 1) {
          item.el.classList.add('active');
        } else {
          item.el.classList.remove('active');
        }
      }
    });

    const inputs = computeInputs(qc, qb, qa);

    // Update real-time input monitor
    const monitorMap = {
      'mon-jc': inputs.jc,
      'mon-kc': inputs.kc,
      'mon-jb': inputs.jb,
      'mon-kb': inputs.kb,
      'mon-ja': inputs.ja,
      'mon-ka': inputs.ka
    };

    Object.entries(monitorMap).forEach(([id, val]) => {
      const el = document.getElementById(id);
      if (el) {
        el.textContent = val;
        el.className = `mon-val ${val === 1 ? 'val-high' : 'val-low'}`;
      }
    });

    // Update dropdown
    if (stateSelect) {
      stateSelect.value = dec.toString();
    }
  }

  // Append entry to state log
  function logTransition(fromDec, toDec) {
    if (!logBox) return;

    const fromBin = fromDec.toString(2).padStart(3, '0');
    const toBin = toDec.toString(2).padStart(3, '0');
    const isUnused = (fromDec === 0 || fromDec === 4 || fromDec === 6);
    const tag = isUnused ? '<span class="log-tag tag-recovery">Recovery</span>' : '<span class="log-tag tag-count">Sequence</span>';

    const line = document.createElement('div');
    line.className = 'log-line';
    line.innerHTML = `
      <span class="log-time">${new Date().toLocaleTimeString()}</span>
      ${tag}
      <span class="log-from">${fromDec} (Q=${fromBin})</span>
      <span class="log-arrow">&rarr;</span>
      <span class="log-to">${toDec} (Q=${toBin})</span>
    `;

    logBox.insertBefore(line, logBox.firstChild);

    // Limit log rows
    while (logBox.children.length > 25) {
      logBox.removeChild(logBox.lastChild);
    }
  }

  // Execute one clock pulse transition
  function clockPulse() {
    const fromDec = (qc << 2) | (qb << 1) | qa;
    const inputs = computeInputs(qc, qb, qa);

    // JK next-state function: Q_next = J · Q' + K' · Q
    const notC = qc === 0 ? 1 : 0;
    const notB = qb === 0 ? 1 : 0;
    const notA = qa === 0 ? 1 : 0;

    const nextC = (inputs.jc && notC) || ((inputs.kc === 0 ? 1 : 0) && qc) ? 1 : 0;
    const nextB = (inputs.jb && notB) || ((inputs.kb === 0 ? 1 : 0) && qb) ? 1 : 0;
    const nextA = (inputs.ja && notA) || ((inputs.ka === 0 ? 1 : 0) && qa) ? 1 : 0;

    qc = nextC;
    qb = nextB;
    qa = nextA;

    const toDec = (qc << 2) | (qb << 1) | qa;
    logTransition(fromDec, toDec);
    updateUI();
  }

  // Force state from dropdown
  function forceState(decVal) {
    const val = parseInt(decVal, 10);
    qc = (val >> 2) & 1;
    qb = (val >> 1) & 1;
    qa = val & 1;
    updateUI();
  }

  // Event Listeners
  if (btnClock) {
    btnClock.addEventListener('click', function () {
      clockPulse();
    });
  }

  if (btnAuto) {
    btnAuto.addEventListener('click', function () {
      if (timerId) {
        clearInterval(timerId);
        timerId = null;
        btnAuto.textContent = 'Auto Clock (1 Hz)';
        btnAuto.classList.remove('btn-running');
      } else {
        btnAuto.textContent = 'Stop Clock';
        btnAuto.classList.add('btn-running');
        timerId = setInterval(clockPulse, 1000);
      }
    });
  }

  if (btnReset) {
    btnReset.addEventListener('click', function () {
      qc = 0;
      qb = 1;
      qa = 0; // Reset to 2
      updateUI();
    });
  }

  if (stateSelect) {
    stateSelect.addEventListener('change', function () {
      forceState(this.value);
    });
  }

  // Initial draw
  updateUI();
})();
