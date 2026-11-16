/* Display settings: colour theme + light/dark. No dependencies.
   The choice is saved in the viewer's browser (localStorage). */
(function () {
  var root = document.documentElement;
  var btn = document.getElementById('display-toggle');
  var panel = document.getElementById('display-panel');
  if (!btn || !panel) return;

  function save(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  function apply(name, value) {
    if (name === 'theme') root.setAttribute('data-theme', value);
    else root.setAttribute('data-scheme', value);
    save('site-' + name, value);
  }
  // Tick the saved choices
  ['theme', 'scheme'].forEach(function (name) {
    var cur = root.getAttribute('data-' + name) || (name === 'theme' ? 'crimson' : 'auto');
    var input = panel.querySelector('input[name="' + name + '"][value="' + cur + '"]');
    if (input) input.checked = true;
  });
  panel.addEventListener('change', function (e) {
    if (e.target.name) apply(e.target.name, e.target.value);
  });

  function close() { panel.hidden = true; btn.setAttribute('aria-expanded', 'false'); }
  btn.addEventListener('click', function () {
    var open = panel.hidden;
    panel.hidden = !open;
    btn.setAttribute('aria-expanded', String(open));
    if (open) { var c = panel.querySelector('input:checked'); if (c) c.focus(); }
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && !panel.hidden) { close(); btn.focus(); }
  });
  document.addEventListener('click', function (e) {
    if (!panel.hidden && !panel.contains(e.target) && e.target !== btn) close();
  });
})();
