'use strict';

(() => {
  const initial = { a: 10, b: 3, g: 0, j: 1, k: 0 };
  let state = { ...initial };
  let step = 0;
  const $ = (id) => document.getElementById(id);
  const binary = (value) => value.toString(2).padStart(4, '0');
  const modes = [
    { id: 'a', label: 'ส่ง A', code: '000', g: 0, j: 0, k: 0 },
    { id: 'b', label: 'ส่ง B', code: '001', g: 0, j: 0, k: 1 },
    { id: 'not-a', label: 'กลับบิต A', code: '010', g: 0, j: 1, k: 0 },
    { id: 'not-b', label: 'กลับบิต B', code: '011', g: 0, j: 1, k: 1 },
    { id: 'ones', label: 'บังคับ 1111', code: '1××', g: 1 }
  ];

  function currentMode() {
    return modes.find((m) => m.g === state.g && (m.g === 1 || (m.j === state.j && m.k === state.k)));
  }

  function clearInputError() {
    $('input-error').textContent = '';
    for (const word of ['a', 'b']) $(word + '-value').removeAttribute('aria-invalid');
  }

  function render() {
    const r = MultifunctionCircuit.calculate(state);
    const mode = currentMode();
    for (const word of ['a', 'b']) {
      const input = $(word + '-value');
      if (input.getAttribute('aria-invalid') !== 'true') input.value = state[word];
    }
    document.querySelectorAll('[data-word]').forEach((button) => {
      const on = (state[button.dataset.word] >> Number(button.dataset.bit)) & 1;
      button.textContent = on;
      button.setAttribute('aria-pressed', String(Boolean(on)));
    });
    document.querySelectorAll('[data-control]').forEach((button) => {
      const key = button.dataset.control;
      button.textContent = `${key.toUpperCase()} = ${state[key]}`;
      button.setAttribute('aria-pressed', String(Boolean(state[key])));
    });
    document.querySelectorAll('[data-mode]').forEach((button) => {
      button.setAttribute('aria-pressed', String(button.dataset.mode === mode.id));
    });
    $('result-bits').textContent = binary(r.output);
    $('result-decimal').textContent = ` = ${r.output}₁₀`;
    $('mode-label').textContent = mode.label;
    $('mode-reason').textContent = `G = ${state.g}, J = ${state.j}, K = ${state.k}`;
    $('xor-values').innerHTML = `A ⊕ J = ${binary(r.xorA)}<br>B ⊕ J = ${binary(r.xorB)}`;
    $('operand-values').innerHTML = `X = ${binary(r.x)}<br>Y = ${binary(r.y)}`;
    $('sum-values').innerHTML = `Σ = ${binary(r.sum)}<br>C₀ = 0, C₄ = ${r.carry}`;
    $('output-values').innerHTML = `${binary(r.sum)} ∨ ${binary(state.g * 15)}<br>S = ${binary(r.output)}`;
    document.querySelectorAll('[data-stage]').forEach((card) => {
      const active = Number(card.dataset.stage) === step;
      card.classList.toggle('current', active);
      if (active) card.setAttribute('aria-current', 'step');
      else card.removeAttribute('aria-current');
    });
    $('step-count').textContent = `ขั้นที่ ${step + 1} / 4`;
    $('step-prev').disabled = step === 0;
    $('step-next').disabled = step === 3;
    const explanation = [
      state.j === 1
        ? `J = 1 จึงกลับทุกบิต: A ${binary(state.a)} → ${binary(r.xorA)} และ B ${binary(state.b)} → ${binary(r.xorB)}`
        : `J = 0 ทำให้ XOR ผ่านข้อมูลเดิม: A ${binary(state.a)} → ${binary(r.xorA)} และ B ${binary(state.b)} → ${binary(r.xorB)}`,
      state.k === 0
        ? `K = 0 และ K กลับค่า = 1 จึงเปิดฝั่ง A: X = ${binary(r.x)} ส่วนฝั่ง B ถูก AND กับ 0 ทำให้ Y = 0000`
        : `K = 1 และ K กลับค่า = 0 จึงเปิดฝั่ง B: Y = ${binary(r.y)} ส่วนฝั่ง A ถูก AND กับ 0 ทำให้ X = 0000`,
      `74283 บวก X + Y + C₀ = ${binary(r.x)} + ${binary(r.y)} + 0 = ${binary(r.sum)} มีข้อมูลเพียงฝั่งเดียว จึงไม่มีตัวทดทุกบิต: C₁ = C₂ = C₃ = C₄ = 0`,
      state.g === 1
        ? `G = 1: ทุกบิตผ่าน OR กับ 1 ดังนั้น ${binary(r.sum)} ∨ 1111 = 1111 ไม่ว่าค่า J, K, A, B จะเป็นอะไร`
        : `G = 0: ทุกบิตผ่าน OR กับ 0 ดังนั้น S = ${binary(r.sum)} ∨ 0000 = ${binary(r.output)} (${mode.label})`
    ];
    $('step-text').textContent = explanation[step];
    $('carry-rows').innerHTML = r.rows.map((row) => `<tr><th scope="row">${row.bit}${row.bit === 1 ? ' · LSB' : row.bit === 4 ? ' · MSB' : ''}</th><td>${row.x}</td><td>${row.y}</td><td>${row.cin}</td><td>${row.sigma}</td><td>${row.cout}</td><td>${row.g}</td><td>${row.s}</td></tr>`).join('');
    $('example-caption').textContent = `ตารางที่ 5 · A = ${binary(state.a)}, B = ${binary(state.b)}`;
    $('mode-rows').innerHTML = modes.map((m) => {
      const control = m.g === 1 ? { g: 1, j: state.j, k: state.k } : { g: 0, j: m.j, k: m.k };
      const value = MultifunctionCircuit.calculate({ ...state, ...control }).output;
      return `<tr data-mode-row="${m.id}"${m.id === mode.id ? ' class="active"' : ''}><td>${m.code}</td><td>${m.label}</td><td class="math">${binary(value)}</td><td>${value}</td></tr>`;
    }).join('');
  }

  document.querySelectorAll('[data-word]').forEach((button) => {
    button.addEventListener('click', () => {
      state[button.dataset.word] ^= 1 << Number(button.dataset.bit);
      clearInputError();
      render();
    });
  });
  document.querySelectorAll('[data-control]').forEach((button) => {
    button.addEventListener('click', () => {
      state[button.dataset.control] ^= 1;
      clearInputError();
      render();
    });
  });
  document.querySelectorAll('[data-mode]').forEach((button) => {
    button.addEventListener('click', () => {
      const mode = modes.find((m) => m.id === button.dataset.mode);
      state.g = mode.g;
      if (mode.g === 0) { state.j = mode.j; state.k = mode.k; }
      clearInputError();
      render();
    });
  });
  for (const word of ['a', 'b']) {
    const input = $(word + '-value');
    input.addEventListener('input', () => {
      const value = input.valueAsNumber;
      if (!Number.isInteger(value) || value < 0 || value > 15) {
        input.setAttribute('aria-invalid', 'true');
        $('input-error').textContent = `ข้อมูล ${word.toUpperCase()} ต้องเป็นจำนวนเต็ม 0–15 ผลลัพธ์ยังใช้ค่าล่าสุด ${state[word]}`;
        return;
      }
      state[word] = value;
      clearInputError();
      render();
    });
  }
  $('step-prev').addEventListener('click', () => { step = Math.max(0, step - 1); render(); });
  $('step-next').addEventListener('click', () => { step = Math.min(3, step + 1); render(); });
  $('reset-lab').addEventListener('click', () => { state = { ...initial }; step = 0; clearInputError(); render(); });
  $('swap-inputs').addEventListener('click', () => { [state.a, state.b] = [state.b, state.a]; clearInputError(); render(); });
  $('print-button').addEventListener('click', () => window.print());
  document.querySelectorAll('[data-answer]').forEach((button) => {
    button.addEventListener('click', () => {
      document.querySelectorAll('[data-answer]').forEach((b) => b.classList.remove('correct', 'incorrect'));
      const correct = button.dataset.answer === '0101';
      button.classList.add(correct ? 'correct' : 'incorrect');
      const reasons = {
        '1010': '1010 คือค่า A เดิม แต่ J = 1 ต้องกลับทุกบิต จึงได้ 0101',
        '0110': '0110 คือกลับบิต A แล้วบวก 1 แต่ข้อนี้ C₀ = 0 จึงได้ One\'s complement คือ 0101',
        '1111': '1111 จะถูกบังคับเมื่อ G = 1 แต่ข้อนี้ G = 0 จึงผ่านค่ากลับบิต A คือ 0101'
      };
      $('quiz-feedback').textContent = correct
        ? 'ถูกต้อง: K = 0 เลือก A, J = 1 กลับ 1010 เป็น 0101, C₀ = 0 และ G = 0 ให้ผลผ่านตามเดิม'
        : reasons[button.dataset.answer];
    });
  });

  const dialog = $('figure-dialog');
  document.querySelectorAll('[data-zoom]').forEach((button) => {
    button.addEventListener('click', () => {
      $('figure-image').src = button.dataset.zoom;
      $('figure-image').alt = button.dataset.title;
      $('figure-title').textContent = button.dataset.title;
      dialog.showModal();
    });
  });
  $('close-figure').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', (event) => {
    if (event.target !== dialog) return;
    const box = dialog.getBoundingClientRect();
    if (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom) dialog.close();
  });
  render();
})();
