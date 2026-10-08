/* ============================================================
 * Paper_Interaction shared core v5 (规范源码 — 构建站点时内联)
 * 变更: 去双语（英文单语）/ 章→节→卡 三级大纲 / 卡标题单一字段
 * 铁律: 0 反引号 / 无 IIFE / 全局函数 / addEventListener
 * ============================================================ */

function piGet(id) { return document.getElementById(id); }

/* ---------- 进度管理 ---------- */
function ProgressManager(slug) {
  this.slug = slug;
  this.key = 'pi-progress-' + slug;
}
ProgressManager.prototype.load = function () {
  try {
    var raw = localStorage.getItem(this.key);
    if (raw) { return JSON.parse(raw); }
  } catch (e) { }
  return { card: 0, done: false };
};
ProgressManager.prototype.save = function (state) {
  try { localStorage.setItem(this.key, JSON.stringify(state)); } catch (e) { }
};

/* ---------- 导航引擎 ---------- */
var PI = { cards: [], cur: 0, pm: null, slug: '' };

function goCard(n) {
  if (n < 0) { n = 0; }
  if (n >= PI.cards.length) { n = PI.cards.length - 1; }
  PI.cur = n;
  var i;
  for (i = 0; i < PI.cards.length; i++) {
    if (i === n) { PI.cards[i].classList.add('active'); }
    else { PI.cards[i].classList.remove('active'); }
  }
  piGet('progressFill').style.width = ((n + 1) / PI.cards.length * 100) + '%';
  piGet('pageNum').textContent = (n + 1) + ' / ' + PI.cards.length;
  markOutlineHere();
  piGet('navPrev').disabled = (n === 0);
  piGet('navNext').textContent = (n === PI.cards.length - 1) ? 'Finish ✓' : 'Continue →';
  piGet('cardArea').scrollTop = 0;
  showChapter();
  paperSync();
  PI.pm.save({ card: n, done: (n === PI.cards.length - 1) });
  if (typeof onCardChange === 'function') { onCardChange(n); }
}
function navNext() { goCard(PI.cur + 1); }
function navPrev() { goCard(PI.cur - 1); }
function toggleOutline() {
  piGet('outline').classList.toggle('open');
  document.body.classList.toggle('outline-open');
}

