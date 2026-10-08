/* ============================================================
 * Paper_Interaction core v5.1 — 覆盖片断
 * 1) 大纲：章 → 节 → 卡 三级，可折叠；编号在节内部（1.1 / 1.2），不整体累计
 * 2) 原 PDF 对照栏：左卡右页，双向跳转；卡声明的矩形在页面上高亮
 * 铁律: 0 反引号 / 无 IIFE / 全局函数 / addEventListener
 * ============================================================ */

/* ---------- 大纲：章 → 节 → 卡，可折叠 ---------- */
function outlineState() {
  try {
    var raw = localStorage.getItem('pi-outline-' + PI.slug);
    if (raw) { return JSON.parse(raw); }
  } catch (e) { }
  return { closed: {} };
}
function saveOutlineState(st) {
  try { localStorage.setItem('pi-outline-' + PI.slug, JSON.stringify(st)); } catch (e) { }
}
function outlineKey(kind, a, b) { return kind + '|' + a + '|' + b; }
function makeToggleGroup(li, key) {
  return function (ev) {
    if (ev) { ev.stopPropagation(); }
    var st = outlineState();
    var body = li.querySelector('.ol-body');
    var isClosed = body.classList.toggle('closed');
    li.classList.toggle('closed', isClosed);
    st.closed[key] = isClosed;
    saveOutlineState(st);
  };
}
function rebuildOutline() {
  var ol = piGet('outlineList');
  if (!ol) { return; }
  ol.innerHTML = '';
  var st = outlineState();
  var i, card, chap, sec, li, body, head, arrow, curChap, curSec, chapLi, secLi;
  curChap = null; curSec = null;
  chapLi = null; secLi = null;
  var chapCount = 0, secCount = 0;
  for (i = 0; i < PI.cards.length; i++) {
    card = PI.cards[i];
    chap = card.getAttribute('data-chapter') || '';
    sec = card.getAttribute('data-sec-num') || '';
    if (chap !== curChap) {
      curChap = chap;
      curSec = null;
      chapCount++;
      var cnum = card.getAttribute('data-chapter-num') || '';
      var cname = chap === 'Start here' ? '' : (cnum === '0' ? '' : cnum + ' ');
      li = document.createElement('li');
      li.className = 'ol-chap';
      head = document.createElement('div');
      head.className = 'ol-head';
      arrow = document.createElement('span');
      arrow.className = 'ol-arrow';
      arrow.textContent = '▾';
      head.appendChild(arrow);
      var lbl = document.createElement('span');
      lbl.className = 'ol-label';
      lbl.textContent = cname + chap;
      head.appendChild(lbl);
      li.appendChild(head);
      body = document.createElement('ul');
      body.className = 'ol-body';
      li.appendChild(body);
      ol.appendChild(li);
      chapLi = body;
      var ckey = outlineKey('c', chapCount, chap);
      head.addEventListener('click', makeToggleGroup(li, ckey));
      if (st.closed[ckey]) { li.classList.add('closed'); body.classList.add('closed'); }
    }
    if (sec !== curSec) {
      curSec = sec;
      secCount = (secLi && secLi.parentNode) ? secCount : 0;
      li = document.createElement('li');
      li.className = 'ol-sec';
      head = document.createElement('div');
      head.className = 'ol-head';
      arrow = document.createElement('span');
      arrow.className = 'ol-arrow';
      arrow.textContent = '▾';
      head.appendChild(arrow);
      var sl = document.createElement('span');
      sl.className = 'ol-label';
      var sname = card.getAttribute('data-section') || '';
      sl.textContent = sname || 'Cards';
      head.appendChild(sl);
      li.appendChild(head);
      body = document.createElement('ul');
      body.className = 'ol-body';
      li.appendChild(body);
      chapLi.appendChild(li);
      secLi = body;
      var skey = outlineKey('s', curChap, sec);
      head.addEventListener('click', makeToggleGroup(li, skey));
      if (st.closed[skey]) { li.classList.add('closed'); body.classList.add('closed'); }
    }
    li = document.createElement('li');
    li.className = 'ol-card';
    li.setAttribute('data-idx', String(i));
    li.textContent = card.getAttribute('data-title') || ('Card ' + (i + 1));
    if (card.getAttribute('data-pdf')) {
      var pgb = document.createElement('span');
      pgb.className = 'ol-pg';
      pgb.textContent = 'p.' + card.getAttribute('data-pdf');
      li.appendChild(pgb);
    }
    li.addEventListener('click', makeOutlineGo(i));
    secLi.appendChild(li);
  }
  markOutlineHere();
}
function markOutlineHere() {
  var items = piGet('outlineList').querySelectorAll('li[data-idx]');
  var i, li, open = null;
  for (i = 0; i < items.length; i++) {
    li = items[i];
    if (parseInt(li.getAttribute('data-idx'), 10) === PI.cur) {
      li.classList.add('here');
      open = li;
    } else { li.classList.remove('here'); }
  }
  if (open) {
    var n = open.parentNode;
    while (n && n.id !== 'outlineList') {
      if (n.classList && n.classList.contains('closed')) {
        n.classList.remove('closed');
        var st = outlineState();
        var sib = n.parentNode;
        if (sib && sib.classList) { sib.classList.remove('closed'); }
      }
      n = n.parentNode;
    }
  }
  var cnt = piGet('outlineCount');
  if (cnt) { cnt.textContent = (PI.cur + 1) + ' / ' + PI.cards.length; }
}
function setAllGroups(closed) {
  var boxes = piGet('outlineList').querySelectorAll('.ol-body');
  var i, st = outlineState();
  for (i = 0; i < boxes.length; i++) {
    if (closed) { boxes[i].classList.add('closed'); boxes[i].parentNode.classList.add('closed'); }
    else { boxes[i].classList.remove('closed'); boxes[i].parentNode.classList.remove('closed'); }
  }
  st.closed = {};
  if (closed) {
    var heads = piGet('outlineList').querySelectorAll('li.ol-chap, li.ol-sec');
    for (i = 0; i < heads.length; i++) { heads[i].classList.add('closed'); }
  }
  saveOutlineState(st);
}

