document.addEventListener('DOMContentLoaded', function () {
  var container = document.getElementById('research-list');
  var select = document.getElementById('sort-select');
  if (!container || !select) return;

  var papers = Array.prototype.slice.call(container.querySelectorAll('.paper-item'));
  var yearSections = Array.prototype.slice.call(container.querySelectorAll('.year-section'));

  // Save original structure: which papers belong to which section, in order
  var sectionPapers = yearSections.map(function (sec) {
    return Array.prototype.slice.call(sec.querySelectorAll('.paper-item'));
  });

  // Flat container for sorted views
  var flatRow = document.createElement('div');
  flatRow.className = 'row';
  flatRow.id = 'flat-sort-row';
  flatRow.style.display = 'none';
  container.appendChild(flatRow);

  function showDefault() {
    flatRow.style.display = 'none';
    flatRow.innerHTML = '';
    papers.forEach(function (p) {
      var metric = p.querySelector('.sort-metric');
      if (metric) metric.remove();
    });
    sectionPapers.forEach(function (items, i) {
      var sec = yearSections[i];
      items.forEach(function (paper) {
        sec.appendChild(paper);
      });
      sec.style.display = '';
    });
  }

  function sortBy(attr, label) {
    yearSections.forEach(function (sec) { sec.style.display = 'none'; });

    var sorted = papers.slice().sort(function (a, b) {
      var va = parseInt(a.getAttribute('data-' + attr)) || 0;
      var vb = parseInt(b.getAttribute('data-' + attr)) || 0;
      if (vb !== va) return vb - va;
      return (b.getAttribute('data-date') || '').localeCompare(a.getAttribute('data-date') || '');
    });

    flatRow.innerHTML = '';
    sorted.forEach(function (paper, i) {
      var numSpan = paper.querySelector('.paper-number');
      if (numSpan) numSpan.textContent = sorted.length - i;

      var existing = paper.querySelector('.sort-metric');
      if (existing) existing.remove();
      var val = parseInt(paper.getAttribute('data-' + attr)) || 0;
      if (val > 0) {
        var metricSpan = document.createElement('span');
        metricSpan.className = 'sort-metric';
        metricSpan.textContent = label + ': ' + val.toLocaleString();
        var titleLink = paper.querySelector('.paper-title');
        if (titleLink && titleLink.parentNode) {
          titleLink.parentNode.insertBefore(metricSpan, titleLink.nextSibling);
        }
      }

      flatRow.appendChild(paper);
    });

    flatRow.style.display = '';
  }

  select.addEventListener('change', function () {
    var mode = select.value;
    if (mode === 'default') {
      showDefault();
    } else if (mode === 'citations') {
      sortBy('citations', 'Citations');
    } else if (mode === 'stars') {
      sortBy('stars', 'Stars');
    }
  });
});
