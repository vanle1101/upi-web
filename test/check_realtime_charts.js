const fs = require('fs');
const path = require('path');
const vm = require('vm');

const root = path.resolve(__dirname, '..');
const read = (rel) => fs.readFileSync(path.join(root, rel), 'utf8');
const assert = (condition, message) => {
  if (!condition) {
    throw new Error(message);
  }
};

const html = read('web/static/index.html');
const css = read('web/static/operations.css');
const scripts = [
  'web/static/app.js',
  'web/static/session.js',
  'web/static/upi.js',
  'web/static/getacc.js',
  'web/static/settings_panel.js',
];

for (const script of scripts) {
  new vm.Script(read(script), { filename: script });
}

for (const id of [
  'reg-realtime-chart',
  'reg-total-jobs-chart',
  'reg-active-runs-chart',
  'reg-avg-time-chart',
  'reg-error-rate-chart',
  'session-realtime-chart',
  'upi-realtime-chart',
  'upi-total-jobs-chart',
  'upi-active-runs-chart',
  'upi-avg-time-chart',
  'upi-error-rate-chart',
  'getacc-realtime-chart',
]) {
  const count = (html.match(new RegExp(`id="${id}"`, 'g')) || []).length;
  assert(count === 1, `${id} should exist once in index.html`);
}

for (const id of [
  'upi-metric-total-jobs',
  'upi-metric-success-rate',
  'upi-metric-active-runs',
  'upi-metric-avg-time',
  'upi-metric-error-rate',
]) {
  const count = (html.match(new RegExp(`id="${id}"`, 'g')) || []).length;
  assert(count === 1, `${id} should exist once in index.html`);
}

assert(read('web/static/app.js').includes('updateRealtimeChart'), 'app.js should expose realtime chart helper');
assert(html.includes('@lhv_myhanh'), 'visible brand should be @lhv_myhanh');
assert(read('web/static/app.js').includes('chartVisualPoints'), 'realtime charts should render visual movement when values are flat');
assert(read('web/static/app.js').includes('updatePipelineFromStats'), 'registration pipeline should follow live job stats');
assert(read('web/static/app.js').includes('reg-active-runs-chart'), 'registration active runs chart should be wired');
assert(read('web/static/app.js').includes('reg-error-rate-chart'), 'registration error chart should be wired');
assert(read('web/static/session.js').includes('session-realtime-chart'), 'session chart should be wired');
assert(read('web/static/upi.js').includes('upi-realtime-chart'), 'UPI chart should be wired');
assert(read('web/static/upi.js').includes('upi-active-runs-chart'), 'UPI active runs chart should be wired');
assert(read('web/static/upi.js').includes('upi-error-rate-chart'), 'UPI error chart should be wired');
assert(read('web/static/upi.js').includes('upi-metric-success-rate'), 'UPI metrics should be wired');
assert(read('web/static/getacc.js').includes('getacc-realtime-chart'), 'Get Acc chart should be wired');
assert(!html.includes('settings-realtime-chart'), 'Settings chart should be removed from settings UI');
assert(css.includes('.ops-realtime-chart'), 'chart CSS should exist');
assert(css.includes('.metric-sparkline'), 'metric cards should use realtime sparkline charts');
assert(css.includes('.job-actions .icon-btn'), 'job action icon override should exist');
assert(css.includes('width: 22px'), 'job action icons should use compact old-style sizing');
assert(css.includes('--metric-ring'), 'success ring should be driven by realtime metric value');
assert(!css.includes('.pipeline-step:first-child.is-current::before'), 'current first pipeline step must not fake a completed tick');
assert(css.includes('.mac-select-dropdown.is-open'), 'custom select dropdown should be positioned and styled');
assert(read('web/static/app.js').includes("successRing.style.setProperty('--metric-ring'"), 'registration success ring should update from live stats');
assert(read('web/static/upi.js').includes("upiSuccessRing.style.setProperty('--metric-ring'"), 'UPI success ring should update from live stats');
assert(css.includes('.job-status.status-running'), 'running status should have a blue state override');
assert(css.includes('.job-status.status-error'), 'error status should have a red state override');
assert(css.includes('.pipeline-strip.is-running'), 'pipeline should have a running animation state');
assert(css.includes('.modal[style*="display: none"]'), 'modal hidden state should remain explicit');

console.log('realtime chart + action button checks OK');
