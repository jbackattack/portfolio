// Replays the "check run" in the home page hero. Without JavaScript, or with
// reduced motion, the panel stays in its finished, approved state.
(() => {
  const panel = document.querySelector("[data-run]");
  if (!panel) return;

  const rows = [...panel.querySelectorAll(".run__row")];
  const summary = panel.querySelector("[data-run-summary]");
  const replay = panel.querySelector("[data-run-replay]");
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  const total = rows.length;
  const labels = { queued: "Queued", running: "Running", passed: "Passed" };
  let timers = [];

  const setState = (row, state) => {
    row.dataset.state = state;
    row.querySelector(".run__status").textContent = labels[state];
  };

  const showFinished = () => {
    rows.forEach((row) => setState(row, "passed"));
    summary.textContent = `${total} of ${total} checks passed`;
    panel.classList.add("is-approved");
  };

  const play = () => {
    timers.forEach(clearTimeout);
    timers = [];
    panel.classList.remove("is-approved");
    rows.forEach((row) => setState(row, "queued"));
    summary.textContent = `0 of ${total} checks passed`;
    replay.disabled = true;

    let t = 500;
    rows.forEach((row, i) => {
      timers.push(setTimeout(() => setState(row, "running"), t));
      t += 700;
      timers.push(
        setTimeout(() => {
          setState(row, "passed");
          summary.textContent = `${i + 1} of ${total} checks passed`;
        }, t)
      );
      t += 150;
    });

    timers.push(
      setTimeout(() => {
        panel.classList.add("is-approved");
        replay.disabled = false;
      }, t + 200)
    );
  };

  replay.addEventListener("click", () => {
    if (reduceMotion.matches) {
      showFinished();
    } else {
      play();
    }
  });

  if (reduceMotion.matches) {
    showFinished();
  } else {
    play();
  }
})();