/* ---------- 原 PDF 对照栏 ---------- */
var PP = { on: false, pages: {}, ratio: 1, pageW: 0 };

function paperInit() {
  var pane = piGet('paperPane');
  if (!pane) { return; }
  var imgs = pane.querySelectorAll('.pg img');
  var i;
  for (i = 0; i < imgs.length; i++) {
    var wrap = imgs[i].parentNode;
    PP.pages[wrap.getAttribute('data-page')] = wrap;
    wrap.addEventListener('click', makePageClick(wrap));
  }
  var first = pane.querySelector('.pg img');
  if (first) {
    first.addEventListener('load', function () { paperMeasure(); });
    if (first.complete) { paperMeasure(); }
  }
  var btn = piGet('paperBtn');
  if (btn) { btn.addEventListener('click', paperToggle); }
  if (paperNarrow()) { pane.classList.add('hidden'); }
}
function paperMeasure() {
  var pane = piGet('paperPane');
  if (!pane) { return; }
  var img = pane.querySelector('.pg img');
  if (!img || !img.naturalWidth) { return; }
  PP.pageW = img.clientWidth || img.offsetWidth;
  PP.ratio = PP.pageW / img.naturalWidth;
}
function paperNarrow() { return window.innerWidth < 1180; }
function paperToggle() {
  var pane = piGet('paperPane');
  if (!pane) { return; }
  PP.on = !PP.on;
  if (PP.on && paperNarrow()) {
    alert('The paper pane needs a wider window (1180px or more). Widen the window or the pane will cover the cards.');
  }
  document.body.classList.toggle('paper-open', PP.on);
  pane.classList.toggle('hidden', !PP.on);
  var btn = piGet('paperBtn');
  if (btn) { btn.setAttribute('aria-pressed', PP.on ? 'true' : 'false'); }
  if (PP.on) { paperMeasure(); paperSync(); }
}
function paperSync() {
  if (!PP.on) { return; }
  var pane = piGet('paperPane');
  var card = PI.cards[PI.cur];
  if (!pane || !card) { return; }
  var pg = card.getAttribute('data-pdf');
  var i, all = pane.querySelectorAll('.pg');
  for (i = 0; i < all.length; i++) { all[i].classList.remove('current'); }
  var hl = pane.querySelectorAll('.pg-hl');
  for (i = 0; i < hl.length; i++) { hl[i].hidden = true; hl[i].style.cssText = ''; }
  if (!pg) { return; }
  var box = PP.pages[pg];
  if (!box) { return; }
  box.classList.add('current');
  var rect = card.getAttribute('data-pdf-rect');
  var img = box.querySelector('img');
  if (rect && img) {
    var r = rect.split(',');
    var sc = (img.clientWidth || PP.pageW) / img.naturalWidth;
    var h = box.querySelector('.pg-hl');
    h.hidden = false;
    h.style.left = (parseFloat(r[0]) * sc) + 'px';
    h.style.top = (parseFloat(r[1]) * sc) + 'px';
    h.style.width = ((parseFloat(r[2]) - parseFloat(r[0])) * sc) + 'px';
    h.style.height = ((parseFloat(r[3]) - parseFloat(r[1])) * sc) + 'px';
  }
  var top = box.offsetTop - 12;
  pane.scrollTop = Math.max(0, top);
}
function makePageClick(box) {
  return function () {
    var pg = box.getAttribute('data-page');
    var i, c;
    for (i = 0; i < PI.cards.length; i++) {
      c = PI.cards[i];
      if (c.getAttribute('data-pdf') === pg) { goCard(i); return; }
    }
  };
}
