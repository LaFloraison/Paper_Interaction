/* ============ 实验台 1 · 超图平滑沙盒（式 1） ============
 * 4 个顶点，超边 e1={1,2} e2={2,3} e3={3,4} 固定，e4={1,2,3} 可选。
 * 施加 X <- Dv^-1/2 H De^-1 H^T Dv^-1/2 X（W = I，Θ = I，不含 σ）。
 * ======================================================== */

var LAB1_EDGES = [[0, 1], [1, 2], [1, 3]];   // star: e1={1,2} e2={2,3} e3={2,4}
var LAB1_EXTRA = [0, 1, 2];
var LAB1_N = 4;

function lab1Sets(extraOn) {
  var sets = [], e;
  for (e = 0; e < LAB1_EDGES.length; e++) { sets.push(LAB1_EDGES[e]); }
  if (extraOn) { sets.push(LAB1_EXTRA); }
  return sets;
}

function lab1Step(xs, extraOn) {
  var sets = lab1Sets(extraOn), n = LAB1_N, m = sets.length;
  var H = [], i, j, e;
  for (i = 0; i < n; i++) {
    var row = [];
    for (j = 0; j < m; j++) { row.push(sets[j].indexOf(i) >= 0 ? 1 : 0); }
    H.push(row);
  }
  var dv = [], de = [];
  for (i = 0; i < n; i++) {
    var s = 0;
    for (j = 0; j < m; j++) { s += H[i][j]; }
    dv.push(s);
  }
  for (j = 0; j < m; j++) {
    var t = 0;
    for (i = 0; i < n; i++) { t += H[i][j]; }
    de.push(t);
  }
  var a = [];
  for (i = 0; i < n; i++) { a.push(xs[i] / Math.sqrt(dv[i])); }
  var b = [];
  for (j = 0; j < m; j++) {
    var acc = 0;
    for (i = 0; i < n; i++) { acc += H[i][j] * a[i]; }
    b.push(de[j] > 0 ? acc / de[j] : 0);
  }
  var c = [];
  for (i = 0; i < n; i++) {
    var acc2 = 0;
    for (j = 0; j < m; j++) { acc2 += H[i][j] * b[j]; }
    c.push(acc2);
  }
  var out = [];
  for (i = 0; i < n; i++) { out.push(c[i] / Math.sqrt(dv[i])); }
  return { out: out, dv: dv, de: de };
}

function lab1Render() {
  var xs = [], i;
  for (i = 0; i < LAB1_N; i++) { xs.push(parseFloat(piGet('lab1x' + i).value)); }
  var extra = piGet('lab1extra').checked;
  var st = piGet('lab1state');
  var raw = st.getAttribute('data-vec');
  var vec = raw ? JSON.parse(raw) : xs.slice(0);
  var steps = parseInt(st.getAttribute('data-steps'), 10) || 0;

  var lo = Math.min.apply(null, vec), hi = Math.max.apply(null, vec);
  var bars = '';
  for (i = 0; i < LAB1_N; i++) {
    bars += '<div class="hg-row"><span class="hg-vertex">v' + (i + 1) + '</span>'
         +  '<span class="hg-val">' + vec[i].toFixed(3) + '</span>'
         +  '<div class="bar-wrap"><div class="bar-fill" style="width:'
         +  Math.max(0, Math.min(100, vec[i] * 8)) + '%"></div></div></div>';
  }
  piGet('lab1bars').innerHTML = bars;

  var info = lab1Step(vec, extra);
  piGet('lab1deg').innerHTML = 'vertex degrees (' + info.dv.join(', ') + ') &nbsp;·&nbsp; '
                             + 'hyperedge degrees (' + info.de.join(', ') + ')';
  piGet('lab1range').innerHTML = 'range = ' + (hi - lo).toFixed(3)
                              + ' &nbsp;·&nbsp; step ' + steps;
  var eList = 'e1={1,2} e2={2,3} e3={2,4}' + (extra ? ' e4={1,2,3}' : '');
  piGet('lab1edges').innerHTML = 'hyperedges: ' + eList;
}

function makeLab1Slide(i) {
  return function () {
    piGet('lab1o' + i).textContent = piGet('lab1x' + i).value;
    piGet('lab1state').removeAttribute('data-vec');
    piGet('lab1state').setAttribute('data-steps', '0');
    lab1Render();
  };
}

