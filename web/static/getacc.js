(() => {
  "use strict";

  const dom = {
    input: document.getElementById("getacc-json-input"),
    btnExtract: document.getElementById("getacc-extract-btn"),
    jobList: document.getElementById("getacc-job-list"),
    jobSummary: document.getElementById("getacc-job-summary"),
    btnClearAll: document.getElementById("getacc-btn-clear-all"),
  };

  if (!dom.input || !dom.jobList) return;

  let state = {
    jobs: [], // array of extracted results
    counter: 0,
  };

  const escHtml = (str) => {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  };

  const updateGetAccChart = () => {
    const total = state.jobs.length;
    const failed = state.jobs.filter((j) => !j.cookies && !j.credentials).length;
    const success = Math.max(total - failed, 0);
    const successRate = total ? (success / total) * 100 : 0;
    if (window.GptUi && window.GptUi.updateRealtimeChart) {
      window.GptUi.updateRealtimeChart('getacc-realtime-chart', successRate, {
        color: 'var(--ops-blue)',
        displayValue: window.GptUi.fmtPercent ? window.GptUi.fmtPercent(successRate) : `${successRate.toFixed(1)}%`,
        label: 'Extraction success rate',
      });
    }
    const totalEl = document.getElementById('getacc-chart-total');
    const errorEl = document.getElementById('getacc-chart-errors');
    const successEl = document.getElementById('getacc-rail-success');
    if (successEl) successEl.textContent = String(success);
    if (totalEl) totalEl.textContent = String(total);
    if (errorEl) errorEl.textContent = String(failed);
  };

  const renderList = () => {
    if (state.jobs.length === 0) {
      dom.jobList.innerHTML = '<div class="empty">No data yet. Paste JSON into the input box to begin.</div>';
      if (dom.jobSummary) dom.jobSummary.textContent = '0 total';
      updateGetAccChart();
      return;
    }

    const html = state.jobs.map((j, idx) => {
      let emailText = j.email || "Unknown Email";
      
      let statusClass = "success";
      let statusText = "success";
      if (!j.cookies && !j.credentials) {
         statusClass = "error";
         statusText = "failed";
      } else if (!j.cookies) {
         statusClass = "warning";
         statusText = "combo only";
      } else if (!j.credentials && j.email) {
         // It's still a success since we extracted cookies!
         statusClass = "success";
         statusText = "cookies only";
      }

      let actionBtns = '';
      if (j.credentials) {
         actionBtns += `<button class="icon-btn" data-action="copy-combo" data-id="${j.id}" title="Copy Combo (mail|pass|2fa)">${window.GptUi?.icon ? window.GptUi.icon('copy') : '📋'}</button>`;
      }
      if (j.cookies) {
         actionBtns += `<button class="icon-btn" data-action="copy-cookies" data-id="${j.id}" title="Copy JSON Cookies">${window.GptUi?.icon ? window.GptUi.icon('token') : '🍪'}</button>`;
      }

      const planBadge = j.plan_type
        ? `<span class="plan-badge plan-${escHtml(j.plan_type.toLowerCase())}">${escHtml(j.plan_type)}</span>`
        : '';

      return `
        <div class="job" data-id="${j.id}">
          <div class="job-index">${state.jobs.length - idx}</div>
          <div class="job-status status-${statusClass}">${escHtml(statusText)}</div>
          <div class="job-main">
            <div class="job-email" title="${escHtml(emailText)}">
              <span class="job-email-text">${escHtml(emailText)}</span>
              ${planBadge}
              ${j.credentials ? '<span class="plan-badge plan-plus" style="margin-left: 8px;">Combo Found</span>' : ''}
              ${j.cookies ? '<span class="plan-badge plan-free" style="margin-left: 8px;">Cookies</span>' : ''}
            </div>
          </div>
          <div class="job-actions">
            ${actionBtns}
            <button class="icon-btn icon-danger" data-action="remove" data-id="${j.id}" title="Remove">${window.GptUi?.icon ? window.GptUi.icon('remove') : '❌'}</button>
          </div>
        </div>
      `;
    }).join('');

    dom.jobList.innerHTML = html;
    if (dom.jobSummary) dom.jobSummary.textContent = `${state.jobs.length} total`;
    updateGetAccChart();
  };

  // Event Delegation for action buttons
  dom.jobList.addEventListener('click', async (e) => {
    const btn = e.target.closest('button[data-action]');
    if (!btn) return;
    
    const action = btn.dataset.action;
    const id = parseInt(btn.dataset.id, 10);
    const job = state.jobs.find(x => x.id === id);
    if (!job) return;

    if (action === 'remove') {
      state.jobs = state.jobs.filter(x => x.id !== id);
      renderList();
    } else if (action === 'copy-cookies' && job.cookies) {
      try {
        await navigator.clipboard.writeText(job.cookies);
        // Visual feedback
        const origHtml = btn.innerHTML;
        btn.innerHTML = '✅';
        setTimeout(() => { btn.innerHTML = origHtml; }, 1000);
      } catch (err) { alert('Copy failed!'); }
    } else if (action === 'copy-combo' && job.credentials) {
      try {
        await navigator.clipboard.writeText(job.credentials);
        const origHtml = btn.innerHTML;
        btn.innerHTML = '✅';
        setTimeout(() => { btn.innerHTML = origHtml; }, 1000);
      } catch (err) { alert('Copy failed!'); }
    }
  });

  if (dom.btnClearAll) {
    dom.btnClearAll.addEventListener('click', () => {
      state.jobs = [];
      renderList();
    });
  }

  const processInput = async () => {
    const rawVal = dom.input.value.trim();
    if (!rawVal) return;

    let email = null;
    let extractedCookies = null;
    let planType = null;

    try {
      const parsed = JSON.parse(rawVal);
      if (parsed.user && parsed.user.email) email = parsed.user.email;
      else if (parsed.email) email = parsed.email;
      
      if (parsed.account && parsed.account.planType) {
        planType = parsed.account.planType;
      }
      
      if (parsed.sessionToken && (!parsed.__cookies || !Array.isArray(parsed.__cookies) || parsed.__cookies.length === 0)) {
        const chunkString = (str, length) => str.match(new RegExp('.{1,' + length + '}', 'g')) || [];
        const chunks = chunkString(parsed.sessionToken, 3900);
        parsed.__cookies = chunks.map((chunk, index) => ({
          name: chunks.length > 1 ? `__Secure-next-auth.session-token.${index}` : '__Secure-next-auth.session-token',
          value: chunk,
          domain: "chatgpt.com",
          path: "/",
          secure: true,
          httpOnly: true,
          sameSite: "lax"
        }));
      }

      if (parsed.__cookies && Array.isArray(parsed.__cookies)) {
        const fixedCookies = parsed.__cookies.map(cookie => {
          if (cookie.sameSite) {
            cookie.sameSite = cookie.sameSite.toLowerCase();
            if (cookie.sameSite === 'none') cookie.sameSite = 'no_restriction';
          }
          return cookie;
        });
        extractedCookies = JSON.stringify(fixedCookies, null, 2);
      }
    } catch (err) {
      if (rawVal.includes("@")) {
        const parts = rawVal.split("|");
        email = parts[0].trim();
      }
    }

    if (!email && !extractedCookies) return;

    state.counter++;
    const newJob = {
      id: state.counter,
      email: email,
      cookies: extractedCookies,
      credentials: null,
      plan_type: planType
    };
    
    // Add to top of the list
    state.jobs.unshift(newJob);
    renderList();
    
    // Auto-clear input!
    dom.input.value = "";

    // Fetch credentials quietly in background
    if (email) {
      try {
        const token = document.querySelector('meta[name="auth-token"]')?.content || "";
        const res = await fetch(`/api/account-credentials?email=${encodeURIComponent(email)}`, {
          headers: { "X-API-Token": token }
        });
        if (res.ok) {
          const data = await res.json();
          if (data.success) {
            newJob.credentials = data.credentials;
            renderList(); // re-render to show combo button
          }
        }
      } catch (err) {}
    }
  };

  let inputTimer;
  dom.input.addEventListener("input", () => {
    clearTimeout(inputTimer);
    inputTimer = setTimeout(() => {
      if (dom.input.value.trim().length > 10) {
        processInput();
      }
    }, 250);
  });

  if (dom.btnExtract) {
    dom.btnExtract.addEventListener("click", processInput);
  }

})();
