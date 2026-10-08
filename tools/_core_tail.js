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

