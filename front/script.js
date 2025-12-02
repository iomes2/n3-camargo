async function loadResults() {
  const summaryEl = document.getElementById('summary');
  const bestEl = document.getElementById('best');
  const metricsTbody = document.getElementById('metrics');
  metricsTbody.innerHTML = '';

  try {
    const res = await fetch('../models/results.json');
    if (!res.ok) throw new Error('Não foi possível carregar results.json');
    const data = await res.json();

    const entries = Object.entries(data);
    const best = entries.reduce((acc, [name, m]) => {
      return !acc || (m.f1 > acc[1].f1) ? [name, m] : acc;
    }, null);

    summaryEl.innerHTML = `<span class="badge">Modelos avaliados: ${entries.length}</span>`;
    if (best) {
      bestEl.innerHTML = `<div class="badge">${best[0]}</div> <span class="best">F1: ${best[1].f1.toFixed(3)}</span>`;
    } else {
      bestEl.textContent = 'Sem dados';
    }

    entries.forEach(([name, m]) => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${name}</td>
        <td>${Number(m.accuracy).toFixed(3)}</td>
        <td>${Number(m.precision).toFixed(3)}</td>
        <td>${Number(m.recall).toFixed(3)}</td>
        <td>${Number(m.f1).toFixed(3)}</td>
      `;
      metricsTbody.appendChild(tr);
    });
  } catch (err) {
    summaryEl.textContent = 'Erro ao carregar: ' + err.message;
    bestEl.textContent = '';
  }
}

document.getElementById('reload').addEventListener('click', loadResults);
loadResults();
