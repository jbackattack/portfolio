// Collapses the long testimonials to their first paragraph, with a toggle to read the rest.
// Without JavaScript, the full recommendations stay visible.
(() => {
  document.querySelectorAll(".quote-card__rest").forEach((rest) => {
    rest.hidden = true;
    const button = document.createElement("button");
    button.type = "button";
    button.className = "quote-card__toggle";
    button.setAttribute("aria-expanded", "false");
    button.setAttribute("aria-controls", rest.id);
    button.textContent = "Read the full recommendation";
    button.addEventListener("click", () => {
      const open = rest.hidden;
      rest.hidden = !open;
      button.setAttribute("aria-expanded", String(open));
      button.textContent = open ? "Show less" : "Read the full recommendation";
    });
    rest.after(button);
  });
})();
