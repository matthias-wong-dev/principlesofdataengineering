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
      const quoteText = Array.from(quote.querySelectorAll("p"))
        .map((p) => p.textContent.trim())
        .filter(Boolean)
        .join("\n\n");

      const chapterTitle =
        document.querySelector("h1")?.textContent?.trim() || document.title;

      const workTitle = "Principles of Data Engineering";
      const url = `${window.location.origin}${window.location.pathname}#${id}`;

      const shareText = `“${quoteText}”\n\n— ${chapterTitle}, ${workTitle}`;

      try {
        if (navigator.share) {
          await navigator.share({
            title: `${chapterTitle} | ${workTitle}`,
            text: shareText,
            url
          });
        } else {
          await navigator.clipboard.writeText(`${shareText}\n${url}`);
          button.textContent = "Copied";
          setTimeout(() => button.textContent = "Share", 1500);
        }
      } catch {
        // User cancelled native share, or browser blocked it.
      }
    });

    quote.appendChild(button);
  });
});