/* ---------- 顶栏当前章 ---------- */
function showChapter() {
  var el = piGet('chapStrip');
  if (!el || !PI.cards[PI.cur]) { return; }
  var c = PI.cards[PI.cur];
  var num = c.getAttribute('data-chapter-num') || '';
  var name = c.getAttribute('data-chapter') || '';
  var sec = c.getAttribute('data-section') || '';
  el.innerHTML = '<b>' + num + ' ' + name + '</b>' + (sec ? ' · ' + sec : '');
}

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
  var fresh = !st.init;
  if (fresh) { st.init = true; st.closed = {}; }
  var i, card, chap, sec, li, body, head, arrow, curChap, curSec, chapLi, secLi;
  curChap = null; curSec = null;
  chapLi = null; secLi = null;
  var chapCount = 0, secCount = 0;
  var chapOf = {};
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
      if (fresh) {
        st.closed[ckey] = true;
        chapOf[i] = ckey;
      }
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
      if (fresh) { st.closed[skey] = true; }
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
  if (fresh) { saveOutlineState(st); }
  markOutlineHere(true);
}
function markOutlineHere(first) {
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
    var st = outlineState();
    var n = open.parentNode;
    while (n && n.id !== 'outlineList') {
      if (n.classList && n.classList.contains('closed')) {
        n.classList.remove('closed');
        if (n.parentNode && n.parentNode.classList) {
          n.parentNode.classList.remove('closed');
          var h = n.parentNode.querySelector('.ol-head');
          if (h && h.parentNode.classList) { n.parentNode.classList.remove('closed'); }
        }
      }
      n = n.parentNode;
    }
    /* 收起其它章，保持大纲可读；当前章保持打开 */
    var chaps = piGet('outlineList').children;
    var k;
    for (k = 0; k < chaps.length; k++) {
      var b = chaps[k].querySelector('.ol-body');
      if (!b) { continue; }
      var inside = chaps[k].contains(open);
      if (!inside && !b.classList.contains('closed')) {
        b.classList.add('closed'); chaps[k].classList.add('closed');
      }
    }
    saveOutlineState(st);
    if (first || piGet('outline').classList.contains('open')) {
      try { open.scrollIntoView({ block: 'center' }); } catch (e) { }
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

/* ---------- 原论文对照栏：一次一段，衬线白底，图表随卡 ---------- */
var PP = { on: false, flat: [], cur: 0, fromCard: true };

function escHtml(t) {
  return String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}
function paperInit() {
  var pane = piGet('paperPane');
  var btn0 = piGet('paperBtn');
  if (!pane) {
    /* 镜像若剥掉了论文：没有对照栏，隐藏按钮 */
    if (btn0) { btn0.style.display = 'none'; }
    return;
  }
  var ps = pane.querySelectorAll('#paperPages .pb');
  var i;
  for (i = 0; i < ps.length; i++) { PP.flat.push(ps[i]); }
  piGet('ppPrev').addEventListener('click', function () { paperStep(-1); });
  piGet('ppNext').addEventListener('click', function () { paperStep(1); });
  piGet('ppSync').addEventListener('click', function () { PP.fromCard = true; paperSync(); });
  if (btn0) { btn0.addEventListener('click', paperToggle); }
}
function paperNarrow() { return window.innerWidth < 1024; }
function paperToggle() {
  var pane = piGet('paperPane');
  if (!pane) { return; }
  if (!PP.on && paperNarrow()) {
    alert('The paper pane needs a wider window (1024px or more).');
    return;
  }
  PP.on = !PP.on;
  document.body.classList.toggle('paper-open', PP.on);
  pane.classList.toggle('hidden', !PP.on);
  var btn = piGet('paperBtn');
  if (btn) { btn.setAttribute('aria-pressed', PP.on ? 'true' : 'false'); }
  if (PP.on) { PP.fromCard = true; paperSync(); }
}
function paperSync() {
  if (!PP.on) { return; }
  var card = PI.cards[PI.cur];
  if (!card) { return; }
  var pg = card.getAttribute('data-pdf');
  var idx = -1;
  var frag = card.getAttribute('data-pdf-rect');
  if (frag) {
    var pp = frag.split(':');
    var el = piGet('paperPages').querySelector('.pb[data-page="' + pp[0] + '"][data-b="' + pp[1] + '"]');
    if (el) { idx = PP.flat.indexOf(el); }
  }
  if (idx < 0 && pg) {
    for (var i = 0; i < PP.flat.length; i++) {
      if (PP.flat[i].getAttribute('data-page') === pg) { idx = i; break; }
    }
  }
  if (idx < 0) { idx = 0; }
  var quote = card.getAttribute('data-quote') || '';
  /* 背景卡（拓展小节等）不对应某一处原文：说明清楚，而不是塞一段无关的话 */
  if (!card.getAttribute('data-clip') && !quote) {
    PP.cur = idx;
    piGet('ppBody').innerHTML = '<p class="pp-note">This card is <b>background material</b> — it builds a general idea '
      + 'rather than reading one passage of the paper, so there is no passage to put here. Cards that do read a passage '
      + 'show it here as a screenshot from the paper. You can still walk the paper itself with the arrows below.</p>';
    piGet('ppTag').textContent = '—';
    var fb = piGet('ppFig');
    fb.hidden = true; fb.innerHTML = '';
    piGet('ppPrev').disabled = (idx === 0);
    piGet('ppNext').disabled = (idx === PP.flat.length - 1);
    return;
  }
  /* 图表：卡里内嵌的原图直接克隆过来 */
  var figBox = piGet('ppFig');
  figBox.innerHTML = '';
  var im = card.querySelector('.figbox img');
  var cap = card.querySelector('.figcap');
  var ckey = card.getAttribute('data-clip');
  var clip = ckey ? piGet('paperPages').querySelector('img[data-clip="' + ckey.replace(/"/g, '') + '"]') : null;
  if (clip) {
    /* 首选：那一段的原 PDF 截图（关键词已高亮） */
    var cl = clip.cloneNode(false);
    cl.style.width = '100%';
    figBox.innerHTML = '';
    figBox.appendChild(cl);
    if (cap) {
      var cp = document.createElement('div');
      cp.className = 'pp-figcap';
      cp.textContent = cap.textContent;
      figBox.appendChild(cp);
    }
    var tag = document.createElement('div');
    tag.className = 'pp-figcap';
    tag.textContent = 'Screenshot from the paper, page ' + card.getAttribute('data-pdf') + ' — keywords highlighted.';
    figBox.appendChild(tag);
    figBox.hidden = false;
  } else if (im) {
    var cl2 = im.cloneNode(true);
    cl2.style.width = '100%';
    figBox.innerHTML = '';
    figBox.appendChild(cl2);
    if (cap) {
      var cp2 = document.createElement('div');
      cp2.className = 'pp-figcap';
      cp2.textContent = cap.textContent;
      figBox.appendChild(cp2);
    }
    figBox.hidden = false;
  } else { figBox.hidden = true; figBox.innerHTML = ''; }
  showPassage(idx, quote, true);
}
function showPassage(idx, quote, withFig) {
  if (idx < 0) { idx = 0; }
  if (idx >= PP.flat.length) { idx = PP.flat.length - 1; }
  PP.cur = idx;
  var src = PP.flat[idx];
  var t = src.textContent.replace(/\s+/g, ' ').trim();
  var html = escHtml(t);
  if (quote) {
    var qi = t.toUpperCase().indexOf(String(quote).toUpperCase());
    if (qi >= 0) {
      html = escHtml(t.slice(0, qi))
           + '<span class="pp-mark">' + escHtml(t.slice(qi, qi + quote.length)) + '</span>'
           + escHtml(t.slice(qi + quote.length));
    }
  }
  piGet('ppBody').innerHTML = '<p class="pp-lead">' + html + '</p>';
  piGet('ppTag').textContent = 'p.' + src.getAttribute('data-page');
  var figBox = piGet('ppFig');
  if (!withFig) { figBox.hidden = true; figBox.innerHTML = ''; }
  piGet('ppPrev').disabled = (idx === 0);
  piGet('ppNext').disabled = (idx === PP.flat.length - 1);
  var body = piGet('ppBody');
  body.scrollTop = 0;
}
function paperStep(dir) {
  PP.fromCard = false;
  showPassage(PP.cur + dir, '', false);
}

/* ---------- 闭包工厂（替代 IIFE） ---------- */
function makeOutlineGo(idx) {
  return function () {
    goCard(idx);
    toggleOutline();
  };
}
function makeQuizHandler(btn, q) {
  return function () {
    if (q.classList.contains('answered')) { return; }
    var expl = q.querySelector('.expl');
    if (btn.getAttribute('data-correct') === '1') {
      q.classList.add('answered');
      btn.classList.add('right');
      expl.innerHTML = '<b>✓ Correct.</b> ' + btn.getAttribute('data-expl');
      expl.classList.add('show', 'good');
    } else {
      btn.classList.add('wrong');
      btn.disabled = true;
      expl.innerHTML = '<b>✗ Not quite.</b> ' + btn.getAttribute('data-expl');
      expl.classList.add('show', 'bad');
    }
  };
}
function makeStepHandler(box, button, list) {
  return function () {
    if (!box._stepIdx) { box._stepIdx = 0; }
    if (box._stepIdx < list.length - 1) {
      box._stepIdx = box._stepIdx + 1;
      list[box._stepIdx].classList.remove('hidden');
      button.textContent = (box._stepIdx === list.length - 1) ? '↻ Restart' : 'Next step →';
    } else {
      var j;
      for (j = 1; j < list.length; j++) { list[j].classList.add('hidden'); }
      box._stepIdx = 0;
      button.textContent = 'Next step →';
    }
  };
}
function makeRevealHandler(box) {
  return function () { box.classList.add('open'); };
}

/* ---------- 单选习题引擎 ---------- */
function initQuizzes() {
  var quizzes = document.querySelectorAll('.quiz:not(.quiz-num):not(.quiz-multi)');
  var qi, oi, quiz, opts, opt;
  for (qi = 0; qi < quizzes.length; qi++) {
    quiz = quizzes[qi];
    opts = quiz.querySelectorAll('.opt');
    for (oi = 0; oi < opts.length; oi++) {
      opt = opts[oi];
      opt.addEventListener('click', makeQuizHandler(opt, quiz));
    }
  }
}

/* ---------- 数值题引擎 ----------
 * <div class="quiz quiz-num" data-answer="40" data-tol="0.5"
 *      data-hint="常见错误提示" data-sol="完整解答">
 *   <p class="quiz-q">…</p>
 *   <div class="numrow"><input class="numin"><button class="numbtn">Check</button></div>
 *   <div class="expl"></div>
 * </div> ----------------------------------------------------- */
function makeNumHandler(q) {
  return function () {
    if (q.classList.contains('answered')) { return; }
    var inp = q.querySelector('.numin');
    var expl = q.querySelector('.expl');
    var raw = (inp.value || '').replace(/[^\d.\-eE]/g, '');
    var x = parseFloat(raw);
    var ans = parseFloat(q.getAttribute('data-answer'));
    var tol = parseFloat(q.getAttribute('data-tol') || '0.0001');
    if (isNaN(x)) {
      expl.innerHTML = '<b>✗</b> Enter a number first.';
      expl.className = 'expl show bad';
      return;
    }
    if (Math.abs(x - ans) <= tol) {
      q.classList.add('answered');
      inp.disabled = true;
      expl.innerHTML = '<b>✓ Correct!</b> ' + (q.getAttribute('data-sol') || '');
      expl.className = 'expl show good';
    } else {
      var hint = q.getAttribute('data-hint');
      expl.innerHTML = '<b>✗ Try again.</b> ' + (hint ? hint : 'Check units and every factor in the formula.');
      expl.className = 'expl show bad';
    }
  };
}
function initNumQuizzes() {
  var qs = document.querySelectorAll('.quiz-num');
  var i, q, btn;
  for (i = 0; i < qs.length; i++) {
    q = qs[i];
    btn = q.querySelector('.numbtn');
    if (btn) { btn.addEventListener('click', makeNumHandler(q)); }
  }
}

/* ---------- 多选题引擎 (提交式, 可重试) ---------- */
function makeMultiToggle(opt) {
  return function () {
    if (opt.parentNode.parentNode.classList.contains('answered')) { return; }
    opt.classList.toggle('sel');
  };
}
function makeMultiSubmit(q) {
  return function () {
    if (q.classList.contains('answered')) { return; }
    var opts = q.querySelectorAll('.opt');
    var expl = q.querySelector('.expl');
    var ok = true, i, feedback = '';
    for (i = 0; i < opts.length; i++) {
      var sel = opts[i].classList.contains('sel');
      var correct = opts[i].getAttribute('data-correct') === '1';
      if (sel && !correct) {
        ok = false;
        feedback = feedback + '<div><b>✗ ' + opts[i].getAttribute('data-key') + '</b> ' + opts[i].getAttribute('data-expl') + '</div>';
      }
      if (!sel && correct) {
        ok = false;
        feedback = feedback + '<div><b>○ Missed ' + opts[i].getAttribute('data-key') + '</b> ' + opts[i].getAttribute('data-expl') + '</div>';
      }
    }
    if (ok) {
      q.classList.add('answered');
      for (i = 0; i < opts.length; i++) { if (opts[i].getAttribute('data-correct') === '1') { opts[i].classList.add('right'); } }
      expl.innerHTML = '<b>✓ All correct!</b>';
      expl.className = 'expl show good';
    } else {
      for (i = 0; i < opts.length; i++) {
        var s = opts[i].classList.contains('sel');
        var c = opts[i].getAttribute('data-correct') === '1';
        if (s && !c) { opts[i].classList.remove('sel'); }
      }
      expl.innerHTML = '<b>✗ Not yet — retry allowed.</b>' + feedback;
      expl.className = 'expl show bad';
    }
  };
}
function initMultiQuizzes() {
  var qs = document.querySelectorAll('.quiz-multi');
  var i, j, q, opts, btn;
  for (i = 0; i < qs.length; i++) {
    q = qs[i];
    opts = q.querySelectorAll('.opt');
    for (j = 0; j < opts.length; j++) {
      opts[j].addEventListener('click', makeMultiToggle(opts[j]));
    }
    btn = q.querySelector('.mulbtn');
    if (btn) { btn.addEventListener('click', makeMultiSubmit(q)); }
  }
}

/* ---------- 自定义插卡 ----------
 * 存储: localStorage['pi-custom-'+slug] = [{c, title, body, id}]
 * c = 锚点原生卡的 data-c；插到它后面 -------------------- */
function customLoad(slug) {
  try {
    var raw = localStorage.getItem('pi-custom-' + slug);
    if (raw) { return JSON.parse(raw); }
  } catch (e) { }
  return [];
}
function customSave(slug, arr) {
  try { localStorage.setItem('pi-custom-' + slug, JSON.stringify(arr)); } catch (e) { }
}
function openCardEditor(anchorC) {
  var ov = piGet('editorOverlay');
  ov.classList.add('open');
  piGet('edAnchor').value = anchorC;
  piGet('edTitle').value = '';
  piGet('edBody').value = '';
}
function closeCardEditor() { piGet('editorOverlay').classList.remove('open'); }
function makeInsertBtn(card) {
  return function () { openCardEditor(card.getAttribute('data-c')); };
}
function buildCustomCard(item) {
  var sec = document.createElement('section');
  sec.className = 'card custom';
  sec.setAttribute('data-custom-id', item.id);
  sec.setAttribute('data-title', item.title || 'Custom card');
  sec.innerHTML = '<div class="card-inner"><div class="card-kicker">Custom card</div>'
    + '<h2></h2><div class="custom-body">' + item.body + '</div>'
    + '<button class="btn btn-ghost custom-del">Delete this card</button></div>';
  sec.querySelector('h2').textContent = item.title || 'Custom card';
  return sec;
}
function mountCustomCards(slug) {
  var arr = customLoad(slug);
  arr.sort(function (a, b) { return a.c - b.c; });
  var natives = document.querySelectorAll('.card[data-c]');
  var i, k;
  for (i = 0; i < arr.length; i++) {
    for (k = 0; k < natives.length; k++) {
      if (parseInt(natives[k].getAttribute('data-c'), 10) === arr[i].c) {
        natives[k].parentNode.insertBefore(buildCustomCard(arr[i]), natives[k].nextSibling);
        break;
      }
    }
  }
  var dels = document.querySelectorAll('.custom-del');
  for (i = 0; i < dels.length; i++) {
    dels[i].addEventListener('click', makeCustomDelete(dels[i].parentNode.parentNode, slug));
  }
}
function makeCustomDelete(sec, slug) {
  return function () {
    if (!confirm('Delete this custom card?')) { return; }
    var id = sec.getAttribute('data-custom-id');
    var arr = customLoad(slug);
    var out = [], i;
    for (i = 0; i < arr.length; i++) { if (String(arr[i].id) !== String(id)) { out.push(arr[i]); } }
    customSave(slug, out);
    sec.parentNode.removeChild(sec);
    PI.cards = document.querySelectorAll('.card');
    rebuildOutline();
    goCard(Math.max(0, PI.cur - 1));
  };
}
function saveCustomFromEditor(slug) {
  var title = piGet('edTitle').value.replace(/</g, '&lt;');
  var body = piGet('edBody').value;
  if (!title) { alert('A title is required.'); return; }
  if (!body) { alert('Some content is required.'); return; }
  function esc(s) {
    return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/\n\n+/g, '</p><p>').replace(/\n/g, '<br>');
  }
  var item = {
    c: parseInt(piGet('edAnchor').value, 10),
    title: title,
    body: '<p>' + esc(body) + '</p>',
    id: Date.now()
  };
  var arr = customLoad(slug);
  arr.push(item);
  customSave(slug, arr);
  closeCardEditor();
  var anchorCard = document.querySelector('.card[data-c="' + item.c + '"]');
  if (anchorCard) {
    var sec = buildCustomCard(item);
    anchorCard.parentNode.insertBefore(sec, anchorCard.nextSibling);
    sec.querySelector('.custom-del').addEventListener('click', makeCustomDelete(sec, slug));
    PI.cards = document.querySelectorAll('.card');
    rebuildOutline();
    var idx = Array.prototype.indexOf.call(PI.cards, sec);
    goCard(idx);
  }
}

/* ---------- 折叠揭示 / 步进器 ---------- */
function initSteppers() {
  var sts = document.querySelectorAll('.stepper');
  var si, st, btn, steps;
  for (si = 0; si < sts.length; si++) {
    st = sts[si];
    steps = st.querySelectorAll('.step');
    var k;
    for (k = 1; k < steps.length; k++) { steps[k].classList.add('hidden'); }
    btn = st.querySelector('.step-btn');
    if (!btn) { continue; }
    btn.addEventListener('click', makeStepHandler(st, btn, steps));
  }
}
function initReveals() {
  var rvs = document.querySelectorAll('.reveal');
  var ri, rv, btn;
  for (ri = 0; ri < rvs.length; ri++) {
    rv = rvs[ri];
    btn = rv.querySelector('.reveal-btn');
    if (!btn) { continue; }
    btn.addEventListener('click', makeRevealHandler(rv));
  }
}

/* ---------- 初始化 ---------- */
function initCore(slug) {
  PI.slug = slug;
  PI.pm = new ProgressManager(slug);
  mountCustomCards(slug);
  PI.cards = document.querySelectorAll('.card');
  rebuildOutline();
  piGet('navPrev').addEventListener('click', navPrev);
  piGet('navNext').addEventListener('click', navNext);
  piGet('menuBtn').addEventListener('click', toggleOutline);
  piGet('outlineClose').addEventListener('click', toggleOutline);
  piGet('scrim').addEventListener('click', toggleOutline);
  if (piGet('expandAll')) { piGet('expandAll').addEventListener('click', function () { setAllGroups(false); }); }
  if (piGet('collapseAll')) { piGet('collapseAll').addEventListener('click', function () { setAllGroups(true); }); }
  paperInit();
  /* 深链：?paper=1 打开对照栏；#outline 打开大纲 */
  if (location.search.indexOf('paper=1') >= 0) { paperToggle(); }
  if (location.hash === '#outline' || location.search.indexOf('outline=1') >= 0) { toggleOutline(); }
  piGet('edSave').addEventListener('click', function () { saveCustomFromEditor(slug); });
  piGet('edCancel').addEventListener('click', closeCardEditor);
  document.addEventListener('keydown', function (ev) {
    if (ev.target && (ev.target.tagName === 'INPUT' || ev.target.tagName === 'TEXTAREA')) { return; }
    if (ev.key === 'ArrowRight' || ev.key === 'd' || ev.key === 'D') { navNext(); }
    if (ev.key === 'ArrowLeft' || ev.key === 'a' || ev.key === 'A') { navPrev(); }
    if (ev.key === 'p' || ev.key === 'P') { paperToggle(); }
  });
  /* 每张原生卡挂 ✚ 插卡按钮 */
  var i;
  for (i = 0; i < PI.cards.length; i++) {
    if (PI.cards[i].getAttribute('data-c') === null) { continue; }
    var ib = document.createElement('button');
    ib.className = 'insert-btn';
    ib.setAttribute('title', 'Insert your own card after this one');
    ib.textContent = '＋ Add card';
    ib.addEventListener('click', makeInsertBtn(PI.cards[i]));
    PI.cards[i].querySelector('.card-inner').appendChild(ib);
  }
  /* 恢复进度 / 锚点跳转 */
  var h = location.hash || '';
  var st = PI.pm.load();
  var target = st.card || 0;
  if (h.indexOf('#kp-') === 0 || h.indexOf('#c-') === 0) {
    for (i = 0; i < PI.cards.length; i++) {
      if (h === '#' + PI.cards[i].getAttribute('data-kp') || h === '#c-' + PI.cards[i].getAttribute('data-c')) {
        target = i; break;
      }
    }
  }
  goCard(target);
}

