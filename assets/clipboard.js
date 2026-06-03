(function () {
  const daxFunctions = new Set([
    "ABS", "ALL", "ALLSELECTED", "ALLEXCEPT", "AVERAGE", "AVERAGEX",
    "BLANK", "CALCULATE", "CALCULATETABLE", "COUNT", "COUNTA", "COUNTAX",
    "COUNTBLANK", "COUNTROWS", "CROSSFILTER", "DATE", "DATEADD", "DATESBETWEEN",
    "DATESINPERIOD", "DATESYTD", "DISTINCT", "DISTINCTCOUNT", "DIVIDE",
    "EARLIER", "FILTER", "FORMAT", "HASONEVALUE", "IF", "ISBLANK",
    "ISFILTERED", "ISINSCOPE", "KEEPFILTERS", "MAX", "MAXX", "MIN", "MINX",
    "RELATED", "RELATEDTABLE", "REMOVEFILTERS", "SAMEPERIODLASTYEAR",
    "SELECTEDVALUE", "SUM", "SUMX", "SWITCH", "TREATAS", "USERELATIONSHIP",
    "VALUES"
  ]);
  const daxKeywords = new Set([
    "AND", "ASC", "BY", "DEFINE", "DESC", "EVALUATE", "FALSE", "IN",
    "MEASURE", "NOT", "OR", "ORDER", "RETURN", "START", "TABLE", "TRUE", "VAR"
  ]);

  function codeLanguage(code) {
    const explicit = code.dataset.lang || "";
    const className = code.className || "";
    const match = className.match(/language-([^\s]+)/i);
    return (explicit || (match && match[1]) || "").toLowerCase();
  }

  function escapeHtml(text) {
    return text
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");
  }

  function span(className, text) {
    return `<span class="${className}">${escapeHtml(text)}</span>`;
  }

  function highlightDax(code) {
    const text = code.textContent;
    let html = "";
    let index = 0;

    while (index < text.length) {
      const rest = text.slice(index);

      if (rest.startsWith("--") || rest.startsWith("//")) {
        const end = text.indexOf("\n", index);
        const next = end === -1 ? text.length : end;
        html += span("dax-comment", text.slice(index, next));
        index = next;
        continue;
      }

      const char = text[index];

      if (char === '"') {
        let next = index + 1;
        while (next < text.length) {
          if (text[next] === '"' && text[next + 1] === '"') {
            next += 2;
          } else if (text[next] === '"') {
            next += 1;
            break;
          } else {
            next += 1;
          }
        }
        html += span("dax-string", text.slice(index, next));
        index = next;
        continue;
      }

      if (char === "'") {
        let next = index + 1;
        while (next < text.length) {
          if (text[next] === "'" && text[next + 1] === "'") {
            next += 2;
          } else if (text[next] === "'") {
            next += 1;
            break;
          } else {
            next += 1;
          }
        }
        html += span("dax-table", text.slice(index, next));
        index = next;
        continue;
      }

      if (char === "[") {
        const end = text.indexOf("]", index + 1);
        const next = end === -1 ? index + 1 : end + 1;
        html += span("dax-identifier", text.slice(index, next));
        index = next;
        continue;
      }

      if (/[0-9]/.test(char)) {
        const match = rest.match(/^[0-9]+(?:\.[0-9]+)?/);
        html += span("dax-number", match[0]);
        index += match[0].length;
        continue;
      }

      if (/[A-Za-z_]/.test(char)) {
        const match = rest.match(/^[A-Za-z_][A-Za-z0-9_]*/);
        const word = match[0];
        const upper = word.toUpperCase();
        const nextNonSpace = text.slice(index + word.length).match(/^\s*(.)/);

        if (daxFunctions.has(upper) && nextNonSpace && nextNonSpace[1] === "(") {
          html += span("dax-function", word);
        } else if (daxKeywords.has(upper)) {
          html += span("dax-keyword", word);
        } else {
          html += escapeHtml(word);
        }

        index += word.length;
        continue;
      }

      html += escapeHtml(char);
      index += 1;
    }

    code.innerHTML = html;
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
    if (!code) {
      return;
    }
    const language = codeLanguage(code);

    if (language === "dax") {
      highlightDax(code);
    }

    if (!["sql", "dax"].includes(language)) {
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
