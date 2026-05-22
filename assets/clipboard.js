(function () {
  function codeLanguage(code) {
    const explicit = code.dataset.lang || "";
    const className = code.className || "";
    const match = className.match(/language-([^\s]+)/i);
    return (explicit || (match && match[1]) || "").toLowerCase();
  }

  document.querySelectorAll("pre:has(code)").forEach(pre => {
    pre.addEventListener("click", pre.focus);
    pre.addEventListener("copy", function (event) {
      event.preventDefault();
      if (navigator.clipboard) {
        const content = window.getSelection().toString() || pre.textContent;
        navigator.clipboard.writeText(content);
      }
    });

    const code = pre.querySelector("code");
    if (!code || codeLanguage(code) !== "sql") {
      return;
    }

    const block = pre.closest(".highlight") || pre;
    const button = document.createElement("button");
    button.type = "button";
    button.className = "book-codeblock-wrap-toggle";
    button.textContent = "Wrap";
    button.setAttribute("aria-pressed", "false");

    button.addEventListener("click", function () {
      const wrapped = block.classList.toggle("is-wrapped");
      button.textContent = wrapped ? "No wrap" : "Wrap";
      button.setAttribute("aria-pressed", String(wrapped));
    });

    block.classList.add("book-codeblock-with-toggle");
    block.insertBefore(button, block.firstChild);
  });
})();
