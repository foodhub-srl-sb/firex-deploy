(function () {
  var slides = Array.prototype.slice.call(document.querySelectorAll('.slide'));
  var cur = 0, hudTimer;
  var hudN = document.getElementById('hud-n');

  function fit() {
    var overview = document.body.classList.contains('overview');
    var s = overview
      ? Math.min(1, (window.innerWidth - 48) / 1920)
      : Math.min(window.innerWidth / 1920, window.innerHeight / 1080);
    slides.forEach(function (el) {
      if (overview) {
        el.style.transform = '';
        el.style.zoom = s;
      } else {
        el.style.zoom = '';
        el.style.transform = 'translate(-50%, -50%) scale(' + s + ')';
      }
    });
  }

  function show(i) {
    cur = Math.max(0, Math.min(slides.length - 1, i));
    slides.forEach(function (el, k) { el.classList.toggle('active', k === cur); });
    hudN.textContent = (cur + 1) + ' / ' + slides.length;
    if (location.hash !== '#' + (cur + 1)) history.replaceState(null, '', '#' + (cur + 1));
    document.body.classList.add('show-hud');
    clearTimeout(hudTimer);
    hudTimer = setTimeout(function () { document.body.classList.remove('show-hud'); }, 1400);
  }

  document.addEventListener('keydown', function (e) {
    var k = e.key;
    if (k === 'ArrowRight' || k === 'PageDown' || k === ' ' || k === 'Enter') { show(cur + 1); e.preventDefault(); }
    else if (k === 'ArrowLeft' || k === 'PageUp' || k === 'Backspace') { show(cur - 1); e.preventDefault(); }
    else if (k === 'Home') show(0);
    else if (k === 'End') show(slides.length - 1);
    else if (k === 'f' || k === 'F') {
      if (document.fullscreenElement) document.exitFullscreen();
      else document.documentElement.requestFullscreen && document.documentElement.requestFullscreen();
    } else if (k === 'o' || k === 'O') {
      document.body.classList.toggle('overview');
      fit();
      if (!document.body.classList.contains('overview')) show(cur);
    }
  });

  document.addEventListener('click', function (e) {
    if (document.body.classList.contains('overview')) {
      var el = e.target.closest('.slide');
      if (el) { document.body.classList.remove('overview'); fit(); show(slides.indexOf(el)); }
      return;
    }
    show(e.clientX < window.innerWidth / 3 ? cur - 1 : cur + 1);
  });

  var tx = null;
  document.addEventListener('touchstart', function (e) { tx = e.touches[0].clientX; }, { passive: true });
  document.addEventListener('touchend', function (e) {
    if (tx === null) return;
    var dx = e.changedTouches[0].clientX - tx;
    if (Math.abs(dx) > 40) show(dx < 0 ? cur + 1 : cur - 1);
    tx = null;
  });

  window.addEventListener('resize', fit);
  window.addEventListener('beforeprint', function () { slides.forEach(function (el) { el.style.zoom = ''; }); });
  window.addEventListener('afterprint', fit);
  fit();
  show((parseInt(location.hash.slice(1), 10) || 1) - 1);
})();
