document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("blockquote").forEach((quote) => {
    const firstP = quote.querySelector("p");
    if (!firstP) return;

    const match = firstP.textContent.match(/^\[!SHARE:([a-z0-9-]+)\]/i);
    if (!match) return;

    const id = match[1];

    quote.id = id;
    quote.classList.add("share-block");

    firstP.textContent = firstP.textContent
      .replace(match[0], "")
      .trim();

    const button = document.createElement("button");
    button.className = "share-quote";
    button.textContent = "Share";

    button.addEventListener("click", async () => {
      const text = quote.innerText.replace("Share", "").trim();
      const url = `${window.location.origin}${window.location.pathname}#${id}`;

      try {
        if (navigator.share) {
          await navigator.share({
            title: document.title,
            text,
            url
          });
        } else {
          await navigator.clipboard.writeText(`${text}\n\n${url}`);
          button.textContent = "Copied";
          setTimeout(() => button.textContent = "Share", 1500);
        }
      } catch {}
    });

    quote.appendChild(button);
  });
});