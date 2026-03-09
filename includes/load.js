(function () {
  var script = document.currentScript;
  var base = script.src.replace(/\/[^/]*$/, '/');
  var headerEl = document.getElementById('site-header');
  var footerEl = document.getElementById('site-footer');

  function setActiveNav(container) {
    if (!container) return;
    var path = location.pathname || '';
    var page = path.slice(path.lastIndexOf('/') + 1) || 'index.html';
    container.querySelectorAll('.nav-links a[href]').forEach(function (a) {
      var href = a.getAttribute('href');
      if (href === page || (page === '' && href === 'index.html')) {
        a.classList.add('is-active');
      }
    });
  }

  function setupMenuToggle(headerNode) {
    if (!headerNode) return;
    var toggle = headerNode.querySelector('.nav-toggle');
    if (!toggle) return;
    toggle.addEventListener('click', function () {
      var open = headerNode.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', open);
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    });
    headerNode.querySelectorAll('.nav-links a').forEach(function (a) {
      a.addEventListener('click', function () {
        headerNode.classList.remove('is-open');
        toggle.setAttribute('aria-expanded', 'false');
        toggle.setAttribute('aria-label', 'Open menu');
      });
    });
  }

  function inject(placeholder, url, onDone, tagName) {
    if (!placeholder) return Promise.resolve();
    return fetch(base + url)
      .then(function (r) {
        if (!r.ok) throw new Error(url + ' ' + r.status);
        return r.text();
      })
      .then(function (html) {
        var wrap = document.createElement('div');
        wrap.innerHTML = html.trim();
        var node = wrap.firstChild;
        if (tagName && (!node || node.nodeType !== 1 || node.tagName.toUpperCase() !== tagName.toUpperCase())) {
          return;
        }
        placeholder.parentNode.replaceChild(node, placeholder);
        if (onDone) onDone(node);
      });
  }

  Promise.all([
    inject(headerEl, 'header.html', function (node) {
      setActiveNav(node);
      setupMenuToggle(node);
    }, 'HEADER'),
    inject(footerEl, 'footer.html', null, 'FOOTER')
  ]).catch(function (err) {
    if (typeof console !== 'undefined' && console.error) {
      console.error('PeriSmart includes load failed:', err);
    }
    var fallbackHeader = document.querySelector('.site-header');
    if (fallbackHeader) setupMenuToggle(fallbackHeader);
  });
})();
