/**
 * 305241 Digital Logic Design · Exam 03 Interactive Circuit Simulator
 * Synchronous 3-bit Up/Down Counter with Mode Control M (D-FF & JK-FF)
 */

(function () {
  'use strict';

  // State: QC (MSB), QB, QA (LSB) and Mode M (0 = Up, 1 = Down)
  let qc = 0;
  let qb = 0;
  let qa = 0;
  let modeM = 0;
  let timerId = null;

  // DOM Elements
  const numDisplay = document.getElementById('lab-num');
  const chipC = document.getElementById('bit-c');
  const chipB = document.getElementById('bit-b');
  const chipA = document.getElementById('bit-a');
  const modeStatus = document.getElementById('mode-status');
  const logBox = document.getElementById('state-log');
  const btnClock = document.getElementById('btn-clock');
  const btnAuto = document.getElementById('btn-auto');
  const btnReset = document.getElementById('btn-reset');
  const btnToggleMode = document.getElementById('btn-toggle-mode');
  const stateSelect = document.getElementById('select-state');

  // Compute D Flip-Flop excitation inputs
  function computeDInputs(m, c, b, a) {
    const notM = m === 0 ? 1 : 0;
    const notC = c === 0 ? 1 : 0;
    const notB = b === 0 ? 1 : 0;
    const notA = a === 0 ? 1 : 0;

    // Toggle steering conditions:
    // TB = M' · QA + M · QA'
    const tB = (notM && a) || (m && notA) ? 1 : 0;

    // TC = M' · QB · QA + M · QB' · QA'
    const tC = (notM && b && a) || (m && notB && notA) ? 1 : 0;

    // DA = QA'
    const da = notA;

    // DB = QB ⊕ TB
    const db = b ^ tB;

    // DC = QC ⊕ TC
    const dc = c ^ tC;

    return { da, db, dc, tB, tC };
  }

  // Update UI displays
  function updateUI() {
    const dec = (qc << 2) | (qb << 1) | qa;
    if (numDisplay) {
      numDisplay.textContent = dec;
    }

    if (chipC) {
      chipC.textContent = qc;
      chipC.classList.toggle('active', qc === 1);
    }
    if (chipB) {
      chipB.textContent = qb;
      chipB.classList.toggle('active', qb === 1);
    }
    if (chipA) {
      chipA.textContent = qa;
      chipA.classList.toggle('active', qa === 1);
    }

    if (modeStatus) {
      if (modeM === 0) {
        modeStatus.textContent = 'M = 0 (โหมดนับขึ้น UP: 0 → 1 → 2 ... → 7 → 0)';
        modeStatus.style.color = '#38BDF8';
      } else {
        modeStatus.textContent = 'M = 1 (โหมดนับลง DOWN: 7 → 6 → 5 ... → 0 → 7)';
        modeStatus.style.color = '#F59E0B';
      }
    }

    if (stateSelect) {
      stateSelect.value = dec.toString();
    }
  }

  function appendLog(msg) {
    if (!logBox) return;
    const div = document.createElement('div');
    div.textContent = msg;
    logBox.appendChild(div);
    logBox.scrollTop = logBox.scrollHeight;
  }

  // Single Clock Pulse Transition
  function clockPulse() {
    const currentDec = (qc << 2) | (qb << 1) | qa;
    const { da, db, dc, tB, tC } = computeDInputs(modeM, qc, qb, qa);
    const nextDec = (dc << 2) | (db << 1) | da;

    const modeName = modeM === 0 ? 'UP' : 'DOWN';

    appendLog(
      `CLK [${modeName}]: สภาวะ ${currentDec} (${qc}${qb}${qa}) → ถัดไป ${nextDec} (${dc}${db}${da}) | ` +
      `Steering T: (TB=${tB}, TC=${tC}) | D-Inputs: (DC=${dc}, DB=${db}, DA=${da})`
    );

    qc = dc;
    qb = db;
    qa = da;

    updateUI();
  }

  function toggleMode() {
    modeM = modeM === 0 ? 1 : 0;
    const modeName = modeM === 0 ? 'นับขึ้น (UP: M=0)' : 'นับลง (DOWN: M=1)';
    appendLog(`MODE: สลับทิศทางการนับเป็น → ${modeName}`);
    updateUI();
  }

  function setDirectState(val) {
    const num = parseInt(val, 10);
    if (isNaN(num) || num < 0 || num > 7) return;
    qc = (num >> 2) & 1;
    qb = (num >> 1) & 1;
    qa = num & 1;
    appendLog(`FORCE: บังคับตั้งค่าสถานะเริ่มต้นเป็น ${num} (${qc}${qb}${qa})`);
    updateUI();
  }

  function resetState() {
    qc = 0;
    qb = 0;
    qa = 0;
    if (logBox) logBox.innerHTML = '';
    appendLog('RESET: รีเซ็ตวงจรกลับสู่สถานะ 0 (000) เรียบร้อย');
    updateUI();
  }

  function toggleAuto() {
    if (timerId !== null) {
      clearInterval(timerId);
      timerId = null;
      btnAuto.textContent = 'เริ่มนับอัตโนมัติ (Auto Clock)';
      btnAuto.classList.remove('secondary');
    } else {
      timerId = setInterval(clockPulse, 900);
      btnAuto.textContent = 'หยุดนับอัตโนมัติ (Pause)';
      btnAuto.classList.add('secondary');
    }
  }

  // Event Listeners
  if (btnClock) btnClock.addEventListener('click', clockPulse);
  if (btnAuto) btnAuto.addEventListener('click', toggleAuto);
  if (btnReset) btnReset.addEventListener('click', resetState);
  if (btnToggleMode) btnToggleMode.addEventListener('click', toggleMode);
  if (stateSelect) {
    stateSelect.addEventListener('change', (e) => {
      setDirectState(e.target.value);
    });
  }

  // Init
  updateUI();
  appendLog('INITIALIZED: พร้อมจำลองวงจรนับขึ้น/ลง 3 บิต พร้อมขาควบคุมโหมด M (คลิก CLK เพื่อเริ่ม)');
})();
