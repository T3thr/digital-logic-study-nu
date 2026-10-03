/**
 * 305241 Digital Logic Design · Exam 01 Interactive Circuit Simulator
 * Synchronous 4-bit Counter: Divisible by 3 (0, 3, 6, 9, 12, 15) with Next = Present + 1
 */

(function () {
  'use strict';

  // State: QD (MSB), QC, QB, QA (LSB)
  let qd = 0;
  let qc = 0;
  let qb = 0;
  let qa = 0;
  let timerId = null;

  // DOM Elements
  const numDisplay = document.getElementById('lab-num');
  const chipD = document.getElementById('bit-d');
  const chipC = document.getElementById('bit-c');
  const chipB = document.getElementById('bit-b');
  const chipA = document.getElementById('bit-a');
  const logBox = document.getElementById('state-log');
  const btnClock = document.getElementById('btn-clock');
  const btnAuto = document.getElementById('btn-auto');
  const btnReset = document.getElementById('btn-reset');
  const stateSelect = document.getElementById('select-state');

  // Compute logic gate equations for JK inputs based on present state
  function computeInputs(d, c, b, a) {
    const notD = d === 0 ? 1 : 0;
    const notC = c === 0 ? 1 : 0;
    const notB = b === 0 ? 1 : 0;
    const notA = a === 0 ? 1 : 0;

    // JA = 1, KA = 1
    const ja = 1;
    const ka = 1;

    // JB = (QD ⊙ QC) + QD' · QA = (QD' · QC' + QD · QC) + QD' · QA
    const jb = ((notD && notC) || (d && c) || (notD && a)) ? 1 : 0;

    // KB = QD' · QC + QD · QA
    const kb = ((notD && c) || (d && a)) ? 1 : 0;

    // JC = (QB + QD) · QA = QB · QA + QD · QA
    const jc = ((b || d) && a) ? 1 : 0;

    // KC = QB · (QD' + QA) = QB · QD' + QB · QA
    const kc = (b && (notD || a)) ? 1 : 0;

    // JD = QC · QB
    const jd = (c && b) ? 1 : 0;

    // KD = QC · QB · QA
    const kd = (c && b && a) ? 1 : 0;

    return { jd, kd, jc, kc, jb, kb, ja, ka };
  }

  // Compute Next State using JK characteristic: Q+ = J · Q' + K' · Q
  function computeNextState(d, c, b, a) {
    const { jd, kd, jc, kc, jb, kb, ja, ka } = computeInputs(d, c, b, a);
    const nextD = (jd && !d) || (!kd && d) ? 1 : 0;
    const nextC = (jc && !c) || (!kc && c) ? 1 : 0;
    const nextB = (jb && !b) || (!kb && b) ? 1 : 0;
    const nextA = (ja && !a) || (!ka && a) ? 1 : 0;
    return { nextD, nextC, nextB, nextA, jd, kd, jc, kc, jb, kb, ja, ka };
  }

  // Update UI displays
  function updateUI() {
    const dec = (qd << 3) | (qc << 2) | (qb << 1) | qa;
    if (numDisplay) {
      numDisplay.textContent = dec;
    }

    if (chipD) {
      chipD.textContent = qd;
      chipD.classList.toggle('active', qd === 1);
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
    const currentDec = (qd << 3) | (qc << 2) | (qb << 1) | qa;
    const { nextD, nextC, nextB, nextA, jd, kd, jc, kc, jb, kb, ja, ka } = computeNextState(qd, qc, qb, qa);
    const nextDec = (nextD << 3) | (nextC << 2) | (nextB << 1) | nextA;

    const isMainCycle = [0, 3, 6, 9, 12, 15].includes(currentDec);
    const typeLabel = isMainCycle ? '[หาร 3 ลงตัว]' : '[กู้คืน Next = S+1]';

    appendLog(
      `CLK: สภาวะ ${currentDec} (${qd}${qc}${qb}${qa}) ${typeLabel} → ถัดไป ${nextDec} (${nextD}${nextC}${nextB}${nextA}) | ` +
      `J,K: D=(${jd},${kd}) C=(${jc},${kc}) B=(${jb},${kb}) A=(${ja},${ka})`
    );

    qd = nextD;
    qc = nextC;
    qb = nextB;
    qa = nextA;

    updateUI();
  }

  function setDirectState(val) {
    const num = parseInt(val, 10);
    if (isNaN(num) || num < 0 || num > 15) return;
    qd = (num >> 3) & 1;
    qc = (num >> 2) & 1;
    qb = (num >> 1) & 1;
    qa = num & 1;
    appendLog(`FORCE: บังคับตั้งค่าสถานะเริ่มต้นเป็น ${num} (${qd}${qc}${qb}${qa})`);
    updateUI();
  }

  function resetState() {
    qd = 0;
    qc = 0;
    qb = 0;
    qa = 0;
    if (logBox) logBox.innerHTML = '';
    appendLog('RESET: รีเซ็ตวงจรกลับสู่สถานะ 0 (0000) เรียบร้อย');
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
  if (stateSelect) {
    stateSelect.addEventListener('change', (e) => {
      setDirectState(e.target.value);
    });
  }

  // Init
  updateUI();
  appendLog('INITIALIZED: พร้อมจำลองวงจรนับ 4 บิต (คลิก "ส่งสัญญาณนาฬิกา 1 พัลส์" เพื่อเริ่ม)');
})();
