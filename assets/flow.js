// Animates the sales flow: each step lights up in turn, then settles as done.
// Without JavaScript, or with reduced motion, every step stays in its finished state.
(() => {
  const flow = document.querySelector("[data-flow]");
  if (!flow) return;

  const steps = [...flow.querySelectorAll(".flow__step")];
  const replay = document.querySelector("[data-flow-replay]");
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  let timers = [];

  const setState = (step, state) => {
    step.dataset.state = state;
  };

  const showFinished = () => {
    steps.forEach((step) => setState(step, "done"));
  };

  const play = () => {
    timers.forEach(clearTimeout);
    timers = [];
    steps.forEach((step) => setState(step, "idle"));
    replay.disabled = true;

    let t = 400;
    steps.forEach((step) => {
      timers.push(setTimeout(() => setState(step, "active"), t));
      t += 900;
      timers.push(setTimeout(() => setState(step, "done"), t));
      t += 100;
    });
    timers.push(setTimeout(() => { replay.disabled = false; }, t));
  };

  replay.addEventListener("click", () => {
    if (reduceMotion.matches) {
      showFinished();
    } else {
      play();
    }
  });

  if (reduceMotion.matches || !("IntersectionObserver" in window)) {
    showFinished();
    return;
  }

  // Start the animation when the flow scrolls into view.
  const observer = new IntersectionObserver(
    (entries) => {
      if (entries.some((entry) => entry.isIntersecting)) {
        observer.disconnect();
        play();
      }
    },
    { threshold: 0.4 }
  );
  observer.observe(flow);
})();
