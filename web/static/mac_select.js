(() => {
  "use strict";

  function buildMacSelect(select) {
    if (select.dataset.macSelectInitialized) return;
    select.dataset.macSelectInitialized = "true";

    // Create wrapper
    const wrapper = document.createElement("div");
    wrapper.className = "mac-select-wrapper";
    
    // Insert wrapper and move select inside it
    select.parentNode.insertBefore(wrapper, select);
    wrapper.appendChild(select);
    select.classList.add("mac-select-hidden");

    // Create Trigger
    const trigger = document.createElement("div");
    trigger.className = "mac-select-trigger " + select.className.replace("mac-select-hidden", "");
    
    const triggerText = document.createElement("span");
    triggerText.className = "mac-select-trigger-text";
    trigger.appendChild(triggerText);

    // Chevron icon
    const chevron = document.createElement("span");
    chevron.innerHTML = `<svg width="10" height="6" viewBox="0 0 10 6" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M1 1L5 5L9 1" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>`;
    chevron.style.marginLeft = "6px";
    chevron.style.opacity = "0.6";
    trigger.appendChild(chevron);

    wrapper.appendChild(trigger);

    // Create Dropdown
    const dropdown = document.createElement("div");
    dropdown.className = "mac-select-dropdown";
    document.body.appendChild(dropdown);

    let isOpen = false;

    function updateTriggerText() {
      const selectedOption = select.options[select.selectedIndex];
      if (selectedOption) {
        triggerText.textContent = selectedOption.textContent;
      }
    }

    function renderOptions() {
      dropdown.innerHTML = "";
      Array.from(select.options).forEach((option, index) => {
        const item = document.createElement("div");
        item.className = "mac-select-option";
        if (index === select.selectedIndex) {
          item.classList.add("is-selected");
        }
        item.textContent = option.textContent;
        
        item.addEventListener("click", (e) => {
          e.stopPropagation();
          select.selectedIndex = index;
          select.dispatchEvent(new Event("change", { bubbles: true }));
          closeDropdown();
        });

        item.addEventListener("mouseenter", () => {
          Array.from(dropdown.children).forEach(child => child.classList.remove("is-active"));
          item.classList.add("is-active");
        });

        dropdown.appendChild(item);
      });
      updateTriggerText();
    }

    function openDropdown() {
      renderOptions();
      // Calculate width to be at least as wide as trigger
      dropdown.style.minWidth = Math.max(trigger.offsetWidth, 120) + "px";
      
      // Calculate space available below and above to decide opening direction
      const rect = wrapper.getBoundingClientRect();
      const spaceBelow = window.innerHeight - rect.bottom;
      const spaceAbove = rect.top;
      
      dropdown.classList.remove("open-up");
      if (spaceBelow < 250 && spaceAbove > spaceBelow) {
        dropdown.classList.add("open-up");
        dropdown.style.top = 'auto';
        dropdown.style.bottom = (window.innerHeight - rect.top + 4) + 'px';
      } else {
        dropdown.style.top = (rect.bottom + 4) + 'px';
        dropdown.style.bottom = 'auto';
      }
      dropdown.style.left = rect.left + 'px';
      
      dropdown.classList.add("is-open");
      isOpen = true;
    }

    function closeDropdown() {
      dropdown.classList.remove("is-open");
      isOpen = false;
    }

    trigger.addEventListener("click", (e) => {
      e.stopPropagation();
      if (isOpen) {
        closeDropdown();
      } else {
        document.querySelectorAll(".mac-select-dropdown.is-open").forEach(d => d.classList.remove("is-open"));
        openDropdown();
      }
    });

    document.addEventListener("click", (e) => {
      if (!wrapper.contains(e.target) && !dropdown.contains(e.target)) {
        closeDropdown();
      }
    });

    select.addEventListener("change", () => {
      updateTriggerText();
    });

    updateTriggerText();
  }

  function init() {
    document.querySelectorAll("select").forEach(buildMacSelect);
  }

  const observer = new MutationObserver((mutations) => {
    mutations.forEach(mutation => {
      mutation.addedNodes.forEach(node => {
        if (node.nodeType === Node.ELEMENT_NODE) {
          if (node.tagName === "SELECT") {
            buildMacSelect(node);
          } else {
            node.querySelectorAll("select").forEach(buildMacSelect);
          }
        }
      });
    });
  });

  observer.observe(document.body, { childList: true, subtree: true });

  window.addEventListener("wheel", () => {
    document.querySelectorAll(".mac-select-dropdown.is-open").forEach(el => {
      el.classList.remove("is-open");
    });
  }, { passive: true });

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
