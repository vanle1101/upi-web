(() => {
  "use strict";

  function activateDockPanel(dock, target) {
    const tabs = Array.from(dock.querySelectorAll("[data-dock-target]"));
    const panels = Array.from(dock.querySelectorAll("[data-dock-panel]"));
    let matched = false;

    tabs.forEach((tab) => {
      const active = tab.dataset.dockTarget === target;
      tab.classList.toggle("active", active);
      tab.setAttribute("aria-selected", active ? "true" : "false");
      tab.tabIndex = active ? 0 : -1;
      if (active) {
        matched = true;
        tab.classList.remove("has-unseen"); // da mo xem -> tat cham xanh
      }
    });

    panels.forEach((panel) => {
      const active = panel.dataset.dockPanel === target;
      panel.hidden = !active;
      panel.classList.toggle("active", active);
    });

    return matched;
  }

  function setDockCollapsed(dock, collapsed) {
    const button = dock.querySelector("[data-dock-collapse]");
    dock.classList.toggle("is-collapsed", collapsed);
    if (!button) return;
    button.setAttribute("aria-expanded", collapsed ? "false" : "true");
    button.textContent = collapsed ? "Show details" : "Hide details";
  }

  function hasMeaningfulOutput(panel) {
    const output = panel.querySelector(".output-pane") || panel;
    const text = (output.textContent || "").trim();
    if (!text) return false;
    return !text.startsWith("No errors yet") && !text.startsWith("Format:");
  }

  function observeDockOutput(dock) {
    dock.querySelectorAll("[data-dock-panel]").forEach((panel) => {
      const target = panel.dataset.dockPanel;
      const tab = dock.querySelector(`[data-dock-target="${target}"]`);
      if (!tab || target.endsWith("-log")) return;

      const update = () => {
        const hasContent = hasMeaningfulOutput(panel);
        tab.classList.toggle("has-content", hasContent);
        // Chấm xanh "chưa xem": chỉ hiện khi có content VÀ tab đang không được
        // mở. Tab đang active -> coi như đã xem ngay, không báo "unseen".
        if (!hasContent) {
          tab.classList.remove("has-unseen");
        } else if (!tab.classList.contains("active")) {
          tab.classList.add("has-unseen");
        }
      };
      update();
      new MutationObserver(update).observe(panel, {
        childList: true,
        characterData: true,
        subtree: true,
      });
    });
  }

  function initDock(dock) {
    const tabs = Array.from(dock.querySelectorAll("[data-dock-target]"));
    if (!tabs.length) return;

    tabs.forEach((tab, index) => {
      tab.addEventListener("click", () => {
        setDockCollapsed(dock, false);
        activateDockPanel(dock, tab.dataset.dockTarget);
      });
      tab.addEventListener("keydown", (event) => {
        if (event.key !== "ArrowLeft" && event.key !== "ArrowRight") return;
        event.preventDefault();
        const offset = event.key === "ArrowRight" ? 1 : -1;
        const next = tabs[(index + offset + tabs.length) % tabs.length];
        activateDockPanel(dock, next.dataset.dockTarget);
        next.focus();
      });
    });

    const initial = tabs.find((tab) => tab.classList.contains("active")) || tabs[0];
    activateDockPanel(dock, initial.dataset.dockTarget);
    const collapseButton = dock.querySelector("[data-dock-collapse]");
    if (collapseButton) {
      collapseButton.addEventListener("click", () => {
        setDockCollapsed(dock, !dock.classList.contains("is-collapsed"));
      });
    }
    setDockCollapsed(dock, dock.classList.contains("is-collapsed"));
    observeDockOutput(dock);
  }

  document.querySelectorAll("[data-dock]").forEach(initDock);
})();