function makeLab1Step() {
  return function () {
    var st = piGet('lab1state');
    var raw = st.getAttribute('data-vec');
    var vec = [], i;
    if (raw) { vec = JSON.parse(raw); }
    else { for (i = 0; i < LAB1_N; i++) { vec.push(parseFloat(piGet('lab1x' + i).value)); } }
    var res = lab1Step(vec, piGet('lab1extra').checked);
    st.setAttribute('data-vec', JSON.stringify(res.out));
    st.setAttribute('data-steps', String((parseInt(st.getAttribute('data-steps'), 10) || 0) + 1));
    lab1Render();
  };
}

function makeLab1Reset() {
  return function () {
    var st = piGet('lab1state');
    st.removeAttribute('data-vec');
    st.setAttribute('data-steps', '0');
    lab1Render();
  };
}

function makeLab1Extra() { return function () { makeLab1Reset()(); }; }

/* ============ 实验台 2 · TDR 规则流水线（式 4–8） ============
 * 两棵树（图 2）：T1: x2>=2@d0, x1>=1@d1 ; T2: x3>=5@d0, x1>=2@d1, x2>=1@d1
 * ========================================================== */

var LAB2_TREES = [
  [{ f: 'x2', t: 2, d: 0 }, { f: 'x1', t: 1, d: 1 }],
  [{ f: 'x3', t: 5, d: 0 }, { f: 'x1', t: 2, d: 1 }, { f: 'x2', t: 1, d: 1 }]
];

function lab2Render() {
  var xs = {
    x1: parseFloat(piGet('lab2x1').value),
    x2: parseFloat(piGet('lab2x2').value),
    x3: parseFloat(piGet('lab2x3').value)
  };
  var a = parseFloat(piGet('lab2alpha').value);
  var b = parseFloat(piGet('lab2beta').value);
  var xsv = 0.9526;

  var chips = '', row = [], ti, ni;
  for (ti = 0; ti < LAB2_TREES.length; ti++) {
    for (ni = 0; ni < LAB2_TREES[ti].length; ni++) {
      var nd = LAB2_TREES[ti][ni];
      var sat = xs[nd.f] >= nd.t;
      var mc = sat ? 0 : 1;
      var mp = a / (nd.d + b);
      var val = mp * mc;
      row.push(val);
      chips += '<span class="rulechip">T' + (ti + 1) + ' ' + nd.f + '&ge;' + nd.t
            + ' <span class="' + (sat ? 'ok' : 'no') + '">'
            + (sat ? 'covered' : 'not covered') + '</span>'
            + ' &mu;p=' + mp.toFixed(3) + ' &rArr; <b>' + val.toFixed(3) + '</b></span>';
    }
  }
  piGet('lab2chips').innerHTML = chips;

  var cells = '', cells2 = '';
  for (ni = 0; ni < row.length; ni++) {
    var cls = row[ni] === 0 ? 'vec-cell zero' : 'vec-cell hot';
    cells += '<div class="' + cls + '">' + row[ni].toFixed(3) + '</div>';
    var scaled = xsv * row[ni];
    cells2 += '<div class="' + (scaled === 0 ? 'vec-cell zero' : 'vec-cell hot') + '">'
            + scaled.toFixed(3) + '</div>';
  }
  piGet('lab2xr').innerHTML = cells;
  piGet('lab2xrscaled').innerHTML = cells2;
  piGet('lab2z').innerHTML = cells2 + cells;
  piGet('lab2dim').innerHTML = 'C<sub>r</sub> = ' + row.length
                             + ' &nbsp;&middot;&nbsp; dim(Z) = 2 &times; C<sub>r</sub> = '
                             + (2 * row.length);
  piGet('lab2alphao').textContent = a;
  piGet('lab2betao').textContent = b;
}

function makeLab2Change() { return function () { lab2Render(); }; }

/* ============ 初始化 ============ */

function initLabs() {
  var i;
  for (i = 0; i < LAB1_N; i++) {
    piGet('lab1x' + i).addEventListener('input', makeLab1Slide(i));
    piGet('lab1o' + i).textContent = piGet('lab1x' + i).value;
  }
  piGet('lab1go').addEventListener('click', makeLab1Step());
  piGet('lab1reset').addEventListener('click', makeLab1Reset());
  piGet('lab1extra').addEventListener('change', makeLab1Extra());

  var ids = ['lab2x1', 'lab2x2', 'lab2x3', 'lab2alpha', 'lab2beta'];
  for (i = 0; i < ids.length; i++) {
    piGet(ids[i]).addEventListener('input', makeLab2Change());
    piGet(ids[i] + 'o').textContent = piGet(ids[i]).value;
  }
  lab1Render();
  lab2Render();
}
