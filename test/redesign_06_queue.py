# -*- coding: utf-8 -*-
import io
PATH = "web/static/workspace.css"
s = io.open(PATH, encoding="utf-8").read()
pairs = []

# Empty state: calmer, more intentional worklist placeholder.
pairs.append((
""".job-list .empty {
  display: grid;
  place-items: center;
  min-height: 180px;
  margin: 20px;
  padding: 34px 20px;
  border: 0;
  border-radius: var(--radius-md);
  color: var(--faint);
  background: var(--paper-soft);
  font-size: 12.5px;
}""",
""".job-list .empty {
  display: grid;
  place-items: center;
  min-height: 180px;
  margin: 18px;
  padding: 40px 24px;
  border: 1px dashed var(--line);
  border-radius: var(--radius-md);
  color: var(--faint);
  background:
    repeating-linear-gradient(135deg, rgba(216, 212, 200, 0.10) 0 11px, transparent 11px 22px),
    var(--paper-soft);
  font-size: 12.5px;
  line-height: 1.6;
  text-align: center;
}"""))

# Job row: more scannable height + clearer active state with stronger accent edge.
pairs.append((
""".job {
  min-height: 52px;
  margin: 0;
  padding: 9px 14px;
  gap: 11px;
  border: 0;
  border-bottom: 1px solid var(--line-soft);
  border-radius: 0;
  color: var(--ink);
  background: transparent;
  box-shadow: none;
  transition: background 140ms ease;
}""",
""".job {
  min-height: 56px;
  margin: 0;
  padding: 11px 16px;
  gap: 13px;
  border: 0;
  border-bottom: 1px solid var(--line-soft);
  border-radius: 0;
  color: var(--ink);
  background: transparent;
  box-shadow: none;
  transition: background 140ms ease, box-shadow 140ms ease;
}"""))

pairs.append((
""".job:hover {
  border-color: var(--line-soft);
  background: #f8f6f1;
  transform: none;
}

.job.is-active {
  border-color: var(--line-soft);
  background: var(--accent-soft);
  box-shadow: inset 3px 0 0 var(--accent);
}""",
""".job:hover {
  border-color: var(--line-soft);
  background: var(--paper-soft);
  transform: none;
}

.job.is-active {
  border-color: transparent;
  background: linear-gradient(90deg, var(--accent-soft), rgba(221, 232, 225, 0.4));
  box-shadow: inset 3px 0 0 var(--accent);
}

.job.is-active .job-email {
  color: var(--accent-hover);
}"""))

# Status chips: refined padding + tabular, slightly stronger weight.
pairs.append((
""".job-status,
.badge,
.plan-badge,
.upi-countdown-badge,
.upi-plan-badge {
  border: 0;
  border-radius: 4px;
  font-family: var(--font-sans);
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.01em;
  text-transform: none;
}""",
""".job-status,
.badge,
.plan-badge,
.upi-countdown-badge,
.upi-plan-badge {
  display: inline-flex;
  align-items: center;
  padding: 3px 8px;
  border: 0;
  border-radius: 999px;
  font-family: var(--font-sans);
  font-size: 10px;
  font-weight: 640;
  letter-spacing: 0.02em;
  text-transform: none;
}"""))

# Running chip: add a soft live dot via the brass-free amber tone already set.
pairs.append((
""".status-running,
.pill-running {
  color: #8a6516;
  border: 0;
  background: #f6ecd5;
}""",
""".status-running,
.pill-running {
  color: #82611a;
  border: 0;
  background: var(--warning-soft);
}

.job-status.status-running::before {
  content: "";
  width: 6px;
  height: 6px;
  margin-right: 6px;
  border-radius: 50%;
  background: currentColor;
  animation: jobPulse 1.6s ease-in-out infinite;
}

@keyframes jobPulse {
  0%, 100% { opacity: 0.4; }
  50% { opacity: 1; }
}"""))

# Success / error chip tones -> align to new soft tokens.
pairs.append((
""".status-success,
.pill-success,
.badge-active,
.badge-success {
  color: #426a4d;
  border: 0;
  background: #e1ede3;
}""",
""".status-success,
.pill-success,
.badge-active,
.badge-success {
  color: #3d6549;
  border: 0;
  background: var(--success-soft);
}"""))

pairs.append((
""".status-error,
.pill-error,
.badge-error {
  color: #925355;
  border: 0;
  background: #f2e2e1;
}""",
""".status-error,
.pill-error,
.badge-error {
  color: #93504a;
  border: 0;
  background: var(--danger-soft);
}"""))

miss = []
for old, new in pairs:
    if old not in s: miss.append(old[:45]); continue
    s = s.replace(old, new, 1)
io.open(PATH, "w", encoding="utf-8").write(s)
print("missing:", miss)
