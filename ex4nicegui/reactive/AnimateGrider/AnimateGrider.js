const ds = Vue.defineComponent
const ps = Vue.computed
const ms = Vue.ref
const gs = Vue.openBlock
const ys = Vue.createElementBlock
const xs = Vue.normalizeStyle
const vs = Vue.unref
const bs = Vue.renderSlot
const ws = Vue.nextTick
function Ft(l) {
  if (l === void 0)
    throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
  return l;
}
function en(l, t) {
  l.prototype = Object.create(t.prototype), l.prototype.constructor = l, l.__proto__ = t;
}
/*!
 * GSAP 3.12.2
 * https://greensock.com
 *
 * @license Copyright 2008-2023, GreenSock. All rights reserved.
 * Subject to the terms at https://greensock.com/standard-license or for
 * Club GreenSock members, the agreement issued with that membership.
 * @author: Jack Doyle, jack@greensock.com
*/
var ht = {
  autoSleep: 120,
  force3D: "auto",
  nullTargetWarn: 1,
  units: {
    lineHeight: ""
  }
}, be = {
  duration: 0.5,
  overwrite: !1,
  delay: 0
}, ir, tt, U, mt = 1e8, L = 1 / mt, Bi = Math.PI * 2, Ts = Bi / 4, Ps = 0, rn = Math.sqrt, ks = Math.cos, Ss = Math.sin, j = function(t) {
  return typeof t == "string";
}, q = function(t) {
  return typeof t == "function";
}, zt = function(t) {
  return typeof t == "number";
}, rr = function(t) {
  return typeof t > "u";
}, Mt = function(t) {
  return typeof t == "object";
}, st = function(t) {
  return t !== !1;
}, nr = function() {
  return typeof window < "u";
}, We = function(t) {
  return q(t) || j(t);
}, nn = typeof ArrayBuffer == "function" && ArrayBuffer.isView || function() {
}, et = Array.isArray, zi = /(?:-?\.?\d|\.)+/gi, sn = /[-+=.]*\d+[.e\-+]*\d*[e\-+]*\d*/g, he = /[-+=.]*\d+[.e-]*\d*[a-z%]*/g, vi = /[-+=.]*\d+\.?\d*(?:e-|e\+)?\d*/gi, an = /[+-]=-?[.\d]+/, on = /[^,'"\[\]\s]+/gi, Cs = /^[+\-=e\s\d]*\d+[.\d]*([a-z]*|%)\s*$/i, V, pt, Vi, sr, ct = {}, ti = {}, un, ln = function(t) {
  return (ti = se(t, ct)) && ut;
}, ar = function(t, e) {
  return console.warn("Invalid property", t, "set to", e, "Missing plugin? gsap.registerPlugin()");
}, ei = function(t, e) {
  return !e && console.warn(t);
}, fn = function(t, e) {
  return t && (ct[t] = e) && ti && (ti[t] = e) || ct;
}, ze = function() {
  return 0;
}, Os = {
  suppressEvents: !0,
  isStart: !0,
  kill: !1
}, je = {
  suppressEvents: !0,
  kill: !1
}, Ms = {
  suppressEvents: !0
}, or = {}, qt = [], Ni = {}, hn, lt = {}, bi = {}, Dr = 30, Ke = [], ur = "", lr = function(t) {
  var e = t[0], i, r;
  if (Mt(e) || q(e) || (t = [t]), !(i = (e._gsap || {}).harness)) {
    for (r = Ke.length; r-- && !Ke[r].targetTest(e); )
      ;
    i = Ke[r];
  }
  for (r = t.length; r--; )
    t[r] && (t[r]._gsap || (t[r]._gsap = new In(t[r], i))) || t.splice(r, 1);
  return t;
}, te = function(t) {
  return t._gsap || lr(gt(t))[0]._gsap;
}, cn = function(t, e, i) {
  return (i = t[e]) && q(i) ? t[e]() : rr(i) && t.getAttribute && t.getAttribute(e) || i;
}, at = function(t, e) {
  return (t = t.split(",")).forEach(e) || t;
}, $ = function(t) {
  return Math.round(t * 1e5) / 1e5 || 0;
}, Q = function(t) {
  return Math.round(t * 1e7) / 1e7 || 0;
}, pe = function(t, e) {
  var i = e.charAt(0), r = parseFloat(e.substr(2));
  return t = parseFloat(t), i === "+" ? t + r : i === "-" ? t - r : i === "*" ? t * r : t / r;
}, Es = function(t, e) {
  for (var i = e.length, r = 0; t.indexOf(e[r]) < 0 && ++r < i; )
    ;
  return r < i;
}, ii = function() {
  var t = qt.length, e = qt.slice(0), i, r;
  for (Ni = {}, qt.length = 0, i = 0; i < t; i++)
    r = e[i], r && r._lazy && (r.render(r._lazy[0], r._lazy[1], !0)._lazy = 0);
}, _n = function(t, e, i, r) {
  qt.length && !tt && ii(), t.render(e, i, r || tt && e < 0 && (t._initted || t._startAt)), qt.length && !tt && ii();
}, dn = function(t) {
  var e = parseFloat(t);
  return (e || e === 0) && (t + "").match(on).length < 2 ? e : j(t) ? t.trim() : t;
}, pn = function(t) {
  return t;
}, vt = function(t, e) {
  for (var i in e)
    i in t || (t[i] = e[i]);
  return t;
}, Ds = function(t) {
  return function(e, i) {
    for (var r in i)
      r in e || r === "duration" && t || r === "ease" || (e[r] = i[r]);
  };
}, se = function(t, e) {
  for (var i in e)
    t[i] = e[i];
  return t;
}, Ar = function l(t, e) {
  for (var i in e)
    i !== "__proto__" && i !== "constructor" && i !== "prototype" && (t[i] = Mt(e[i]) ? l(t[i] || (t[i] = {}), e[i]) : e[i]);
  return t;
}, ri = function(t, e) {
  var i = {}, r;
  for (r in t)
    r in e || (i[r] = t[r]);
  return i;
}, Ae = function(t) {
  var e = t.parent || V, i = t.keyframes ? Ds(et(t.keyframes)) : vt;
  if (st(t.inherit))
    for (; e; )
      i(t, e.vars.defaults), e = e.parent || e._dp;
  return t;
}, As = function(t, e) {
  for (var i = t.length, r = i === e.length; r && i-- && t[i] === e[i]; )
    ;
  return i < 0;
}, mn = function(t, e, i, r, n) {
  i === void 0 && (i = "_first"), r === void 0 && (r = "_last");
  var s = t[r], a;
  if (n)
    for (a = e[n]; s && s[n] > a; )
      s = s._prev;
  return s ? (e._next = s._next, s._next = e) : (e._next = t[i], t[i] = e), e._next ? e._next._prev = e : t[r] = e, e._prev = s, e.parent = e._dp = t, e;
}, hi = function(t, e, i, r) {
  i === void 0 && (i = "_first"), r === void 0 && (r = "_last");
  var n = e._prev, s = e._next;
  n ? n._next = s : t[i] === e && (t[i] = s), s ? s._prev = n : t[r] === e && (t[r] = n), e._next = e._prev = e.parent = null;
}, $t = function(t, e) {
  t.parent && (!e || t.parent.autoRemoveChildren) && t.parent.remove && t.parent.remove(t), t._act = 0;
}, ee = function(t, e) {
  if (t && (!e || e._end > t._dur || e._start < 0))
    for (var i = t; i; )
      i._dirty = 1, i = i.parent;
  return t;
}, Rs = function(t) {
  for (var e = t.parent; e && e.parent; )
    e._dirty = 1, e.totalDuration(), e = e.parent;
  return t;
}, Xi = function(t, e, i, r) {
  return t._startAt && (tt ? t._startAt.revert(je) : t.vars.immediateRender && !t.vars.autoRevert || t._startAt.render(e, !0, r));
}, Fs = function l(t) {
  return !t || t._ts && l(t.parent);
}, Rr = function(t) {
  return t._repeat ? we(t._tTime, t = t.duration() + t._rDelay) * t : 0;
}, we = function(t, e) {
  var i = Math.floor(t /= e);
  return t && i === t ? i - 1 : i;
}, ni = function(t, e) {
  return (t - e._start) * e._ts + (e._ts >= 0 ? 0 : e._dirty ? e.totalDuration() : e._tDur);
}, ci = function(t) {
  return t._end = Q(t._start + (t._tDur / Math.abs(t._ts || t._rts || L) || 0));
}, _i = function(t, e) {
  var i = t._dp;
  return i && i.smoothChildTiming && t._ts && (t._start = Q(i._time - (t._ts > 0 ? e / t._ts : ((t._dirty ? t.totalDuration() : t._tDur) - e) / -t._ts)), ci(t), i._dirty || ee(i, t)), t;
}, gn = function(t, e) {
  var i;
  if ((e._time || !e._dur && e._initted || e._start < t._time && (e._dur || !e.add)) && (i = ni(t.rawTime(), e), (!e._dur || $e(0, e.totalDuration(), i) - e._tTime > L) && e.render(i, !0)), ee(t, e)._dp && t._initted && t._time >= t._dur && t._ts) {
    if (t._dur < t.duration())
      for (i = t; i._dp; )
        i.rawTime() >= 0 && i.totalTime(i._tTime), i = i._dp;
    t._zTime = -L;
  }
}, St = function(t, e, i, r) {
  return e.parent && $t(e), e._start = Q((zt(i) ? i : i || t !== V ? dt(t, i, e) : t._time) + e._delay), e._end = Q(e._start + (e.totalDuration() / Math.abs(e.timeScale()) || 0)), mn(t, e, "_first", "_last", t._sort ? "_start" : 0), Yi(e) || (t._recent = e), r || gn(t, e), t._ts < 0 && _i(t, t._tTime), t;
}, yn = function(t, e) {
  return (ct.ScrollTrigger || ar("scrollTrigger", e)) && ct.ScrollTrigger.create(e, t);
}, xn = function(t, e, i, r, n) {
  if (hr(t, e, n), !t._initted)
    return 1;
  if (!i && t._pt && !tt && (t._dur && t.vars.lazy !== !1 || !t._dur && t.vars.lazy) && hn !== ft.frame)
    return qt.push(t), t._lazy = [n, r], 1;
}, Is = function l(t) {
  var e = t.parent;
  return e && e._ts && e._initted && !e._lock && (e.rawTime() < 0 || l(e));
}, Yi = function(t) {
  var e = t.data;
  return e === "isFromStart" || e === "isStart";
}, Ls = function(t, e, i, r) {
  var n = t.ratio, s = e < 0 || !e && (!t._start && Is(t) && !(!t._initted && Yi(t)) || (t._ts < 0 || t._dp._ts < 0) && !Yi(t)) ? 0 : 1, a = t._rDelay, u = 0, o, f, h;
  if (a && t._repeat && (u = $e(0, t._tDur, e), f = we(u, a), t._yoyo && f & 1 && (s = 1 - s), f !== we(t._tTime, a) && (n = 1 - s, t.vars.repeatRefresh && t._initted && t.invalidate())), s !== n || tt || r || t._zTime === L || !e && t._zTime) {
    if (!t._initted && xn(t, e, r, i, u))
      return;
    for (h = t._zTime, t._zTime = e || (i ? L : 0), i || (i = e && !h), t.ratio = s, t._from && (s = 1 - s), t._time = 0, t._tTime = u, o = t._pt; o; )
      o.r(s, o.d), o = o._next;
    e < 0 && Xi(t, e, i, !0), t._onUpdate && !i && yt(t, "onUpdate"), u && t._repeat && !i && t.parent && yt(t, "onRepeat"), (e >= t._tDur || e < 0) && t.ratio === s && (s && $t(t, 1), !i && !tt && (yt(t, s ? "onComplete" : "onReverseComplete", !0), t._prom && t._prom()));
  } else
    t._zTime || (t._zTime = e);
}, Bs = function(t, e, i) {
  var r;
  if (i > e)
    for (r = t._first; r && r._start <= i; ) {
      if (r.data === "isPause" && r._start > e)
        return r;
      r = r._next;
    }
  else
    for (r = t._last; r && r._start >= i; ) {
      if (r.data === "isPause" && r._start < e)
        return r;
      r = r._prev;
    }
}, Te = function(t, e, i, r) {
  var n = t._repeat, s = Q(e) || 0, a = t._tTime / t._tDur;
  return a && !r && (t._time *= s / t._dur), t._dur = s, t._tDur = n ? n < 0 ? 1e10 : Q(s * (n + 1) + t._rDelay * n) : s, a > 0 && !r && _i(t, t._tTime = t._tDur * a), t.parent && ci(t), i || ee(t.parent, t), t;
}, Fr = function(t) {
  return t instanceof nt ? ee(t) : Te(t, t._dur);
}, zs = {
  _start: 0,
  endTime: ze,
  totalDuration: ze
}, dt = function l(t, e, i) {
  var r = t.labels, n = t._recent || zs, s = t.duration() >= mt ? n.endTime(!1) : t._dur, a, u, o;
  return j(e) && (isNaN(e) || e in r) ? (u = e.charAt(0), o = e.substr(-1) === "%", a = e.indexOf("="), u === "<" || u === ">" ? (a >= 0 && (e = e.replace(/=/, "")), (u === "<" ? n._start : n.endTime(n._repeat >= 0)) + (parseFloat(e.substr(1)) || 0) * (o ? (a < 0 ? n : i).totalDuration() / 100 : 1)) : a < 0 ? (e in r || (r[e] = s), r[e]) : (u = parseFloat(e.charAt(a - 1) + e.substr(a + 1)), o && i && (u = u / 100 * (et(i) ? i[0] : i).totalDuration()), a > 1 ? l(t, e.substr(0, a - 1), i) + u : s + u)) : e == null ? s : +e;
}, Re = function(t, e, i) {
  var r = zt(e[1]), n = (r ? 2 : 1) + (t < 2 ? 0 : 1), s = e[n], a, u;
  if (r && (s.duration = e[1]), s.parent = i, t) {
    for (a = s, u = i; u && !("immediateRender" in a); )
      a = u.vars.defaults || {}, u = st(u.vars.inherit) && u.parent;
    s.immediateRender = st(a.immediateRender), t < 2 ? s.runBackwards = 1 : s.startAt = e[n - 1];
  }
  return new H(e[0], s, e[n + 1]);
}, Ht = function(t, e) {
  return t || t === 0 ? e(t) : e;
}, $e = function(t, e, i) {
  return i < t ? t : i > e ? e : i;
}, J = function(t, e) {
  return !j(t) || !(e = Cs.exec(t)) ? "" : e[1];
}, Vs = function(t, e, i) {
  return Ht(i, function(r) {
    return $e(t, e, r);
  });
}, Ui = [].slice, vn = function(t, e) {
  return t && Mt(t) && "length" in t && (!e && !t.length || t.length - 1 in t && Mt(t[0])) && !t.nodeType && t !== pt;
}, Ns = function(t, e, i) {
  return i === void 0 && (i = []), t.forEach(function(r) {
    var n;
    return j(r) && !e || vn(r, 1) ? (n = i).push.apply(n, gt(r)) : i.push(r);
  }) || i;
}, gt = function(t, e, i) {
  return U && !e && U.selector ? U.selector(t) : j(t) && !i && (Vi || !Pe()) ? Ui.call((e || sr).querySelectorAll(t), 0) : et(t) ? Ns(t, i) : vn(t) ? Ui.call(t, 0) : t ? [t] : [];
}, qi = function(t) {
  return t = gt(t)[0] || ei("Invalid scope") || {}, function(e) {
    var i = t.current || t.nativeElement || t;
    return gt(e, i.querySelectorAll ? i : i === t ? ei("Invalid scope") || sr.createElement("div") : t);
  };
}, bn = function(t) {
  return t.sort(function() {
    return 0.5 - Math.random();
  });
}, wn = function(t) {
  if (q(t))
    return t;
  var e = Mt(t) ? t : {
    each: t
  }, i = ie(e.ease), r = e.from || 0, n = parseFloat(e.base) || 0, s = {}, a = r > 0 && r < 1, u = isNaN(r) || a, o = e.axis, f = r, h = r;
  return j(r) ? f = h = {
    center: 0.5,
    edges: 0.5,
    end: 1
  }[r] || 0 : !a && u && (f = r[0], h = r[1]), function(_, d, p) {
    var c = (p || e).length, m = s[c], g, v, y, b, x, P, k, T, w;
    if (!m) {
      if (w = e.grid === "auto" ? 0 : (e.grid || [1, mt])[1], !w) {
        for (k = -mt; k < (k = p[w++].getBoundingClientRect().left) && w < c; )
          ;
        w--;
      }
      for (m = s[c] = [], g = u ? Math.min(w, c) * f - 0.5 : r % w, v = w === mt ? 0 : u ? c * h / w - 0.5 : r / w | 0, k = 0, T = mt, P = 0; P < c; P++)
        y = P % w - g, b = v - (P / w | 0), m[P] = x = o ? Math.abs(o === "y" ? b : y) : rn(y * y + b * b), x > k && (k = x), x < T && (T = x);
      r === "random" && bn(m), m.max = k - T, m.min = T, m.v = c = (parseFloat(e.amount) || parseFloat(e.each) * (w > c ? c - 1 : o ? o === "y" ? c / w : w : Math.max(w, c / w)) || 0) * (r === "edges" ? -1 : 1), m.b = c < 0 ? n - c : n, m.u = J(e.amount || e.each) || 0, i = i && c < 0 ? An(i) : i;
    }
    return c = (m[_] - m.min) / m.max || 0, Q(m.b + (i ? i(c) : c) * m.v) + m.u;
  };
}, Gi = function(t) {
  var e = Math.pow(10, ((t + "").split(".")[1] || "").length);
  return function(i) {
    var r = Q(Math.round(parseFloat(i) / t) * t * e);
    return (r - r % 1) / e + (zt(i) ? 0 : J(i));
  };
}, Tn = function(t, e) {
  var i = et(t), r, n;
  return !i && Mt(t) && (r = i = t.radius || mt, t.values ? (t = gt(t.values), (n = !zt(t[0])) && (r *= r)) : t = Gi(t.increment)), Ht(e, i ? q(t) ? function(s) {
    return n = t(s), Math.abs(n - s) <= r ? n : s;
  } : function(s) {
    for (var a = parseFloat(n ? s.x : s), u = parseFloat(n ? s.y : 0), o = mt, f = 0, h = t.length, _, d; h--; )
      n ? (_ = t[h].x - a, d = t[h].y - u, _ = _ * _ + d * d) : _ = Math.abs(t[h] - a), _ < o && (o = _, f = h);
    return f = !r || o <= r ? t[f] : s, n || f === s || zt(s) ? f : f + J(s);
  } : Gi(t));
}, Pn = function(t, e, i, r) {
  return Ht(et(t) ? !e : i === !0 ? !!(i = 0) : !r, function() {
    return et(t) ? t[~~(Math.random() * t.length)] : (i = i || 1e-5) && (r = i < 1 ? Math.pow(10, (i + "").length - 2) : 1) && Math.floor(Math.round((t - i / 2 + Math.random() * (e - t + i * 0.99)) / i) * i * r) / r;
  });
}, Xs = function() {
  for (var t = arguments.length, e = new Array(t), i = 0; i < t; i++)
    e[i] = arguments[i];
  return function(r) {
    return e.reduce(function(n, s) {
      return s(n);
    }, r);
  };
}, Ys = function(t, e) {
  return function(i) {
    return t(parseFloat(i)) + (e || J(i));
  };
}, Us = function(t, e, i) {
  return Sn(t, e, 0, 1, i);
}, kn = function(t, e, i) {
  return Ht(i, function(r) {
    return t[~~e(r)];
  });
}, qs = function l(t, e, i) {
  var r = e - t;
  return et(t) ? kn(t, l(0, t.length), e) : Ht(i, function(n) {
    return (r + (n - t) % r) % r + t;
  });
}, Gs = function l(t, e, i) {
  var r = e - t, n = r * 2;
  return et(t) ? kn(t, l(0, t.length - 1), e) : Ht(i, function(s) {
    return s = (n + (s - t) % n) % n || 0, t + (s > r ? n - s : s);
  });
}, Ve = function(t) {
  for (var e = 0, i = "", r, n, s, a; ~(r = t.indexOf("random(", e)); )
    s = t.indexOf(")", r), a = t.charAt(r + 7) === "[", n = t.substr(r + 7, s - r - 7).match(a ? on : zi), i += t.substr(e, r - e) + Pn(a ? n : +n[0], a ? 0 : +n[1], +n[2] || 1e-5), e = s + 1;
  return i + t.substr(e, t.length - e);
}, Sn = function(t, e, i, r, n) {
  var s = e - t, a = r - i;
  return Ht(n, function(u) {
    return i + ((u - t) / s * a || 0);
  });
}, $s = function l(t, e, i, r) {
  var n = isNaN(t + e) ? 0 : function(d) {
    return (1 - d) * t + d * e;
  };
  if (!n) {
    var s = j(t), a = {}, u, o, f, h, _;
    if (i === !0 && (r = 1) && (i = null), s)
      t = {
        p: t
      }, e = {
        p: e
      };
    else if (et(t) && !et(e)) {
      for (f = [], h = t.length, _ = h - 2, o = 1; o < h; o++)
        f.push(l(t[o - 1], t[o]));
      h--, n = function(p) {
        p *= h;
        var c = Math.min(_, ~~p);
        return f[c](p - c);
      }, i = e;
    } else
      r || (t = se(et(t) ? [] : {}, t));
    if (!f) {
      for (u in e)
        fr.call(a, t, u, "get", e[u]);
      n = function(p) {
        return dr(p, a) || (s ? t.p : t);
      };
    }
  }
  return Ht(i, n);
}, Ir = function(t, e, i) {
  var r = t.labels, n = mt, s, a, u;
  for (s in r)
    a = r[s] - e, a < 0 == !!i && a && n > (a = Math.abs(a)) && (u = s, n = a);
  return u;
}, yt = function(t, e, i) {
  var r = t.vars, n = r[e], s = U, a = t._ctx, u, o, f;
  if (n)
    return u = r[e + "Params"], o = r.callbackScope || t, i && qt.length && ii(), a && (U = a), f = u ? n.apply(o, u) : n.call(o), U = s, f;
}, Me = function(t) {
  return $t(t), t.scrollTrigger && t.scrollTrigger.kill(!!tt), t.progress() < 1 && yt(t, "onInterrupt"), t;
}, ce, Cn = [], On = function(t) {
  if (nr() && t) {
    t = !t.name && t.default || t;
    var e = t.name, i = q(t), r = e && !i && t.init ? function() {
      this._props = [];
    } : t, n = {
      init: ze,
      render: dr,
      add: fr,
      kill: ua,
      modifier: oa,
      rawVars: 0
    }, s = {
      targetTest: 0,
      get: 0,
      getSetter: _r,
      aliases: {},
      register: 0
    };
    if (Pe(), t !== r) {
      if (lt[e])
        return;
      vt(r, vt(ri(t, n), s)), se(r.prototype, se(n, ri(t, s))), lt[r.prop = e] = r, t.targetTest && (Ke.push(r), or[e] = 1), e = (e === "css" ? "CSS" : e.charAt(0).toUpperCase() + e.substr(1)) + "Plugin";
    }
    fn(e, r), t.register && t.register(ut, r, ot);
  } else
    t && Cn.push(t);
}, I = 255, Ee = {
  aqua: [0, I, I],
  lime: [0, I, 0],
  silver: [192, 192, 192],
  black: [0, 0, 0],
  maroon: [128, 0, 0],
  teal: [0, 128, 128],
  blue: [0, 0, I],
  navy: [0, 0, 128],
  white: [I, I, I],
  olive: [128, 128, 0],
  yellow: [I, I, 0],
  orange: [I, 165, 0],
  gray: [128, 128, 128],
  purple: [128, 0, 128],
  green: [0, 128, 0],
  red: [I, 0, 0],
  pink: [I, 192, 203],
  cyan: [0, I, I],
  transparent: [I, I, I, 0]
}, wi = function(t, e, i) {
  return t += t < 0 ? 1 : t > 1 ? -1 : 0, (t * 6 < 1 ? e + (i - e) * t * 6 : t < 0.5 ? i : t * 3 < 2 ? e + (i - e) * (2 / 3 - t) * 6 : e) * I + 0.5 | 0;
}, Mn = function(t, e, i) {
  var r = t ? zt(t) ? [t >> 16, t >> 8 & I, t & I] : 0 : Ee.black, n, s, a, u, o, f, h, _, d, p;
  if (!r) {
    if (t.substr(-1) === "," && (t = t.substr(0, t.length - 1)), Ee[t])
      r = Ee[t];
    else if (t.charAt(0) === "#") {
      if (t.length < 6 && (n = t.charAt(1), s = t.charAt(2), a = t.charAt(3), t = "#" + n + n + s + s + a + a + (t.length === 5 ? t.charAt(4) + t.charAt(4) : "")), t.length === 9)
        return r = parseInt(t.substr(1, 6), 16), [r >> 16, r >> 8 & I, r & I, parseInt(t.substr(7), 16) / 255];
      t = parseInt(t.substr(1), 16), r = [t >> 16, t >> 8 & I, t & I];
    } else if (t.substr(0, 3) === "hsl") {
      if (r = p = t.match(zi), !e)
        u = +r[0] % 360 / 360, o = +r[1] / 100, f = +r[2] / 100, s = f <= 0.5 ? f * (o + 1) : f + o - f * o, n = f * 2 - s, r.length > 3 && (r[3] *= 1), r[0] = wi(u + 1 / 3, n, s), r[1] = wi(u, n, s), r[2] = wi(u - 1 / 3, n, s);
      else if (~t.indexOf("="))
        return r = t.match(sn), i && r.length < 4 && (r[3] = 1), r;
    } else
      r = t.match(zi) || Ee.transparent;
    r = r.map(Number);
  }
  return e && !p && (n = r[0] / I, s = r[1] / I, a = r[2] / I, h = Math.max(n, s, a), _ = Math.min(n, s, a), f = (h + _) / 2, h === _ ? u = o = 0 : (d = h - _, o = f > 0.5 ? d / (2 - h - _) : d / (h + _), u = h === n ? (s - a) / d + (s < a ? 6 : 0) : h === s ? (a - n) / d + 2 : (n - s) / d + 4, u *= 60), r[0] = ~~(u + 0.5), r[1] = ~~(o * 100 + 0.5), r[2] = ~~(f * 100 + 0.5)), i && r.length < 4 && (r[3] = 1), r;
}, En = function(t) {
  var e = [], i = [], r = -1;
  return t.split(Gt).forEach(function(n) {
    var s = n.match(he) || [];
    e.push.apply(e, s), i.push(r += s.length + 1);
  }), e.c = i, e;
}, Lr = function(t, e, i) {
  var r = "", n = (t + r).match(Gt), s = e ? "hsla(" : "rgba(", a = 0, u, o, f, h;
  if (!n)
    return t;
  if (n = n.map(function(_) {
    return (_ = Mn(_, e, 1)) && s + (e ? _[0] + "," + _[1] + "%," + _[2] + "%," + _[3] : _.join(",")) + ")";
  }), i && (f = En(t), u = i.c, u.join(r) !== f.c.join(r)))
    for (o = t.replace(Gt, "1").split(he), h = o.length - 1; a < h; a++)
      r += o[a] + (~u.indexOf(a) ? n.shift() || s + "0,0,0,0)" : (f.length ? f : n.length ? n : i).shift());
  if (!o)
    for (o = t.split(Gt), h = o.length - 1; a < h; a++)
      r += o[a] + n[a];
  return r + o[h];
}, Gt = function() {
  var l = "(?:\\b(?:(?:rgb|rgba|hsl|hsla)\\(.+?\\))|\\B#(?:[0-9a-f]{3,4}){1,2}\\b", t;
  for (t in Ee)
    l += "|" + t + "\\b";
  return new RegExp(l + ")", "gi");
}(), Ws = /hsl[a]?\(/, Dn = function(t) {
  var e = t.join(" "), i;
  if (Gt.lastIndex = 0, Gt.test(e))
    return i = Ws.test(e), t[1] = Lr(t[1], i), t[0] = Lr(t[0], i, En(t[1])), !0;
}, Ne, ft = function() {
  var l = Date.now, t = 500, e = 33, i = l(), r = i, n = 1e3 / 240, s = n, a = [], u, o, f, h, _, d, p = function c(m) {
    var g = l() - r, v = m === !0, y, b, x, P;
    if (g > t && (i += g - e), r += g, x = r - i, y = x - s, (y > 0 || v) && (P = ++h.frame, _ = x - h.time * 1e3, h.time = x = x / 1e3, s += y + (y >= n ? 4 : n - y), b = 1), v || (u = o(c)), b)
      for (d = 0; d < a.length; d++)
        a[d](x, _, P, m);
  };
  return h = {
    time: 0,
    frame: 0,
    tick: function() {
      p(!0);
    },
    deltaRatio: function(m) {
      return _ / (1e3 / (m || 60));
    },
    wake: function() {
      un && (!Vi && nr() && (pt = Vi = window, sr = pt.document || {}, ct.gsap = ut, (pt.gsapVersions || (pt.gsapVersions = [])).push(ut.version), ln(ti || pt.GreenSockGlobals || !pt.gsap && pt || {}), f = pt.requestAnimationFrame, Cn.forEach(On)), u && h.sleep(), o = f || function(m) {
        return setTimeout(m, s - h.time * 1e3 + 1 | 0);
      }, Ne = 1, p(2));
    },
    sleep: function() {
      (f ? pt.cancelAnimationFrame : clearTimeout)(u), Ne = 0, o = ze;
    },
    lagSmoothing: function(m, g) {
      t = m || 1 / 0, e = Math.min(g || 33, t);
    },
    fps: function(m) {
      n = 1e3 / (m || 240), s = h.time * 1e3 + n;
    },
    add: function(m, g, v) {
      var y = g ? function(b, x, P, k) {
        m(b, x, P, k), h.remove(y);
      } : m;
      return h.remove(m), a[v ? "unshift" : "push"](y), Pe(), y;
    },
    remove: function(m, g) {
      ~(g = a.indexOf(m)) && a.splice(g, 1) && d >= g && d--;
    },
    _listeners: a
  }, h;
}(), Pe = function() {
  return !Ne && ft.wake();
}, D = {}, Hs = /^[\d.\-M][\d.\-,\s]/, Zs = /["']/g, js = function(t) {
  for (var e = {}, i = t.substr(1, t.length - 3).split(":"), r = i[0], n = 1, s = i.length, a, u, o; n < s; n++)
    u = i[n], a = n !== s - 1 ? u.lastIndexOf(",") : u.length, o = u.substr(0, a), e[r] = isNaN(o) ? o.replace(Zs, "").trim() : +o, r = u.substr(a + 1).trim();
  return e;
}, Ks = function(t) {
  var e = t.indexOf("(") + 1, i = t.indexOf(")"), r = t.indexOf("(", e);
  return t.substring(e, ~r && r < i ? t.indexOf(")", i + 1) : i);
}, Qs = function(t) {
  var e = (t + "").split("("), i = D[e[0]];
  return i && e.length > 1 && i.config ? i.config.apply(null, ~t.indexOf("{") ? [js(e[1])] : Ks(t).split(",").map(dn)) : D._CE && Hs.test(t) ? D._CE("", t) : i;
}, An = function(t) {
  return function(e) {
    return 1 - t(1 - e);
  };
}, Rn = function l(t, e) {
  for (var i = t._first, r; i; )
    i instanceof nt ? l(i, e) : i.vars.yoyoEase && (!i._yoyo || !i._repeat) && i._yoyo !== e && (i.timeline ? l(i.timeline, e) : (r = i._ease, i._ease = i._yEase, i._yEase = r, i._yoyo = e)), i = i._next;
}, ie = function(t, e) {
  return t && (q(t) ? t : D[t] || Qs(t)) || e;
}, ue = function(t, e, i, r) {
  i === void 0 && (i = function(u) {
    return 1 - e(1 - u);
  }), r === void 0 && (r = function(u) {
    return u < 0.5 ? e(u * 2) / 2 : 1 - e((1 - u) * 2) / 2;
  });
  var n = {
    easeIn: e,
    easeOut: i,
    easeInOut: r
  }, s;
  return at(t, function(a) {
    D[a] = ct[a] = n, D[s = a.toLowerCase()] = i;
    for (var u in n)
      D[s + (u === "easeIn" ? ".in" : u === "easeOut" ? ".out" : ".inOut")] = D[a + "." + u] = n[u];
  }), n;
}, Fn = function(t) {
  return function(e) {
    return e < 0.5 ? (1 - t(1 - e * 2)) / 2 : 0.5 + t((e - 0.5) * 2) / 2;
  };
}, Ti = function l(t, e, i) {
  var r = e >= 1 ? e : 1, n = (i || (t ? 0.3 : 0.45)) / (e < 1 ? e : 1), s = n / Bi * (Math.asin(1 / r) || 0), a = function(f) {
    return f === 1 ? 1 : r * Math.pow(2, -10 * f) * Ss((f - s) * n) + 1;
  }, u = t === "out" ? a : t === "in" ? function(o) {
    return 1 - a(1 - o);
  } : Fn(a);
  return n = Bi / n, u.config = function(o, f) {
    return l(t, o, f);
  }, u;
}, Pi = function l(t, e) {
  e === void 0 && (e = 1.70158);
  var i = function(s) {
    return s ? --s * s * ((e + 1) * s + e) + 1 : 0;
  }, r = t === "out" ? i : t === "in" ? function(n) {
    return 1 - i(1 - n);
  } : Fn(i);
  return r.config = function(n) {
    return l(t, n);
  }, r;
};
at("Linear,Quad,Cubic,Quart,Quint,Strong", function(l, t) {
  var e = t < 5 ? t + 1 : t;
  ue(l + ",Power" + (e - 1), t ? function(i) {
    return Math.pow(i, e);
  } : function(i) {
    return i;
  }, function(i) {
    return 1 - Math.pow(1 - i, e);
  }, function(i) {
    return i < 0.5 ? Math.pow(i * 2, e) / 2 : 1 - Math.pow((1 - i) * 2, e) / 2;
  });
});
D.Linear.easeNone = D.none = D.Linear.easeIn;
ue("Elastic", Ti("in"), Ti("out"), Ti());
(function(l, t) {
  var e = 1 / t, i = 2 * e, r = 2.5 * e, n = function(a) {
    return a < e ? l * a * a : a < i ? l * Math.pow(a - 1.5 / t, 2) + 0.75 : a < r ? l * (a -= 2.25 / t) * a + 0.9375 : l * Math.pow(a - 2.625 / t, 2) + 0.984375;
  };
  ue("Bounce", function(s) {
    return 1 - n(1 - s);
  }, n);
})(7.5625, 2.75);
ue("Expo", function(l) {
  return l ? Math.pow(2, 10 * (l - 1)) : 0;
});
ue("Circ", function(l) {
  return -(rn(1 - l * l) - 1);
});
ue("Sine", function(l) {
  return l === 1 ? 1 : -ks(l * Ts) + 1;
});
ue("Back", Pi("in"), Pi("out"), Pi());
D.SteppedEase = D.steps = ct.SteppedEase = {
  config: function(t, e) {
    t === void 0 && (t = 1);
    var i = 1 / t, r = t + (e ? 0 : 1), n = e ? 1 : 0, s = 1 - L;
    return function(a) {
      return ((r * $e(0, s, a) | 0) + n) * i;
    };
  }
};
be.ease = D["quad.out"];
at("onComplete,onUpdate,onStart,onRepeat,onReverseComplete,onInterrupt", function(l) {
  return ur += l + "," + l + "Params,";
});
var In = function(t, e) {
  this.id = Ps++, t._gsap = this, this.target = t, this.harness = e, this.get = e ? e.get : cn, this.set = e ? e.getSetter : _r;
}, Xe = /* @__PURE__ */ function() {
  function l(e) {
    this.vars = e, this._delay = +e.delay || 0, (this._repeat = e.repeat === 1 / 0 ? -2 : e.repeat || 0) && (this._rDelay = e.repeatDelay || 0, this._yoyo = !!e.yoyo || !!e.yoyoEase), this._ts = 1, Te(this, +e.duration, 1, 1), this.data = e.data, U && (this._ctx = U, U.data.push(this)), Ne || ft.wake();
  }
  var t = l.prototype;
  return t.delay = function(i) {
    return i || i === 0 ? (this.parent && this.parent.smoothChildTiming && this.startTime(this._start + i - this._delay), this._delay = i, this) : this._delay;
  }, t.duration = function(i) {
    return arguments.length ? this.totalDuration(this._repeat > 0 ? i + (i + this._rDelay) * this._repeat : i) : this.totalDuration() && this._dur;
  }, t.totalDuration = function(i) {
    return arguments.length ? (this._dirty = 0, Te(this, this._repeat < 0 ? i : (i - this._repeat * this._rDelay) / (this._repeat + 1))) : this._tDur;
  }, t.totalTime = function(i, r) {
    if (Pe(), !arguments.length)
      return this._tTime;
    var n = this._dp;
    if (n && n.smoothChildTiming && this._ts) {
      for (_i(this, i), !n._dp || n.parent || gn(n, this); n && n.parent; )
        n.parent._time !== n._start + (n._ts >= 0 ? n._tTime / n._ts : (n.totalDuration() - n._tTime) / -n._ts) && n.totalTime(n._tTime, !0), n = n.parent;
      !this.parent && this._dp.autoRemoveChildren && (this._ts > 0 && i < this._tDur || this._ts < 0 && i > 0 || !this._tDur && !i) && St(this._dp, this, this._start - this._delay);
    }
    return (this._tTime !== i || !this._dur && !r || this._initted && Math.abs(this._zTime) === L || !i && !this._initted && (this.add || this._ptLookup)) && (this._ts || (this._pTime = i), _n(this, i, r)), this;
  }, t.time = function(i, r) {
    return arguments.length ? this.totalTime(Math.min(this.totalDuration(), i + Rr(this)) % (this._dur + this._rDelay) || (i ? this._dur : 0), r) : this._time;
  }, t.totalProgress = function(i, r) {
    return arguments.length ? this.totalTime(this.totalDuration() * i, r) : this.totalDuration() ? Math.min(1, this._tTime / this._tDur) : this.ratio;
  }, t.progress = function(i, r) {
    return arguments.length ? this.totalTime(this.duration() * (this._yoyo && !(this.iteration() & 1) ? 1 - i : i) + Rr(this), r) : this.duration() ? Math.min(1, this._time / this._dur) : this.ratio;
  }, t.iteration = function(i, r) {
    var n = this.duration() + this._rDelay;
    return arguments.length ? this.totalTime(this._time + (i - 1) * n, r) : this._repeat ? we(this._tTime, n) + 1 : 1;
  }, t.timeScale = function(i) {
    if (!arguments.length)
      return this._rts === -L ? 0 : this._rts;
    if (this._rts === i)
      return this;
    var r = this.parent && this._ts ? ni(this.parent._time, this) : this._tTime;
    return this._rts = +i || 0, this._ts = this._ps || i === -L ? 0 : this._rts, this.totalTime($e(-Math.abs(this._delay), this._tDur, r), !0), ci(this), Rs(this);
  }, t.paused = function(i) {
    return arguments.length ? (this._ps !== i && (this._ps = i, i ? (this._pTime = this._tTime || Math.max(-this._delay, this.rawTime()), this._ts = this._act = 0) : (Pe(), this._ts = this._rts, this.totalTime(this.parent && !this.parent.smoothChildTiming ? this.rawTime() : this._tTime || this._pTime, this.progress() === 1 && Math.abs(this._zTime) !== L && (this._tTime -= L)))), this) : this._ps;
  }, t.startTime = function(i) {
    if (arguments.length) {
      this._start = i;
      var r = this.parent || this._dp;
      return r && (r._sort || !this.parent) && St(r, this, i - this._delay), this;
    }
    return this._start;
  }, t.endTime = function(i) {
    return this._start + (st(i) ? this.totalDuration() : this.duration()) / Math.abs(this._ts || 1);
  }, t.rawTime = function(i) {
    var r = this.parent || this._dp;
    return r ? i && (!this._ts || this._repeat && this._time && this.totalProgress() < 1) ? this._tTime % (this._dur + this._rDelay) : this._ts ? ni(r.rawTime(i), this) : this._tTime : this._tTime;
  }, t.revert = function(i) {
    i === void 0 && (i = Ms);
    var r = tt;
    return tt = i, (this._initted || this._startAt) && (this.timeline && this.timeline.revert(i), this.totalTime(-0.01, i.suppressEvents)), this.data !== "nested" && i.kill !== !1 && this.kill(), tt = r, this;
  }, t.globalTime = function(i) {
    for (var r = this, n = arguments.length ? i : r.rawTime(); r; )
      n = r._start + n / (r._ts || 1), r = r._dp;
    return !this.parent && this._sat ? this._sat.vars.immediateRender ? -1 / 0 : this._sat.globalTime(i) : n;
  }, t.repeat = function(i) {
    return arguments.length ? (this._repeat = i === 1 / 0 ? -2 : i, Fr(this)) : this._repeat === -2 ? 1 / 0 : this._repeat;
  }, t.repeatDelay = function(i) {
    if (arguments.length) {
      var r = this._time;
      return this._rDelay = i, Fr(this), r ? this.time(r) : this;
    }
    return this._rDelay;
  }, t.yoyo = function(i) {
    return arguments.length ? (this._yoyo = i, this) : this._yoyo;
  }, t.seek = function(i, r) {
    return this.totalTime(dt(this, i), st(r));
  }, t.restart = function(i, r) {
    return this.play().totalTime(i ? -this._delay : 0, st(r));
  }, t.play = function(i, r) {
    return i != null && this.seek(i, r), this.reversed(!1).paused(!1);
  }, t.reverse = function(i, r) {
    return i != null && this.seek(i || this.totalDuration(), r), this.reversed(!0).paused(!1);
  }, t.pause = function(i, r) {
    return i != null && this.seek(i, r), this.paused(!0);
  }, t.resume = function() {
    return this.paused(!1);
  }, t.reversed = function(i) {
    return arguments.length ? (!!i !== this.reversed() && this.timeScale(-this._rts || (i ? -L : 0)), this) : this._rts < 0;
  }, t.invalidate = function() {
    return this._initted = this._act = 0, this._zTime = -L, this;
  }, t.isActive = function() {
    var i = this.parent || this._dp, r = this._start, n;
    return !!(!i || this._ts && this._initted && i.isActive() && (n = i.rawTime(!0)) >= r && n < this.endTime(!0) - L);
  }, t.eventCallback = function(i, r, n) {
    var s = this.vars;
    return arguments.length > 1 ? (r ? (s[i] = r, n && (s[i + "Params"] = n), i === "onUpdate" && (this._onUpdate = r)) : delete s[i], this) : s[i];
  }, t.then = function(i) {
    var r = this;
    return new Promise(function(n) {
      var s = q(i) ? i : pn, a = function() {
        var o = r.then;
        r.then = null, q(s) && (s = s(r)) && (s.then || s === r) && (r.then = o), n(s), r.then = o;
      };
      r._initted && r.totalProgress() === 1 && r._ts >= 0 || !r._tTime && r._ts < 0 ? a() : r._prom = a;
    });
  }, t.kill = function() {
    Me(this);
  }, l;
}();
vt(Xe.prototype, {
  _time: 0,
  _start: 0,
  _end: 0,
  _tTime: 0,
  _tDur: 0,
  _dirty: 0,
  _repeat: 0,
  _yoyo: !1,
  parent: null,
  _initted: !1,
  _rDelay: 0,
  _ts: 1,
  _dp: 0,
  ratio: 0,
  _zTime: -L,
  _prom: 0,
  _ps: !1,
  _rts: 1
});
var nt = /* @__PURE__ */ function(l) {
  en(t, l);
  function t(i, r) {
    var n;
    return i === void 0 && (i = {}), n = l.call(this, i) || this, n.labels = {}, n.smoothChildTiming = !!i.smoothChildTiming, n.autoRemoveChildren = !!i.autoRemoveChildren, n._sort = st(i.sortChildren), V && St(i.parent || V, Ft(n), r), i.reversed && n.reverse(), i.paused && n.paused(!0), i.scrollTrigger && yn(Ft(n), i.scrollTrigger), n;
  }
  var e = t.prototype;
  return e.to = function(r, n, s) {
    return Re(0, arguments, this), this;
  }, e.from = function(r, n, s) {
    return Re(1, arguments, this), this;
  }, e.fromTo = function(r, n, s, a) {
    return Re(2, arguments, this), this;
  }, e.set = function(r, n, s) {
    return n.duration = 0, n.parent = this, Ae(n).repeatDelay || (n.repeat = 0), n.immediateRender = !!n.immediateRender, new H(r, n, dt(this, s), 1), this;
  }, e.call = function(r, n, s) {
    return St(this, H.delayedCall(0, r, n), s);
  }, e.staggerTo = function(r, n, s, a, u, o, f) {
    return s.duration = n, s.stagger = s.stagger || a, s.onComplete = o, s.onCompleteParams = f, s.parent = this, new H(r, s, dt(this, u)), this;
  }, e.staggerFrom = function(r, n, s, a, u, o, f) {
    return s.runBackwards = 1, Ae(s).immediateRender = st(s.immediateRender), this.staggerTo(r, n, s, a, u, o, f);
  }, e.staggerFromTo = function(r, n, s, a, u, o, f, h) {
    return a.startAt = s, Ae(a).immediateRender = st(a.immediateRender), this.staggerTo(r, n, a, u, o, f, h);
  }, e.render = function(r, n, s) {
    var a = this._time, u = this._dirty ? this.totalDuration() : this._tDur, o = this._dur, f = r <= 0 ? 0 : Q(r), h = this._zTime < 0 != r < 0 && (this._initted || !o), _, d, p, c, m, g, v, y, b, x, P, k;
    if (this !== V && f > u && r >= 0 && (f = u), f !== this._tTime || s || h) {
      if (a !== this._time && o && (f += this._time - a, r += this._time - a), _ = f, b = this._start, y = this._ts, g = !y, h && (o || (a = this._zTime), (r || !n) && (this._zTime = r)), this._repeat) {
        if (P = this._yoyo, m = o + this._rDelay, this._repeat < -1 && r < 0)
          return this.totalTime(m * 100 + r, n, s);
        if (_ = Q(f % m), f === u ? (c = this._repeat, _ = o) : (c = ~~(f / m), c && c === f / m && (_ = o, c--), _ > o && (_ = o)), x = we(this._tTime, m), !a && this._tTime && x !== c && this._tTime - x * m - this._dur <= 0 && (x = c), P && c & 1 && (_ = o - _, k = 1), c !== x && !this._lock) {
          var T = P && x & 1, w = T === (P && c & 1);
          if (c < x && (T = !T), a = T ? 0 : f % o ? o : f, this._lock = 1, this.render(a || (k ? 0 : Q(c * m)), n, !o)._lock = 0, this._tTime = f, !n && this.parent && yt(this, "onRepeat"), this.vars.repeatRefresh && !k && (this.invalidate()._lock = 1), a && a !== this._time || g !== !this._ts || this.vars.onRepeat && !this.parent && !this._act)
            return this;
          if (o = this._dur, u = this._tDur, w && (this._lock = 2, a = T ? o : -1e-4, this.render(a, !0), this.vars.repeatRefresh && !k && this.invalidate()), this._lock = 0, !this._ts && !g)
            return this;
          Rn(this, k);
        }
      }
      if (this._hasPause && !this._forcing && this._lock < 2 && (v = Bs(this, Q(a), Q(_)), v && (f -= _ - (_ = v._start))), this._tTime = f, this._time = _, this._act = !y, this._initted || (this._onUpdate = this.vars.onUpdate, this._initted = 1, this._zTime = r, a = 0), !a && _ && !n && !c && (yt(this, "onStart"), this._tTime !== f))
        return this;
      if (_ >= a && r >= 0)
        for (d = this._first; d; ) {
          if (p = d._next, (d._act || _ >= d._start) && d._ts && v !== d) {
            if (d.parent !== this)
              return this.render(r, n, s);
            if (d.render(d._ts > 0 ? (_ - d._start) * d._ts : (d._dirty ? d.totalDuration() : d._tDur) + (_ - d._start) * d._ts, n, s), _ !== this._time || !this._ts && !g) {
              v = 0, p && (f += this._zTime = -L);
              break;
            }
          }
          d = p;
        }
      else {
        d = this._last;
        for (var S = r < 0 ? r : _; d; ) {
          if (p = d._prev, (d._act || S <= d._end) && d._ts && v !== d) {
            if (d.parent !== this)
              return this.render(r, n, s);
            if (d.render(d._ts > 0 ? (S - d._start) * d._ts : (d._dirty ? d.totalDuration() : d._tDur) + (S - d._start) * d._ts, n, s || tt && (d._initted || d._startAt)), _ !== this._time || !this._ts && !g) {
              v = 0, p && (f += this._zTime = S ? -L : L);
              break;
            }
          }
          d = p;
        }
      }
      if (v && !n && (this.pause(), v.render(_ >= a ? 0 : -L)._zTime = _ >= a ? 1 : -1, this._ts))
        return this._start = b, ci(this), this.render(r, n, s);
      this._onUpdate && !n && yt(this, "onUpdate", !0), (f === u && this._tTime >= this.totalDuration() || !f && a) && (b === this._start || Math.abs(y) !== Math.abs(this._ts)) && (this._lock || ((r || !o) && (f === u && this._ts > 0 || !f && this._ts < 0) && $t(this, 1), !n && !(r < 0 && !a) && (f || a || !u) && (yt(this, f === u && r >= 0 ? "onComplete" : "onReverseComplete", !0), this._prom && !(f < u && this.timeScale() > 0) && this._prom())));
    }
    return this;
  }, e.add = function(r, n) {
    var s = this;
    if (zt(n) || (n = dt(this, n, r)), !(r instanceof Xe)) {
      if (et(r))
        return r.forEach(function(a) {
          return s.add(a, n);
        }), this;
      if (j(r))
        return this.addLabel(r, n);
      if (q(r))
        r = H.delayedCall(0, r);
      else
        return this;
    }
    return this !== r ? St(this, r, n) : this;
  }, e.getChildren = function(r, n, s, a) {
    r === void 0 && (r = !0), n === void 0 && (n = !0), s === void 0 && (s = !0), a === void 0 && (a = -mt);
    for (var u = [], o = this._first; o; )
      o._start >= a && (o instanceof H ? n && u.push(o) : (s && u.push(o), r && u.push.apply(u, o.getChildren(!0, n, s)))), o = o._next;
    return u;
  }, e.getById = function(r) {
    for (var n = this.getChildren(1, 1, 1), s = n.length; s--; )
      if (n[s].vars.id === r)
        return n[s];
  }, e.remove = function(r) {
    return j(r) ? this.removeLabel(r) : q(r) ? this.killTweensOf(r) : (hi(this, r), r === this._recent && (this._recent = this._last), ee(this));
  }, e.totalTime = function(r, n) {
    return arguments.length ? (this._forcing = 1, !this._dp && this._ts && (this._start = Q(ft.time - (this._ts > 0 ? r / this._ts : (this.totalDuration() - r) / -this._ts))), l.prototype.totalTime.call(this, r, n), this._forcing = 0, this) : this._tTime;
  }, e.addLabel = function(r, n) {
    return this.labels[r] = dt(this, n), this;
  }, e.removeLabel = function(r) {
    return delete this.labels[r], this;
  }, e.addPause = function(r, n, s) {
    var a = H.delayedCall(0, n || ze, s);
    return a.data = "isPause", this._hasPause = 1, St(this, a, dt(this, r));
  }, e.removePause = function(r) {
    var n = this._first;
    for (r = dt(this, r); n; )
      n._start === r && n.data === "isPause" && $t(n), n = n._next;
  }, e.killTweensOf = function(r, n, s) {
    for (var a = this.getTweensOf(r, s), u = a.length; u--; )
      Xt !== a[u] && a[u].kill(r, n);
    return this;
  }, e.getTweensOf = function(r, n) {
    for (var s = [], a = gt(r), u = this._first, o = zt(n), f; u; )
      u instanceof H ? Es(u._targets, a) && (o ? (!Xt || u._initted && u._ts) && u.globalTime(0) <= n && u.globalTime(u.totalDuration()) > n : !n || u.isActive()) && s.push(u) : (f = u.getTweensOf(a, n)).length && s.push.apply(s, f), u = u._next;
    return s;
  }, e.tweenTo = function(r, n) {
    n = n || {};
    var s = this, a = dt(s, r), u = n, o = u.startAt, f = u.onStart, h = u.onStartParams, _ = u.immediateRender, d, p = H.to(s, vt({
      ease: n.ease || "none",
      lazy: !1,
      immediateRender: !1,
      time: a,
      overwrite: "auto",
      duration: n.duration || Math.abs((a - (o && "time" in o ? o.time : s._time)) / s.timeScale()) || L,
      onStart: function() {
        if (s.pause(), !d) {
          var m = n.duration || Math.abs((a - (o && "time" in o ? o.time : s._time)) / s.timeScale());
          p._dur !== m && Te(p, m, 0, 1).render(p._time, !0, !0), d = 1;
        }
        f && f.apply(p, h || []);
      }
    }, n));
    return _ ? p.render(0) : p;
  }, e.tweenFromTo = function(r, n, s) {
    return this.tweenTo(n, vt({
      startAt: {
        time: dt(this, r)
      }
    }, s));
  }, e.recent = function() {
    return this._recent;
  }, e.nextLabel = function(r) {
    return r === void 0 && (r = this._time), Ir(this, dt(this, r));
  }, e.previousLabel = function(r) {
    return r === void 0 && (r = this._time), Ir(this, dt(this, r), 1);
  }, e.currentLabel = function(r) {
    return arguments.length ? this.seek(r, !0) : this.previousLabel(this._time + L);
  }, e.shiftChildren = function(r, n, s) {
    s === void 0 && (s = 0);
    for (var a = this._first, u = this.labels, o; a; )
      a._start >= s && (a._start += r, a._end += r), a = a._next;
    if (n)
      for (o in u)
        u[o] >= s && (u[o] += r);
    return ee(this);
  }, e.invalidate = function(r) {
    var n = this._first;
    for (this._lock = 0; n; )
      n.invalidate(r), n = n._next;
    return l.prototype.invalidate.call(this, r);
  }, e.clear = function(r) {
    r === void 0 && (r = !0);
    for (var n = this._first, s; n; )
      s = n._next, this.remove(n), n = s;
    return this._dp && (this._time = this._tTime = this._pTime = 0), r && (this.labels = {}), ee(this);
  }, e.totalDuration = function(r) {
    var n = 0, s = this, a = s._last, u = mt, o, f, h;
    if (arguments.length)
      return s.timeScale((s._repeat < 0 ? s.duration() : s.totalDuration()) / (s.reversed() ? -r : r));
    if (s._dirty) {
      for (h = s.parent; a; )
        o = a._prev, a._dirty && a.totalDuration(), f = a._start, f > u && s._sort && a._ts && !s._lock ? (s._lock = 1, St(s, a, f - a._delay, 1)._lock = 0) : u = f, f < 0 && a._ts && (n -= f, (!h && !s._dp || h && h.smoothChildTiming) && (s._start += f / s._ts, s._time -= f, s._tTime -= f), s.shiftChildren(-f, !1, -1 / 0), u = 0), a._end > n && a._ts && (n = a._end), a = o;
      Te(s, s === V && s._time > n ? s._time : n, 1, 1), s._dirty = 0;
    }
    return s._tDur;
  }, t.updateRoot = function(r) {
    if (V._ts && (_n(V, ni(r, V)), hn = ft.frame), ft.frame >= Dr) {
      Dr += ht.autoSleep || 120;
      var n = V._first;
      if ((!n || !n._ts) && ht.autoSleep && ft._listeners.length < 2) {
        for (; n && !n._ts; )
          n = n._next;
        n || ft.sleep();
      }
    }
  }, t;
}(Xe);
vt(nt.prototype, {
  _lock: 0,
  _hasPause: 0,
  _forcing: 0
});
var Js = function(t, e, i, r, n, s, a) {
  var u = new ot(this._pt, t, e, 0, 1, Xn, null, n), o = 0, f = 0, h, _, d, p, c, m, g, v;
  for (u.b = i, u.e = r, i += "", r += "", (g = ~r.indexOf("random(")) && (r = Ve(r)), s && (v = [i, r], s(v, t, e), i = v[0], r = v[1]), _ = i.match(vi) || []; h = vi.exec(r); )
    p = h[0], c = r.substring(o, h.index), d ? d = (d + 1) % 5 : c.substr(-5) === "rgba(" && (d = 1), p !== _[f++] && (m = parseFloat(_[f - 1]) || 0, u._pt = {
      _next: u._pt,
      p: c || f === 1 ? c : ",",
      //note: SVG spec allows omission of comma/space when a negative sign is wedged between two numbers, like 2.5-5.3 instead of 2.5,-5.3 but when tweening, the negative value may switch to positive, so we insert the comma just in case.
      s: m,
      c: p.charAt(1) === "=" ? pe(m, p) - m : parseFloat(p) - m,
      m: d && d < 4 ? Math.round : 0
    }, o = vi.lastIndex);
  return u.c = o < r.length ? r.substring(o, r.length) : "", u.fp = a, (an.test(r) || g) && (u.e = 0), this._pt = u, u;
}, fr = function(t, e, i, r, n, s, a, u, o, f) {
  q(r) && (r = r(n || 0, t, s));
  var h = t[e], _ = i !== "get" ? i : q(h) ? o ? t[e.indexOf("set") || !q(t["get" + e.substr(3)]) ? e : "get" + e.substr(3)](o) : t[e]() : h, d = q(h) ? o ? na : Vn : cr, p;
  if (j(r) && (~r.indexOf("random(") && (r = Ve(r)), r.charAt(1) === "=" && (p = pe(_, r) + (J(_) || 0), (p || p === 0) && (r = p))), !f || _ !== r || $i)
    return !isNaN(_ * r) && r !== "" ? (p = new ot(this._pt, t, e, +_ || 0, r - (_ || 0), typeof h == "boolean" ? aa : Nn, 0, d), o && (p.fp = o), a && p.modifier(a, this, t), this._pt = p) : (!h && !(e in t) && ar(e, r), Js.call(this, t, e, _, r, d, u || ht.stringFilter, o));
}, ta = function(t, e, i, r, n) {
  if (q(t) && (t = Fe(t, n, e, i, r)), !Mt(t) || t.style && t.nodeType || et(t) || nn(t))
    return j(t) ? Fe(t, n, e, i, r) : t;
  var s = {}, a;
  for (a in t)
    s[a] = Fe(t[a], n, e, i, r);
  return s;
}, Ln = function(t, e, i, r, n, s) {
  var a, u, o, f;
  if (lt[t] && (a = new lt[t]()).init(n, a.rawVars ? e[t] : ta(e[t], r, n, s, i), i, r, s) !== !1 && (i._pt = u = new ot(i._pt, n, t, 0, 1, a.render, a, 0, a.priority), i !== ce))
    for (o = i._ptLookup[i._targets.indexOf(n)], f = a._props.length; f--; )
      o[a._props[f]] = u;
  return a;
}, Xt, $i, hr = function l(t, e, i) {
  var r = t.vars, n = r.ease, s = r.startAt, a = r.immediateRender, u = r.lazy, o = r.onUpdate, f = r.onUpdateParams, h = r.callbackScope, _ = r.runBackwards, d = r.yoyoEase, p = r.keyframes, c = r.autoRevert, m = t._dur, g = t._startAt, v = t._targets, y = t.parent, b = y && y.data === "nested" ? y.vars.targets : v, x = t._overwrite === "auto" && !ir, P = t.timeline, k, T, w, S, O, A, R, E, C, z, X, K, bt;
  if (P && (!p || !n) && (n = "none"), t._ease = ie(n, be.ease), t._yEase = d ? An(ie(d === !0 ? n : d, be.ease)) : 0, d && t._yoyo && !t._repeat && (d = t._yEase, t._yEase = t._ease, t._ease = d), t._from = !P && !!r.runBackwards, !P || p && !r.stagger) {
    if (E = v[0] ? te(v[0]).harness : 0, K = E && r[E.prop], k = ri(r, or), g && (g._zTime < 0 && g.progress(1), e < 0 && _ && a && !c ? g.render(-1, !0) : g.revert(_ && m ? je : Os), g._lazy = 0), s) {
      if ($t(t._startAt = H.set(v, vt({
        data: "isStart",
        overwrite: !1,
        parent: y,
        immediateRender: !0,
        lazy: !g && st(u),
        startAt: null,
        delay: 0,
        onUpdate: o,
        onUpdateParams: f,
        callbackScope: h,
        stagger: 0
      }, s))), t._startAt._dp = 0, t._startAt._sat = t, e < 0 && (tt || !a && !c) && t._startAt.revert(je), a && m && e <= 0 && i <= 0) {
        e && (t._zTime = e);
        return;
      }
    } else if (_ && m && !g) {
      if (e && (a = !1), w = vt({
        overwrite: !1,
        data: "isFromStart",
        //we tag the tween with as "isFromStart" so that if [inside a plugin] we need to only do something at the very END of a tween, we have a way of identifying this tween as merely the one that's setting the beginning values for a "from()" tween. For example, clearProps in CSSPlugin should only get applied at the very END of a tween and without this tag, from(...{height:100, clearProps:"height", delay:1}) would wipe the height at the beginning of the tween and after 1 second, it'd kick back in.
        lazy: a && !g && st(u),
        immediateRender: a,
        //zero-duration tweens render immediately by default, but if we're not specifically instructed to render this tween immediately, we should skip this and merely _init() to record the starting values (rendering them immediately would push them to completion which is wasteful in that case - we'd have to render(-1) immediately after)
        stagger: 0,
        parent: y
        //ensures that nested tweens that had a stagger are handled properly, like gsap.from(".class", {y: gsap.utils.wrap([-100,100]), stagger: 0.5})
      }, k), K && (w[E.prop] = K), $t(t._startAt = H.set(v, w)), t._startAt._dp = 0, t._startAt._sat = t, e < 0 && (tt ? t._startAt.revert(je) : t._startAt.render(-1, !0)), t._zTime = e, !a)
        l(t._startAt, L, L);
      else if (!e)
        return;
    }
    for (t._pt = t._ptCache = 0, u = m && st(u) || u && !m, T = 0; T < v.length; T++) {
      if (O = v[T], R = O._gsap || lr(v)[T]._gsap, t._ptLookup[T] = z = {}, Ni[R.id] && qt.length && ii(), X = b === v ? T : b.indexOf(O), E && (C = new E()).init(O, K || k, t, X, b) !== !1 && (t._pt = S = new ot(t._pt, O, C.name, 0, 1, C.render, C, 0, C.priority), C._props.forEach(function(Pt) {
        z[Pt] = S;
      }), C.priority && (A = 1)), !E || K)
        for (w in k)
          lt[w] && (C = Ln(w, k, t, X, O, b)) ? C.priority && (A = 1) : z[w] = S = fr.call(t, O, w, "get", k[w], X, b, 0, r.stringFilter);
      t._op && t._op[T] && t.kill(O, t._op[T]), x && t._pt && (Xt = t, V.killTweensOf(O, z, t.globalTime(e)), bt = !t.parent, Xt = 0), t._pt && u && (Ni[R.id] = 1);
    }
    A && Yn(t), t._onInit && t._onInit(t);
  }
  t._onUpdate = o, t._initted = (!t._op || t._pt) && !bt, p && e <= 0 && P.render(mt, !0, !0);
}, ea = function(t, e, i, r, n, s, a) {
  var u = (t._pt && t._ptCache || (t._ptCache = {}))[e], o, f, h, _;
  if (!u)
    for (u = t._ptCache[e] = [], h = t._ptLookup, _ = t._targets.length; _--; ) {
      if (o = h[_][e], o && o.d && o.d._pt)
        for (o = o.d._pt; o && o.p !== e && o.fp !== e; )
          o = o._next;
      if (!o)
        return $i = 1, t.vars[e] = "+=0", hr(t, a), $i = 0, 1;
      u.push(o);
    }
  for (_ = u.length; _--; )
    f = u[_], o = f._pt || f, o.s = (r || r === 0) && !n ? r : o.s + (r || 0) + s * o.c, o.c = i - o.s, f.e && (f.e = $(i) + J(f.e)), f.b && (f.b = o.s + J(f.b));
}, ia = function(t, e) {
  var i = t[0] ? te(t[0]).harness : 0, r = i && i.aliases, n, s, a, u;
  if (!r)
    return e;
  n = se({}, e);
  for (s in r)
    if (s in n)
      for (u = r[s].split(","), a = u.length; a--; )
        n[u[a]] = n[s];
  return n;
}, ra = function(t, e, i, r) {
  var n = e.ease || r || "power1.inOut", s, a;
  if (et(e))
    a = i[t] || (i[t] = []), e.forEach(function(u, o) {
      return a.push({
        t: o / (e.length - 1) * 100,
        v: u,
        e: n
      });
    });
  else
    for (s in e)
      a = i[s] || (i[s] = []), s === "ease" || a.push({
        t: parseFloat(t),
        v: e[s],
        e: n
      });
}, Fe = function(t, e, i, r, n) {
  return q(t) ? t.call(e, i, r, n) : j(t) && ~t.indexOf("random(") ? Ve(t) : t;
}, Bn = ur + "repeat,repeatDelay,yoyo,repeatRefresh,yoyoEase,autoRevert", zn = {};
at(Bn + ",id,stagger,delay,duration,paused,scrollTrigger", function(l) {
  return zn[l] = 1;
});
var H = /* @__PURE__ */ function(l) {
  en(t, l);
  function t(i, r, n, s) {
    var a;
    typeof r == "number" && (n.duration = r, r = n, n = null), a = l.call(this, s ? r : Ae(r)) || this;
    var u = a.vars, o = u.duration, f = u.delay, h = u.immediateRender, _ = u.stagger, d = u.overwrite, p = u.keyframes, c = u.defaults, m = u.scrollTrigger, g = u.yoyoEase, v = r.parent || V, y = (et(i) || nn(i) ? zt(i[0]) : "length" in r) ? [i] : gt(i), b, x, P, k, T, w, S, O;
    if (a._targets = y.length ? lr(y) : ei("GSAP target " + i + " not found. https://greensock.com", !ht.nullTargetWarn) || [], a._ptLookup = [], a._overwrite = d, p || _ || We(o) || We(f)) {
      if (r = a.vars, b = a.timeline = new nt({
        data: "nested",
        defaults: c || {},
        targets: v && v.data === "nested" ? v.vars.targets : y
      }), b.kill(), b.parent = b._dp = Ft(a), b._start = 0, _ || We(o) || We(f)) {
        if (k = y.length, S = _ && wn(_), Mt(_))
          for (T in _)
            ~Bn.indexOf(T) && (O || (O = {}), O[T] = _[T]);
        for (x = 0; x < k; x++)
          P = ri(r, zn), P.stagger = 0, g && (P.yoyoEase = g), O && se(P, O), w = y[x], P.duration = +Fe(o, Ft(a), x, w, y), P.delay = (+Fe(f, Ft(a), x, w, y) || 0) - a._delay, !_ && k === 1 && P.delay && (a._delay = f = P.delay, a._start += f, P.delay = 0), b.to(w, P, S ? S(x, w, y) : 0), b._ease = D.none;
        b.duration() ? o = f = 0 : a.timeline = 0;
      } else if (p) {
        Ae(vt(b.vars.defaults, {
          ease: "none"
        })), b._ease = ie(p.ease || r.ease || "none");
        var A = 0, R, E, C;
        if (et(p))
          p.forEach(function(z) {
            return b.to(y, z, ">");
          }), b.duration();
        else {
          P = {};
          for (T in p)
            T === "ease" || T === "easeEach" || ra(T, p[T], P, p.easeEach);
          for (T in P)
            for (R = P[T].sort(function(z, X) {
              return z.t - X.t;
            }), A = 0, x = 0; x < R.length; x++)
              E = R[x], C = {
                ease: E.e,
                duration: (E.t - (x ? R[x - 1].t : 0)) / 100 * o
              }, C[T] = E.v, b.to(y, C, A), A += C.duration;
          b.duration() < o && b.to({}, {
            duration: o - b.duration()
          });
        }
      }
      o || a.duration(o = b.duration());
    } else
      a.timeline = 0;
    return d === !0 && !ir && (Xt = Ft(a), V.killTweensOf(y), Xt = 0), St(v, Ft(a), n), r.reversed && a.reverse(), r.paused && a.paused(!0), (h || !o && !p && a._start === Q(v._time) && st(h) && Fs(Ft(a)) && v.data !== "nested") && (a._tTime = -L, a.render(Math.max(0, -f) || 0)), m && yn(Ft(a), m), a;
  }
  var e = t.prototype;
  return e.render = function(r, n, s) {
    var a = this._time, u = this._tDur, o = this._dur, f = r < 0, h = r > u - L && !f ? u : r < L ? 0 : r, _, d, p, c, m, g, v, y, b;
    if (!o)
      Ls(this, r, n, s);
    else if (h !== this._tTime || !r || s || !this._initted && this._tTime || this._startAt && this._zTime < 0 !== f) {
      if (_ = h, y = this.timeline, this._repeat) {
        if (c = o + this._rDelay, this._repeat < -1 && f)
          return this.totalTime(c * 100 + r, n, s);
        if (_ = Q(h % c), h === u ? (p = this._repeat, _ = o) : (p = ~~(h / c), p && p === h / c && (_ = o, p--), _ > o && (_ = o)), g = this._yoyo && p & 1, g && (b = this._yEase, _ = o - _), m = we(this._tTime, c), _ === a && !s && this._initted)
          return this._tTime = h, this;
        p !== m && (y && this._yEase && Rn(y, g), this.vars.repeatRefresh && !g && !this._lock && (this._lock = s = 1, this.render(Q(c * p), !0).invalidate()._lock = 0));
      }
      if (!this._initted) {
        if (xn(this, f ? r : _, s, n, h))
          return this._tTime = 0, this;
        if (a !== this._time)
          return this;
        if (o !== this._dur)
          return this.render(r, n, s);
      }
      if (this._tTime = h, this._time = _, !this._act && this._ts && (this._act = 1, this._lazy = 0), this.ratio = v = (b || this._ease)(_ / o), this._from && (this.ratio = v = 1 - v), _ && !a && !n && !p && (yt(this, "onStart"), this._tTime !== h))
        return this;
      for (d = this._pt; d; )
        d.r(v, d.d), d = d._next;
      y && y.render(r < 0 ? r : !_ && g ? -L : y._dur * y._ease(_ / this._dur), n, s) || this._startAt && (this._zTime = r), this._onUpdate && !n && (f && Xi(this, r, n, s), yt(this, "onUpdate")), this._repeat && p !== m && this.vars.onRepeat && !n && this.parent && yt(this, "onRepeat"), (h === this._tDur || !h) && this._tTime === h && (f && !this._onUpdate && Xi(this, r, !0, !0), (r || !o) && (h === this._tDur && this._ts > 0 || !h && this._ts < 0) && $t(this, 1), !n && !(f && !a) && (h || a || g) && (yt(this, h === u ? "onComplete" : "onReverseComplete", !0), this._prom && !(h < u && this.timeScale() > 0) && this._prom()));
    }
    return this;
  }, e.targets = function() {
    return this._targets;
  }, e.invalidate = function(r) {
    return (!r || !this.vars.runBackwards) && (this._startAt = 0), this._pt = this._op = this._onUpdate = this._lazy = this.ratio = 0, this._ptLookup = [], this.timeline && this.timeline.invalidate(r), l.prototype.invalidate.call(this, r);
  }, e.resetTo = function(r, n, s, a) {
    Ne || ft.wake(), this._ts || this.play();
    var u = Math.min(this._dur, (this._dp._time - this._start) * this._ts), o;
    return this._initted || hr(this, u), o = this._ease(u / this._dur), ea(this, r, n, s, a, o, u) ? this.resetTo(r, n, s, a) : (_i(this, 0), this.parent || mn(this._dp, this, "_first", "_last", this._dp._sort ? "_start" : 0), this.render(0));
  }, e.kill = function(r, n) {
    if (n === void 0 && (n = "all"), !r && (!n || n === "all"))
      return this._lazy = this._pt = 0, this.parent ? Me(this) : this;
    if (this.timeline) {
      var s = this.timeline.totalDuration();
      return this.timeline.killTweensOf(r, n, Xt && Xt.vars.overwrite !== !0)._first || Me(this), this.parent && s !== this.timeline.totalDuration() && Te(this, this._dur * this.timeline._tDur / s, 0, 1), this;
    }
    var a = this._targets, u = r ? gt(r) : a, o = this._ptLookup, f = this._pt, h, _, d, p, c, m, g;
    if ((!n || n === "all") && As(a, u))
      return n === "all" && (this._pt = 0), Me(this);
    for (h = this._op = this._op || [], n !== "all" && (j(n) && (c = {}, at(n, function(v) {
      return c[v] = 1;
    }), n = c), n = ia(a, n)), g = a.length; g--; )
      if (~u.indexOf(a[g])) {
        _ = o[g], n === "all" ? (h[g] = n, p = _, d = {}) : (d = h[g] = h[g] || {}, p = n);
        for (c in p)
          m = _ && _[c], m && ((!("kill" in m.d) || m.d.kill(c) === !0) && hi(this, m, "_pt"), delete _[c]), d !== "all" && (d[c] = 1);
      }
    return this._initted && !this._pt && f && Me(this), this;
  }, t.to = function(r, n) {
    return new t(r, n, arguments[2]);
  }, t.from = function(r, n) {
    return Re(1, arguments);
  }, t.delayedCall = function(r, n, s, a) {
    return new t(n, 0, {
      immediateRender: !1,
      lazy: !1,
      overwrite: !1,
      delay: r,
      onComplete: n,
      onReverseComplete: n,
      onCompleteParams: s,
      onReverseCompleteParams: s,
      callbackScope: a
    });
  }, t.fromTo = function(r, n, s) {
    return Re(2, arguments);
  }, t.set = function(r, n) {
    return n.duration = 0, n.repeatDelay || (n.repeat = 0), new t(r, n);
  }, t.killTweensOf = function(r, n, s) {
    return V.killTweensOf(r, n, s);
  }, t;
}(Xe);
vt(H.prototype, {
  _targets: [],
  _lazy: 0,
  _startAt: 0,
  _op: 0,
  _onInit: 0
});
at("staggerTo,staggerFrom,staggerFromTo", function(l) {
  H[l] = function() {
    var t = new nt(), e = Ui.call(arguments, 0);
    return e.splice(l === "staggerFromTo" ? 5 : 4, 0, 0), t[l].apply(t, e);
  };
});
var cr = function(t, e, i) {
  return t[e] = i;
}, Vn = function(t, e, i) {
  return t[e](i);
}, na = function(t, e, i, r) {
  return t[e](r.fp, i);
}, sa = function(t, e, i) {
  return t.setAttribute(e, i);
}, _r = function(t, e) {
  return q(t[e]) ? Vn : rr(t[e]) && t.setAttribute ? sa : cr;
}, Nn = function(t, e) {
  return e.set(e.t, e.p, Math.round((e.s + e.c * t) * 1e6) / 1e6, e);
}, aa = function(t, e) {
  return e.set(e.t, e.p, !!(e.s + e.c * t), e);
}, Xn = function(t, e) {
  var i = e._pt, r = "";
  if (!t && e.b)
    r = e.b;
  else if (t === 1 && e.e)
    r = e.e;
  else {
    for (; i; )
      r = i.p + (i.m ? i.m(i.s + i.c * t) : Math.round((i.s + i.c * t) * 1e4) / 1e4) + r, i = i._next;
    r += e.c;
  }
  e.set(e.t, e.p, r, e);
}, dr = function(t, e) {
  for (var i = e._pt; i; )
    i.r(t, i.d), i = i._next;
}, oa = function(t, e, i, r) {
  for (var n = this._pt, s; n; )
    s = n._next, n.p === r && n.modifier(t, e, i), n = s;
}, ua = function(t) {
  for (var e = this._pt, i, r; e; )
    r = e._next, e.p === t && !e.op || e.op === t ? hi(this, e, "_pt") : e.dep || (i = 1), e = r;
  return !i;
}, la = function(t, e, i, r) {
  r.mSet(t, e, r.m.call(r.tween, i, r.mt), r);
}, Yn = function(t) {
  for (var e = t._pt, i, r, n, s; e; ) {
    for (i = e._next, r = n; r && r.pr > e.pr; )
      r = r._next;
    (e._prev = r ? r._prev : s) ? e._prev._next = e : n = e, (e._next = r) ? r._prev = e : s = e, e = i;
  }
  t._pt = n;
}, ot = /* @__PURE__ */ function() {
  function l(e, i, r, n, s, a, u, o, f) {
    this.t = i, this.s = n, this.c = s, this.p = r, this.r = a || Nn, this.d = u || this, this.set = o || cr, this.pr = f || 0, this._next = e, e && (e._prev = this);
  }
  var t = l.prototype;
  return t.modifier = function(i, r, n) {
    this.mSet = this.mSet || this.set, this.set = la, this.m = i, this.mt = n, this.tween = r;
  }, l;
}();
at(ur + "parent,duration,ease,delay,overwrite,runBackwards,startAt,yoyo,immediateRender,repeat,repeatDelay,data,paused,reversed,lazy,callbackScope,stringFilter,id,yoyoEase,stagger,inherit,repeatRefresh,keyframes,autoRevert,scrollTrigger", function(l) {
  return or[l] = 1;
});
ct.TweenMax = ct.TweenLite = H;
ct.TimelineLite = ct.TimelineMax = nt;
V = new nt({
  sortChildren: !1,
  defaults: be,
  autoRemoveChildren: !0,
  id: "root",
  smoothChildTiming: !0
});
ht.stringFilter = Dn;
var re = [], Qe = {}, fa = [], Br = 0, ha = 0, ki = function(t) {
  return (Qe[t] || fa).map(function(e) {
    return e();
  });
}, Wi = function() {
  var t = Date.now(), e = [];
  t - Br > 2 && (ki("matchMediaInit"), re.forEach(function(i) {
    var r = i.queries, n = i.conditions, s, a, u, o;
    for (a in r)
      s = pt.matchMedia(r[a]).matches, s && (u = 1), s !== n[a] && (n[a] = s, o = 1);
    o && (i.revert(), u && e.push(i));
  }), ki("matchMediaRevert"), e.forEach(function(i) {
    return i.onMatch(i);
  }), Br = t, ki("matchMedia"));
}, Un = /* @__PURE__ */ function() {
  function l(e, i) {
    this.selector = i && qi(i), this.data = [], this._r = [], this.isReverted = !1, this.id = ha++, e && this.add(e);
  }
  var t = l.prototype;
  return t.add = function(i, r, n) {
    q(i) && (n = r, r = i, i = q);
    var s = this, a = function() {
      var o = U, f = s.selector, h;
      return o && o !== s && o.data.push(s), n && (s.selector = qi(n)), U = s, h = r.apply(s, arguments), q(h) && s._r.push(h), U = o, s.selector = f, s.isReverted = !1, h;
    };
    return s.last = a, i === q ? a(s) : i ? s[i] = a : a;
  }, t.ignore = function(i) {
    var r = U;
    U = null, i(this), U = r;
  }, t.getTweens = function() {
    var i = [];
    return this.data.forEach(function(r) {
      return r instanceof l ? i.push.apply(i, r.getTweens()) : r instanceof H && !(r.parent && r.parent.data === "nested") && i.push(r);
    }), i;
  }, t.clear = function() {
    this._r.length = this.data.length = 0;
  }, t.kill = function(i, r) {
    var n = this;
    if (i) {
      var s = this.getTweens();
      this.data.forEach(function(u) {
        u.data === "isFlip" && (u.revert(), u.getChildren(!0, !0, !1).forEach(function(o) {
          return s.splice(s.indexOf(o), 1);
        }));
      }), s.map(function(u) {
        return {
          g: u.globalTime(0),
          t: u
        };
      }).sort(function(u, o) {
        return o.g - u.g || -1 / 0;
      }).forEach(function(u) {
        return u.t.revert(i);
      }), this.data.forEach(function(u) {
        return !(u instanceof H) && u.revert && u.revert(i);
      }), this._r.forEach(function(u) {
        return u(i, n);
      }), this.isReverted = !0;
    } else
      this.data.forEach(function(u) {
        return u.kill && u.kill();
      });
    if (this.clear(), r)
      for (var a = re.length; a--; )
        re[a].id === this.id && re.splice(a, 1);
  }, t.revert = function(i) {
    this.kill(i || {});
  }, l;
}(), ca = /* @__PURE__ */ function() {
  function l(e) {
    this.contexts = [], this.scope = e;
  }
  var t = l.prototype;
  return t.add = function(i, r, n) {
    Mt(i) || (i = {
      matches: i
    });
    var s = new Un(0, n || this.scope), a = s.conditions = {}, u, o, f;
    U && !s.selector && (s.selector = U.selector), this.contexts.push(s), r = s.add("onMatch", r), s.queries = i;
    for (o in i)
      o === "all" ? f = 1 : (u = pt.matchMedia(i[o]), u && (re.indexOf(s) < 0 && re.push(s), (a[o] = u.matches) && (f = 1), u.addListener ? u.addListener(Wi) : u.addEventListener("change", Wi)));
    return f && r(s), this;
  }, t.revert = function(i) {
    this.kill(i || {});
  }, t.kill = function(i) {
    this.contexts.forEach(function(r) {
      return r.kill(i, !0);
    });
  }, l;
}(), si = {
  registerPlugin: function() {
    for (var t = arguments.length, e = new Array(t), i = 0; i < t; i++)
      e[i] = arguments[i];
    e.forEach(function(r) {
      return On(r);
    });
  },
  timeline: function(t) {
    return new nt(t);
  },
  getTweensOf: function(t, e) {
    return V.getTweensOf(t, e);
  },
  getProperty: function(t, e, i, r) {
    j(t) && (t = gt(t)[0]);
    var n = te(t || {}).get, s = i ? pn : dn;
    return i === "native" && (i = ""), t && (e ? s((lt[e] && lt[e].get || n)(t, e, i, r)) : function(a, u, o) {
      return s((lt[a] && lt[a].get || n)(t, a, u, o));
    });
  },
  quickSetter: function(t, e, i) {
    if (t = gt(t), t.length > 1) {
      var r = t.map(function(f) {
        return ut.quickSetter(f, e, i);
      }), n = r.length;
      return function(f) {
        for (var h = n; h--; )
          r[h](f);
      };
    }
    t = t[0] || {};
    var s = lt[e], a = te(t), u = a.harness && (a.harness.aliases || {})[e] || e, o = s ? function(f) {
      var h = new s();
      ce._pt = 0, h.init(t, i ? f + i : f, ce, 0, [t]), h.render(1, h), ce._pt && dr(1, ce);
    } : a.set(t, u);
    return s ? o : function(f) {
      return o(t, u, i ? f + i : f, a, 1);
    };
  },
  quickTo: function(t, e, i) {
    var r, n = ut.to(t, se((r = {}, r[e] = "+=0.1", r.paused = !0, r), i || {})), s = function(u, o, f) {
      return n.resetTo(e, u, o, f);
    };
    return s.tween = n, s;
  },
  isTweening: function(t) {
    return V.getTweensOf(t, !0).length > 0;
  },
  defaults: function(t) {
    return t && t.ease && (t.ease = ie(t.ease, be.ease)), Ar(be, t || {});
  },
  config: function(t) {
    return Ar(ht, t || {});
  },
  registerEffect: function(t) {
    var e = t.name, i = t.effect, r = t.plugins, n = t.defaults, s = t.extendTimeline;
    (r || "").split(",").forEach(function(a) {
      return a && !lt[a] && !ct[a] && ei(e + " effect requires " + a + " plugin.");
    }), bi[e] = function(a, u, o) {
      return i(gt(a), vt(u || {}, n), o);
    }, s && (nt.prototype[e] = function(a, u, o) {
      return this.add(bi[e](a, Mt(u) ? u : (o = u) && {}, this), o);
    });
  },
  registerEase: function(t, e) {
    D[t] = ie(e);
  },
  parseEase: function(t, e) {
    return arguments.length ? ie(t, e) : D;
  },
  getById: function(t) {
    return V.getById(t);
  },
  exportRoot: function(t, e) {
    t === void 0 && (t = {});
    var i = new nt(t), r, n;
    for (i.smoothChildTiming = st(t.smoothChildTiming), V.remove(i), i._dp = 0, i._time = i._tTime = V._time, r = V._first; r; )
      n = r._next, (e || !(!r._dur && r instanceof H && r.vars.onComplete === r._targets[0])) && St(i, r, r._start - r._delay), r = n;
    return St(V, i, 0), i;
  },
  context: function(t, e) {
    return t ? new Un(t, e) : U;
  },
  matchMedia: function(t) {
    return new ca(t);
  },
  matchMediaRefresh: function() {
    return re.forEach(function(t) {
      var e = t.conditions, i, r;
      for (r in e)
        e[r] && (e[r] = !1, i = 1);
      i && t.revert();
    }) || Wi();
  },
  addEventListener: function(t, e) {
    var i = Qe[t] || (Qe[t] = []);
    ~i.indexOf(e) || i.push(e);
  },
  removeEventListener: function(t, e) {
    var i = Qe[t], r = i && i.indexOf(e);
    r >= 0 && i.splice(r, 1);
  },
  utils: {
    wrap: qs,
    wrapYoyo: Gs,
    distribute: wn,
    random: Pn,
    snap: Tn,
    normalize: Us,
    getUnit: J,
    clamp: Vs,
    splitColor: Mn,
    toArray: gt,
    selector: qi,
    mapRange: Sn,
    pipe: Xs,
    unitize: Ys,
    interpolate: $s,
    shuffle: bn
  },
  install: ln,
  effects: bi,
  ticker: ft,
  updateRoot: nt.updateRoot,
  plugins: lt,
  globalTimeline: V,
  core: {
    PropTween: ot,
    globals: fn,
    Tween: H,
    Timeline: nt,
    Animation: Xe,
    getCache: te,
    _removeLinkedListItem: hi,
    reverting: function() {
      return tt;
    },
    context: function(t) {
      return t && U && (U.data.push(t), t._ctx = U), U;
    },
    suppressOverwrites: function(t) {
      return ir = t;
    }
  }
};
at("to,from,fromTo,delayedCall,set,killTweensOf", function(l) {
  return si[l] = H[l];
});
ft.add(nt.updateRoot);
ce = si.to({}, {
  duration: 0
});
var _a = function(t, e) {
  for (var i = t._pt; i && i.p !== e && i.op !== e && i.fp !== e; )
    i = i._next;
  return i;
}, da = function(t, e) {
  var i = t._targets, r, n, s;
  for (r in e)
    for (n = i.length; n--; )
      s = t._ptLookup[n][r], s && (s = s.d) && (s._pt && (s = _a(s, r)), s && s.modifier && s.modifier(e[r], t, i[n], r));
}, Si = function(t, e) {
  return {
    name: t,
    rawVars: 1,
    //don't pre-process function-based values or "random()" strings.
    init: function(r, n, s) {
      s._onInit = function(a) {
        var u, o;
        if (j(n) && (u = {}, at(n, function(f) {
          return u[f] = 1;
        }), n = u), e) {
          u = {};
          for (o in n)
            u[o] = e(n[o]);
          n = u;
        }
        da(a, n);
      };
    }
  };
}, ut = si.registerPlugin({
  name: "attr",
  init: function(t, e, i, r, n) {
    var s, a, u;
    this.tween = i;
    for (s in e)
      u = t.getAttribute(s) || "", a = this.add(t, "setAttribute", (u || 0) + "", e[s], r, n, 0, 0, s), a.op = s, a.b = u, this._props.push(s);
  },
  render: function(t, e) {
    for (var i = e._pt; i; )
      tt ? i.set(i.t, i.p, i.b, i) : i.r(t, i.d), i = i._next;
  }
}, {
  name: "endArray",
  init: function(t, e) {
    for (var i = e.length; i--; )
      this.add(t, i, t[i] || 0, e[i], 0, 0, 0, 0, 0, 1);
  }
}, Si("roundProps", Gi), Si("modifiers"), Si("snap", Tn)) || si;
H.version = nt.version = ut.version = "3.12.2";
un = 1;
nr() && Pe();
D.Power0;
D.Power1;
D.Power2;
D.Power3;
D.Power4;
D.Linear;
D.Quad;
D.Cubic;
D.Quart;
D.Quint;
D.Strong;
D.Elastic;
D.Back;
D.SteppedEase;
D.Bounce;
D.Sine;
D.Expo;
D.Circ;
/*!
 * CSSPlugin 3.12.2
 * https://greensock.com
 *
 * Copyright 2008-2023, GreenSock. All rights reserved.
 * Subject to the terms at https://greensock.com/standard-license or for
 * Club GreenSock members, the agreement issued with that membership.
 * @author: Jack Doyle, jack@greensock.com
*/
var zr, Yt, me, pr, Jt, Vr, mr, pa = function() {
  return typeof window < "u";
}, Vt = {}, Qt = 180 / Math.PI, ge = Math.PI / 180, fe = Math.atan2, Nr = 1e8, gr = /([A-Z])/g, ma = /(left|right|width|margin|padding|x)/i, ga = /[\s,\(]\S/, Ct = {
  autoAlpha: "opacity,visibility",
  scale: "scaleX,scaleY",
  alpha: "opacity"
}, Hi = function(t, e) {
  return e.set(e.t, e.p, Math.round((e.s + e.c * t) * 1e4) / 1e4 + e.u, e);
}, ya = function(t, e) {
  return e.set(e.t, e.p, t === 1 ? e.e : Math.round((e.s + e.c * t) * 1e4) / 1e4 + e.u, e);
}, xa = function(t, e) {
  return e.set(e.t, e.p, t ? Math.round((e.s + e.c * t) * 1e4) / 1e4 + e.u : e.b, e);
}, va = function(t, e) {
  var i = e.s + e.c * t;
  e.set(e.t, e.p, ~~(i + (i < 0 ? -0.5 : 0.5)) + e.u, e);
}, qn = function(t, e) {
  return e.set(e.t, e.p, t ? e.e : e.b, e);
}, Gn = function(t, e) {
  return e.set(e.t, e.p, t !== 1 ? e.b : e.e, e);
}, ba = function(t, e, i) {
  return t.style[e] = i;
}, wa = function(t, e, i) {
  return t.style.setProperty(e, i);
}, Ta = function(t, e, i) {
  return t._gsap[e] = i;
}, Pa = function(t, e, i) {
  return t._gsap.scaleX = t._gsap.scaleY = i;
}, ka = function(t, e, i, r, n) {
  var s = t._gsap;
  s.scaleX = s.scaleY = i, s.renderTransform(n, s);
}, Sa = function(t, e, i, r, n) {
  var s = t._gsap;
  s[e] = i, s.renderTransform(n, s);
}, N = "transform", wt = N + "Origin", Ca = function l(t, e) {
  var i = this, r = this.target, n = r.style;
  if (t in Vt && n) {
    if (this.tfm = this.tfm || {}, t !== "transform")
      t = Ct[t] || t, ~t.indexOf(",") ? t.split(",").forEach(function(s) {
        return i.tfm[s] = It(r, s);
      }) : this.tfm[t] = r._gsap.x ? r._gsap[t] : It(r, t);
    else
      return Ct.transform.split(",").forEach(function(s) {
        return l.call(i, s, e);
      });
    if (this.props.indexOf(N) >= 0)
      return;
    r._gsap.svg && (this.svgo = r.getAttribute("data-svg-origin"), this.props.push(wt, e, "")), t = N;
  }
  (n || e) && this.props.push(t, e, n[t]);
}, $n = function(t) {
  t.translate && (t.removeProperty("translate"), t.removeProperty("scale"), t.removeProperty("rotate"));
}, Oa = function() {
  var t = this.props, e = this.target, i = e.style, r = e._gsap, n, s;
  for (n = 0; n < t.length; n += 3)
    t[n + 1] ? e[t[n]] = t[n + 2] : t[n + 2] ? i[t[n]] = t[n + 2] : i.removeProperty(t[n].substr(0, 2) === "--" ? t[n] : t[n].replace(gr, "-$1").toLowerCase());
  if (this.tfm) {
    for (s in this.tfm)
      r[s] = this.tfm[s];
    r.svg && (r.renderTransform(), e.setAttribute("data-svg-origin", this.svgo || "")), n = mr(), (!n || !n.isStart) && !i[N] && ($n(i), r.uncache = 1);
  }
}, Wn = function(t, e) {
  var i = {
    target: t,
    props: [],
    revert: Oa,
    save: Ca
  };
  return t._gsap || ut.core.getCache(t), e && e.split(",").forEach(function(r) {
    return i.save(r);
  }), i;
}, Hn, Zi = function(t, e) {
  var i = Yt.createElementNS ? Yt.createElementNS((e || "http://www.w3.org/1999/xhtml").replace(/^https/, "http"), t) : Yt.createElement(t);
  return i.style ? i : Yt.createElement(t);
}, Ot = function l(t, e, i) {
  var r = getComputedStyle(t);
  return r[e] || r.getPropertyValue(e.replace(gr, "-$1").toLowerCase()) || r.getPropertyValue(e) || !i && l(t, ke(e) || e, 1) || "";
}, Xr = "O,Moz,ms,Ms,Webkit".split(","), ke = function(t, e, i) {
  var r = e || Jt, n = r.style, s = 5;
  if (t in n && !i)
    return t;
  for (t = t.charAt(0).toUpperCase() + t.substr(1); s-- && !(Xr[s] + t in n); )
    ;
  return s < 0 ? null : (s === 3 ? "ms" : s >= 0 ? Xr[s] : "") + t;
}, ji = function() {
  pa() && window.document && (zr = window, Yt = zr.document, me = Yt.documentElement, Jt = Zi("div") || {
    style: {}
  }, Zi("div"), N = ke(N), wt = N + "Origin", Jt.style.cssText = "border-width:0;line-height:0;position:absolute;padding:0", Hn = !!ke("perspective"), mr = ut.core.reverting, pr = 1);
}, Ci = function l(t) {
  var e = Zi("svg", this.ownerSVGElement && this.ownerSVGElement.getAttribute("xmlns") || "http://www.w3.org/2000/svg"), i = this.parentNode, r = this.nextSibling, n = this.style.cssText, s;
  if (me.appendChild(e), e.appendChild(this), this.style.display = "block", t)
    try {
      s = this.getBBox(), this._gsapBBox = this.getBBox, this.getBBox = l;
    } catch {
    }
  else
    this._gsapBBox && (s = this._gsapBBox());
  return i && (r ? i.insertBefore(this, r) : i.appendChild(this)), me.removeChild(e), this.style.cssText = n, s;
}, Yr = function(t, e) {
  for (var i = e.length; i--; )
    if (t.hasAttribute(e[i]))
      return t.getAttribute(e[i]);
}, Zn = function(t) {
  var e;
  try {
    e = t.getBBox();
  } catch {
    e = Ci.call(t, !0);
  }
  return e && (e.width || e.height) || t.getBBox === Ci || (e = Ci.call(t, !0)), e && !e.width && !e.x && !e.y ? {
    x: +Yr(t, ["x", "cx", "x1"]) || 0,
    y: +Yr(t, ["y", "cy", "y1"]) || 0,
    width: 0,
    height: 0
  } : e;
}, jn = function(t) {
  return !!(t.getCTM && (!t.parentNode || t.ownerSVGElement) && Zn(t));
}, Ye = function(t, e) {
  if (e) {
    var i = t.style;
    e in Vt && e !== wt && (e = N), i.removeProperty ? ((e.substr(0, 2) === "ms" || e.substr(0, 6) === "webkit") && (e = "-" + e), i.removeProperty(e.replace(gr, "-$1").toLowerCase())) : i.removeAttribute(e);
  }
}, Ut = function(t, e, i, r, n, s) {
  var a = new ot(t._pt, e, i, 0, 1, s ? Gn : qn);
  return t._pt = a, a.b = r, a.e = n, t._props.push(i), a;
}, Ur = {
  deg: 1,
  rad: 1,
  turn: 1
}, Ma = {
  grid: 1,
  flex: 1
}, Wt = function l(t, e, i, r) {
  var n = parseFloat(i) || 0, s = (i + "").trim().substr((n + "").length) || "px", a = Jt.style, u = ma.test(e), o = t.tagName.toLowerCase() === "svg", f = (o ? "client" : "offset") + (u ? "Width" : "Height"), h = 100, _ = r === "px", d = r === "%", p, c, m, g;
  return r === s || !n || Ur[r] || Ur[s] ? n : (s !== "px" && !_ && (n = l(t, e, i, "px")), g = t.getCTM && jn(t), (d || s === "%") && (Vt[e] || ~e.indexOf("adius")) ? (p = g ? t.getBBox()[u ? "width" : "height"] : t[f], $(d ? n / p * h : n / 100 * p)) : (a[u ? "width" : "height"] = h + (_ ? s : r), c = ~e.indexOf("adius") || r === "em" && t.appendChild && !o ? t : t.parentNode, g && (c = (t.ownerSVGElement || {}).parentNode), (!c || c === Yt || !c.appendChild) && (c = Yt.body), m = c._gsap, m && d && m.width && u && m.time === ft.time && !m.uncache ? $(n / m.width * h) : ((d || s === "%") && !Ma[Ot(c, "display")] && (a.position = Ot(t, "position")), c === t && (a.position = "static"), c.appendChild(Jt), p = Jt[f], c.removeChild(Jt), a.position = "absolute", u && d && (m = te(c), m.time = ft.time, m.width = c[f]), $(_ ? p * n / h : p && n ? h / p * n : 0))));
}, It = function(t, e, i, r) {
  var n;
  return pr || ji(), e in Ct && e !== "transform" && (e = Ct[e], ~e.indexOf(",") && (e = e.split(",")[0])), Vt[e] && e !== "transform" ? (n = qe(t, r), n = e !== "transformOrigin" ? n[e] : n.svg ? n.origin : oi(Ot(t, wt)) + " " + n.zOrigin + "px") : (n = t.style[e], (!n || n === "auto" || r || ~(n + "").indexOf("calc(")) && (n = ai[e] && ai[e](t, e, i) || Ot(t, e) || cn(t, e) || (e === "opacity" ? 1 : 0))), i && !~(n + "").trim().indexOf(" ") ? Wt(t, e, n, i) + i : n;
}, Ea = function(t, e, i, r) {
  if (!i || i === "none") {
    var n = ke(e, t, 1), s = n && Ot(t, n, 1);
    s && s !== i ? (e = n, i = s) : e === "borderColor" && (i = Ot(t, "borderTopColor"));
  }
  var a = new ot(this._pt, t.style, e, 0, 1, Xn), u = 0, o = 0, f, h, _, d, p, c, m, g, v, y, b, x;
  if (a.b = i, a.e = r, i += "", r += "", r === "auto" && (t.style[e] = r, r = Ot(t, e) || r, t.style[e] = i), f = [i, r], Dn(f), i = f[0], r = f[1], _ = i.match(he) || [], x = r.match(he) || [], x.length) {
    for (; h = he.exec(r); )
      m = h[0], v = r.substring(u, h.index), p ? p = (p + 1) % 5 : (v.substr(-5) === "rgba(" || v.substr(-5) === "hsla(") && (p = 1), m !== (c = _[o++] || "") && (d = parseFloat(c) || 0, b = c.substr((d + "").length), m.charAt(1) === "=" && (m = pe(d, m) + b), g = parseFloat(m), y = m.substr((g + "").length), u = he.lastIndex - y.length, y || (y = y || ht.units[e] || b, u === r.length && (r += y, a.e += y)), b !== y && (d = Wt(t, e, c, y) || 0), a._pt = {
        _next: a._pt,
        p: v || o === 1 ? v : ",",
        //note: SVG spec allows omission of comma/space when a negative sign is wedged between two numbers, like 2.5-5.3 instead of 2.5,-5.3 but when tweening, the negative value may switch to positive, so we insert the comma just in case.
        s: d,
        c: g - d,
        m: p && p < 4 || e === "zIndex" ? Math.round : 0
      });
    a.c = u < r.length ? r.substring(u, r.length) : "";
  } else
    a.r = e === "display" && r === "none" ? Gn : qn;
  return an.test(r) && (a.e = 0), this._pt = a, a;
}, qr = {
  top: "0%",
  bottom: "100%",
  left: "0%",
  right: "100%",
  center: "50%"
}, Da = function(t) {
  var e = t.split(" "), i = e[0], r = e[1] || "50%";
  return (i === "top" || i === "bottom" || r === "left" || r === "right") && (t = i, i = r, r = t), e[0] = qr[i] || i, e[1] = qr[r] || r, e.join(" ");
}, Aa = function(t, e) {
  if (e.tween && e.tween._time === e.tween._dur) {
    var i = e.t, r = i.style, n = e.u, s = i._gsap, a, u, o;
    if (n === "all" || n === !0)
      r.cssText = "", u = 1;
    else
      for (n = n.split(","), o = n.length; --o > -1; )
        a = n[o], Vt[a] && (u = 1, a = a === "transformOrigin" ? wt : N), Ye(i, a);
    u && (Ye(i, N), s && (s.svg && i.removeAttribute("transform"), qe(i, 1), s.uncache = 1, $n(r)));
  }
}, ai = {
  clearProps: function(t, e, i, r, n) {
    if (n.data !== "isFromStart") {
      var s = t._pt = new ot(t._pt, e, i, 0, 0, Aa);
      return s.u = r, s.pr = -10, s.tween = n, t._props.push(i), 1;
    }
  }
  /* className feature (about 0.4kb gzipped).
  , className(plugin, target, property, endValue, tween) {
  	let _renderClassName = (ratio, data) => {
  			data.css.render(ratio, data.css);
  			if (!ratio || ratio === 1) {
  				let inline = data.rmv,
  					target = data.t,
  					p;
  				target.setAttribute("class", ratio ? data.e : data.b);
  				for (p in inline) {
  					_removeProperty(target, p);
  				}
  			}
  		},
  		_getAllStyles = (target) => {
  			let styles = {},
  				computed = getComputedStyle(target),
  				p;
  			for (p in computed) {
  				if (isNaN(p) && p !== "cssText" && p !== "length") {
  					styles[p] = computed[p];
  				}
  			}
  			_setDefaults(styles, _parseTransform(target, 1));
  			return styles;
  		},
  		startClassList = target.getAttribute("class"),
  		style = target.style,
  		cssText = style.cssText,
  		cache = target._gsap,
  		classPT = cache.classPT,
  		inlineToRemoveAtEnd = {},
  		data = {t:target, plugin:plugin, rmv:inlineToRemoveAtEnd, b:startClassList, e:(endValue.charAt(1) !== "=") ? endValue : startClassList.replace(new RegExp("(?:\\s|^)" + endValue.substr(2) + "(?![\\w-])"), "") + ((endValue.charAt(0) === "+") ? " " + endValue.substr(2) : "")},
  		changingVars = {},
  		startVars = _getAllStyles(target),
  		transformRelated = /(transform|perspective)/i,
  		endVars, p;
  	if (classPT) {
  		classPT.r(1, classPT.d);
  		_removeLinkedListItem(classPT.d.plugin, classPT, "_pt");
  	}
  	target.setAttribute("class", data.e);
  	endVars = _getAllStyles(target, true);
  	target.setAttribute("class", startClassList);
  	for (p in endVars) {
  		if (endVars[p] !== startVars[p] && !transformRelated.test(p)) {
  			changingVars[p] = endVars[p];
  			if (!style[p] && style[p] !== "0") {
  				inlineToRemoveAtEnd[p] = 1;
  			}
  		}
  	}
  	cache.classPT = plugin._pt = new PropTween(plugin._pt, target, "className", 0, 0, _renderClassName, data, 0, -11);
  	if (style.cssText !== cssText) { //only apply if things change. Otherwise, in cases like a background-image that's pulled dynamically, it could cause a refresh. See https://greensock.com/forums/topic/20368-possible-gsap-bug-switching-classnames-in-chrome/.
  		style.cssText = cssText; //we recorded cssText before we swapped classes and ran _getAllStyles() because in cases when a className tween is overwritten, we remove all the related tweening properties from that class change (otherwise class-specific stuff can't override properties we've directly set on the target's style object due to specificity).
  	}
  	_parseTransform(target, true); //to clear the caching of transforms
  	data.css = new gsap.plugins.css();
  	data.css.init(target, changingVars, tween);
  	plugin._props.push(...data.css._props);
  	return 1;
  }
  */
}, Ue = [1, 0, 0, 1, 0, 0], Kn = {}, Qn = function(t) {
  return t === "matrix(1, 0, 0, 1, 0, 0)" || t === "none" || !t;
}, Gr = function(t) {
  var e = Ot(t, N);
  return Qn(e) ? Ue : e.substr(7).match(sn).map($);
}, yr = function(t, e) {
  var i = t._gsap || te(t), r = t.style, n = Gr(t), s, a, u, o;
  return i.svg && t.getAttribute("transform") ? (u = t.transform.baseVal.consolidate().matrix, n = [u.a, u.b, u.c, u.d, u.e, u.f], n.join(",") === "1,0,0,1,0,0" ? Ue : n) : (n === Ue && !t.offsetParent && t !== me && !i.svg && (u = r.display, r.display = "block", s = t.parentNode, (!s || !t.offsetParent) && (o = 1, a = t.nextElementSibling, me.appendChild(t)), n = Gr(t), u ? r.display = u : Ye(t, "display"), o && (a ? s.insertBefore(t, a) : s ? s.appendChild(t) : me.removeChild(t))), e && n.length > 6 ? [n[0], n[1], n[4], n[5], n[12], n[13]] : n);
}, Ki = function(t, e, i, r, n, s) {
  var a = t._gsap, u = n || yr(t, !0), o = a.xOrigin || 0, f = a.yOrigin || 0, h = a.xOffset || 0, _ = a.yOffset || 0, d = u[0], p = u[1], c = u[2], m = u[3], g = u[4], v = u[5], y = e.split(" "), b = parseFloat(y[0]) || 0, x = parseFloat(y[1]) || 0, P, k, T, w;
  i ? u !== Ue && (k = d * m - p * c) && (T = b * (m / k) + x * (-c / k) + (c * v - m * g) / k, w = b * (-p / k) + x * (d / k) - (d * v - p * g) / k, b = T, x = w) : (P = Zn(t), b = P.x + (~y[0].indexOf("%") ? b / 100 * P.width : b), x = P.y + (~(y[1] || y[0]).indexOf("%") ? x / 100 * P.height : x)), r || r !== !1 && a.smooth ? (g = b - o, v = x - f, a.xOffset = h + (g * d + v * c) - g, a.yOffset = _ + (g * p + v * m) - v) : a.xOffset = a.yOffset = 0, a.xOrigin = b, a.yOrigin = x, a.smooth = !!r, a.origin = e, a.originIsAbsolute = !!i, t.style[wt] = "0px 0px", s && (Ut(s, a, "xOrigin", o, b), Ut(s, a, "yOrigin", f, x), Ut(s, a, "xOffset", h, a.xOffset), Ut(s, a, "yOffset", _, a.yOffset)), t.setAttribute("data-svg-origin", b + " " + x);
}, qe = function(t, e) {
  var i = t._gsap || new In(t);
  if ("x" in i && !e && !i.uncache)
    return i;
  var r = t.style, n = i.scaleX < 0, s = "px", a = "deg", u = getComputedStyle(t), o = Ot(t, wt) || "0", f, h, _, d, p, c, m, g, v, y, b, x, P, k, T, w, S, O, A, R, E, C, z, X, K, bt, Pt, _t, G, Ce, Z, F;
  return f = h = _ = c = m = g = v = y = b = 0, d = p = 1, i.svg = !!(t.getCTM && jn(t)), u.translate && ((u.translate !== "none" || u.scale !== "none" || u.rotate !== "none") && (r[N] = (u.translate !== "none" ? "translate3d(" + (u.translate + " 0 0").split(" ").slice(0, 3).join(", ") + ") " : "") + (u.rotate !== "none" ? "rotate(" + u.rotate + ") " : "") + (u.scale !== "none" ? "scale(" + u.scale.split(" ").join(",") + ") " : "") + (u[N] !== "none" ? u[N] : "")), r.scale = r.rotate = r.translate = "none"), k = yr(t, i.svg), i.svg && (i.uncache ? (K = t.getBBox(), o = i.xOrigin - K.x + "px " + (i.yOrigin - K.y) + "px", X = "") : X = !e && t.getAttribute("data-svg-origin"), Ki(t, X || o, !!X || i.originIsAbsolute, i.smooth !== !1, k)), x = i.xOrigin || 0, P = i.yOrigin || 0, k !== Ue && (O = k[0], A = k[1], R = k[2], E = k[3], f = C = k[4], h = z = k[5], k.length === 6 ? (d = Math.sqrt(O * O + A * A), p = Math.sqrt(E * E + R * R), c = O || A ? fe(A, O) * Qt : 0, v = R || E ? fe(R, E) * Qt + c : 0, v && (p *= Math.abs(Math.cos(v * ge))), i.svg && (f -= x - (x * O + P * R), h -= P - (x * A + P * E))) : (F = k[6], Ce = k[7], Pt = k[8], _t = k[9], G = k[10], Z = k[11], f = k[12], h = k[13], _ = k[14], T = fe(F, G), m = T * Qt, T && (w = Math.cos(-T), S = Math.sin(-T), X = C * w + Pt * S, K = z * w + _t * S, bt = F * w + G * S, Pt = C * -S + Pt * w, _t = z * -S + _t * w, G = F * -S + G * w, Z = Ce * -S + Z * w, C = X, z = K, F = bt), T = fe(-R, G), g = T * Qt, T && (w = Math.cos(-T), S = Math.sin(-T), X = O * w - Pt * S, K = A * w - _t * S, bt = R * w - G * S, Z = E * S + Z * w, O = X, A = K, R = bt), T = fe(A, O), c = T * Qt, T && (w = Math.cos(T), S = Math.sin(T), X = O * w + A * S, K = C * w + z * S, A = A * w - O * S, z = z * w - C * S, O = X, C = K), m && Math.abs(m) + Math.abs(c) > 359.9 && (m = c = 0, g = 180 - g), d = $(Math.sqrt(O * O + A * A + R * R)), p = $(Math.sqrt(z * z + F * F)), T = fe(C, z), v = Math.abs(T) > 2e-4 ? T * Qt : 0, b = Z ? 1 / (Z < 0 ? -Z : Z) : 0), i.svg && (X = t.getAttribute("transform"), i.forceCSS = t.setAttribute("transform", "") || !Qn(Ot(t, N)), X && t.setAttribute("transform", X))), Math.abs(v) > 90 && Math.abs(v) < 270 && (n ? (d *= -1, v += c <= 0 ? 180 : -180, c += c <= 0 ? 180 : -180) : (p *= -1, v += v <= 0 ? 180 : -180)), e = e || i.uncache, i.x = f - ((i.xPercent = f && (!e && i.xPercent || (Math.round(t.offsetWidth / 2) === Math.round(-f) ? -50 : 0))) ? t.offsetWidth * i.xPercent / 100 : 0) + s, i.y = h - ((i.yPercent = h && (!e && i.yPercent || (Math.round(t.offsetHeight / 2) === Math.round(-h) ? -50 : 0))) ? t.offsetHeight * i.yPercent / 100 : 0) + s, i.z = _ + s, i.scaleX = $(d), i.scaleY = $(p), i.rotation = $(c) + a, i.rotationX = $(m) + a, i.rotationY = $(g) + a, i.skewX = v + a, i.skewY = y + a, i.transformPerspective = b + s, (i.zOrigin = parseFloat(o.split(" ")[2]) || 0) && (r[wt] = oi(o)), i.xOffset = i.yOffset = 0, i.force3D = ht.force3D, i.renderTransform = i.svg ? Fa : Hn ? Jn : Ra, i.uncache = 0, i;
}, oi = function(t) {
  return (t = t.split(" "))[0] + " " + t[1];
}, Oi = function(t, e, i) {
  var r = J(e);
  return $(parseFloat(e) + parseFloat(Wt(t, "x", i + "px", r))) + r;
}, Ra = function(t, e) {
  e.z = "0px", e.rotationY = e.rotationX = "0deg", e.force3D = 0, Jn(t, e);
}, jt = "0deg", Oe = "0px", Kt = ") ", Jn = function(t, e) {
  var i = e || this, r = i.xPercent, n = i.yPercent, s = i.x, a = i.y, u = i.z, o = i.rotation, f = i.rotationY, h = i.rotationX, _ = i.skewX, d = i.skewY, p = i.scaleX, c = i.scaleY, m = i.transformPerspective, g = i.force3D, v = i.target, y = i.zOrigin, b = "", x = g === "auto" && t && t !== 1 || g === !0;
  if (y && (h !== jt || f !== jt)) {
    var P = parseFloat(f) * ge, k = Math.sin(P), T = Math.cos(P), w;
    P = parseFloat(h) * ge, w = Math.cos(P), s = Oi(v, s, k * w * -y), a = Oi(v, a, -Math.sin(P) * -y), u = Oi(v, u, T * w * -y + y);
  }
  m !== Oe && (b += "perspective(" + m + Kt), (r || n) && (b += "translate(" + r + "%, " + n + "%) "), (x || s !== Oe || a !== Oe || u !== Oe) && (b += u !== Oe || x ? "translate3d(" + s + ", " + a + ", " + u + ") " : "translate(" + s + ", " + a + Kt), o !== jt && (b += "rotate(" + o + Kt), f !== jt && (b += "rotateY(" + f + Kt), h !== jt && (b += "rotateX(" + h + Kt), (_ !== jt || d !== jt) && (b += "skew(" + _ + ", " + d + Kt), (p !== 1 || c !== 1) && (b += "scale(" + p + ", " + c + Kt), v.style[N] = b || "translate(0, 0)";
}, Fa = function(t, e) {
  var i = e || this, r = i.xPercent, n = i.yPercent, s = i.x, a = i.y, u = i.rotation, o = i.skewX, f = i.skewY, h = i.scaleX, _ = i.scaleY, d = i.target, p = i.xOrigin, c = i.yOrigin, m = i.xOffset, g = i.yOffset, v = i.forceCSS, y = parseFloat(s), b = parseFloat(a), x, P, k, T, w;
  u = parseFloat(u), o = parseFloat(o), f = parseFloat(f), f && (f = parseFloat(f), o += f, u += f), u || o ? (u *= ge, o *= ge, x = Math.cos(u) * h, P = Math.sin(u) * h, k = Math.sin(u - o) * -_, T = Math.cos(u - o) * _, o && (f *= ge, w = Math.tan(o - f), w = Math.sqrt(1 + w * w), k *= w, T *= w, f && (w = Math.tan(f), w = Math.sqrt(1 + w * w), x *= w, P *= w)), x = $(x), P = $(P), k = $(k), T = $(T)) : (x = h, T = _, P = k = 0), (y && !~(s + "").indexOf("px") || b && !~(a + "").indexOf("px")) && (y = Wt(d, "x", s, "px"), b = Wt(d, "y", a, "px")), (p || c || m || g) && (y = $(y + p - (p * x + c * k) + m), b = $(b + c - (p * P + c * T) + g)), (r || n) && (w = d.getBBox(), y = $(y + r / 100 * w.width), b = $(b + n / 100 * w.height)), w = "matrix(" + x + "," + P + "," + k + "," + T + "," + y + "," + b + ")", d.setAttribute("transform", w), v && (d.style[N] = w);
}, Ia = function(t, e, i, r, n) {
  var s = 360, a = j(n), u = parseFloat(n) * (a && ~n.indexOf("rad") ? Qt : 1), o = u - r, f = r + o + "deg", h, _;
  return a && (h = n.split("_")[1], h === "short" && (o %= s, o !== o % (s / 2) && (o += o < 0 ? s : -s)), h === "cw" && o < 0 ? o = (o + s * Nr) % s - ~~(o / s) * s : h === "ccw" && o > 0 && (o = (o - s * Nr) % s - ~~(o / s) * s)), t._pt = _ = new ot(t._pt, e, i, r, o, ya), _.e = f, _.u = "deg", t._props.push(i), _;
}, $r = function(t, e) {
  for (var i in e)
    t[i] = e[i];
  return t;
}, La = function(t, e, i) {
  var r = $r({}, i._gsap), n = "perspective,force3D,transformOrigin,svgOrigin", s = i.style, a, u, o, f, h, _, d, p;
  r.svg ? (o = i.getAttribute("transform"), i.setAttribute("transform", ""), s[N] = e, a = qe(i, 1), Ye(i, N), i.setAttribute("transform", o)) : (o = getComputedStyle(i)[N], s[N] = e, a = qe(i, 1), s[N] = o);
  for (u in Vt)
    o = r[u], f = a[u], o !== f && n.indexOf(u) < 0 && (d = J(o), p = J(f), h = d !== p ? Wt(i, u, o, p) : parseFloat(o), _ = parseFloat(f), t._pt = new ot(t._pt, a, u, h, _ - h, Hi), t._pt.u = p || 0, t._props.push(u));
  $r(a, r);
};
at("padding,margin,Width,Radius", function(l, t) {
  var e = "Top", i = "Right", r = "Bottom", n = "Left", s = (t < 3 ? [e, i, r, n] : [e + n, e + i, r + i, r + n]).map(function(a) {
    return t < 2 ? l + a : "border" + a + l;
  });
  ai[t > 1 ? "border" + l : l] = function(a, u, o, f, h) {
    var _, d;
    if (arguments.length < 4)
      return _ = s.map(function(p) {
        return It(a, p, o);
      }), d = _.join(" "), d.split(_[0]).length === 5 ? _[0] : d;
    _ = (f + "").split(" "), d = {}, s.forEach(function(p, c) {
      return d[p] = _[c] = _[c] || _[(c - 1) / 2 | 0];
    }), a.init(u, d, h);
  };
});
var ts = {
  name: "css",
  register: ji,
  targetTest: function(t) {
    return t.style && t.nodeType;
  },
  init: function(t, e, i, r, n) {
    var s = this._props, a = t.style, u = i.vars.startAt, o, f, h, _, d, p, c, m, g, v, y, b, x, P, k, T;
    pr || ji(), this.styles = this.styles || Wn(t), T = this.styles.props, this.tween = i;
    for (c in e)
      if (c !== "autoRound" && (f = e[c], !(lt[c] && Ln(c, e, i, r, t, n)))) {
        if (d = typeof f, p = ai[c], d === "function" && (f = f.call(i, r, t, n), d = typeof f), d === "string" && ~f.indexOf("random(") && (f = Ve(f)), p)
          p(this, t, c, f, i) && (k = 1);
        else if (c.substr(0, 2) === "--")
          o = (getComputedStyle(t).getPropertyValue(c) + "").trim(), f += "", Gt.lastIndex = 0, Gt.test(o) || (m = J(o), g = J(f)), g ? m !== g && (o = Wt(t, c, o, g) + g) : m && (f += m), this.add(a, "setProperty", o, f, r, n, 0, 0, c), s.push(c), T.push(c, 0, a[c]);
        else if (d !== "undefined") {
          if (u && c in u ? (o = typeof u[c] == "function" ? u[c].call(i, r, t, n) : u[c], j(o) && ~o.indexOf("random(") && (o = Ve(o)), J(o + "") || (o += ht.units[c] || J(It(t, c)) || ""), (o + "").charAt(1) === "=" && (o = It(t, c))) : o = It(t, c), _ = parseFloat(o), v = d === "string" && f.charAt(1) === "=" && f.substr(0, 2), v && (f = f.substr(2)), h = parseFloat(f), c in Ct && (c === "autoAlpha" && (_ === 1 && It(t, "visibility") === "hidden" && h && (_ = 0), T.push("visibility", 0, a.visibility), Ut(this, a, "visibility", _ ? "inherit" : "hidden", h ? "inherit" : "hidden", !h)), c !== "scale" && c !== "transform" && (c = Ct[c], ~c.indexOf(",") && (c = c.split(",")[0]))), y = c in Vt, y) {
            if (this.styles.save(c), b || (x = t._gsap, x.renderTransform && !e.parseTransform || qe(t, e.parseTransform), P = e.smoothOrigin !== !1 && x.smooth, b = this._pt = new ot(this._pt, a, N, 0, 1, x.renderTransform, x, 0, -1), b.dep = 1), c === "scale")
              this._pt = new ot(this._pt, x, "scaleY", x.scaleY, (v ? pe(x.scaleY, v + h) : h) - x.scaleY || 0, Hi), this._pt.u = 0, s.push("scaleY", c), c += "X";
            else if (c === "transformOrigin") {
              T.push(wt, 0, a[wt]), f = Da(f), x.svg ? Ki(t, f, 0, P, 0, this) : (g = parseFloat(f.split(" ")[2]) || 0, g !== x.zOrigin && Ut(this, x, "zOrigin", x.zOrigin, g), Ut(this, a, c, oi(o), oi(f)));
              continue;
            } else if (c === "svgOrigin") {
              Ki(t, f, 1, P, 0, this);
              continue;
            } else if (c in Kn) {
              Ia(this, x, c, _, v ? pe(_, v + f) : f);
              continue;
            } else if (c === "smoothOrigin") {
              Ut(this, x, "smooth", x.smooth, f);
              continue;
            } else if (c === "force3D") {
              x[c] = f;
              continue;
            } else if (c === "transform") {
              La(this, f, t);
              continue;
            }
          } else
            c in a || (c = ke(c) || c);
          if (y || (h || h === 0) && (_ || _ === 0) && !ga.test(f) && c in a)
            m = (o + "").substr((_ + "").length), h || (h = 0), g = J(f) || (c in ht.units ? ht.units[c] : m), m !== g && (_ = Wt(t, c, o, g)), this._pt = new ot(this._pt, y ? x : a, c, _, (v ? pe(_, v + h) : h) - _, !y && (g === "px" || c === "zIndex") && e.autoRound !== !1 ? va : Hi), this._pt.u = g || 0, m !== g && g !== "%" && (this._pt.b = o, this._pt.r = xa);
          else if (c in a)
            Ea.call(this, t, c, o, v ? v + f : f);
          else if (c in t)
            this.add(t, c, o || t[c], v ? v + f : f, r, n);
          else if (c !== "parseTransform") {
            ar(c, f);
            continue;
          }
          y || (c in a ? T.push(c, 0, a[c]) : T.push(c, 1, o || t[c])), s.push(c);
        }
      }
    k && Yn(this);
  },
  render: function(t, e) {
    if (e.tween._time || !mr())
      for (var i = e._pt; i; )
        i.r(t, i.d), i = i._next;
    else
      e.styles.revert();
  },
  get: It,
  aliases: Ct,
  getSetter: function(t, e, i) {
    var r = Ct[e];
    return r && r.indexOf(",") < 0 && (e = r), e in Vt && e !== wt && (t._gsap.x || It(t, "x")) ? i && Vr === i ? e === "scale" ? Pa : Ta : (Vr = i || {}) && (e === "scale" ? ka : Sa) : t.style && !rr(t.style[e]) ? ba : ~e.indexOf("-") ? wa : _r(t, e);
  },
  core: {
    _removeProperty: Ye,
    _getMatrix: yr
  }
};
ut.utils.checkPrefix = ke;
ut.core.getStyleSaver = Wn;
(function(l, t, e, i) {
  var r = at(l + "," + t + "," + e, function(n) {
    Vt[n] = 1;
  });
  at(t, function(n) {
    ht.units[n] = "deg", Kn[n] = 1;
  }), Ct[r[13]] = l + "," + t, at(i, function(n) {
    var s = n.split(":");
    Ct[s[1]] = r[s[0]];
  });
})("x,y,z,scale,scaleX,scaleY,xPercent,yPercent", "rotation,rotationX,rotationY,skewX,skewY", "transform,transformOrigin,svgOrigin,force3D,smoothOrigin,transformPerspective", "0:translateX,1:translateY,2:translateZ,8:rotate,8:rotationZ,8:rotateZ,9:rotateX,10:rotateY");
at("x,y,z,top,right,bottom,left,width,height,fontSize,padding,margin,perspective", function(l) {
  ht.units[l] = "px";
});
ut.registerPlugin(ts);
var es = ut.registerPlugin(ts) || ut;
es.core.Tween;
/*!
 * matrix 3.12.2
 * https://greensock.com
 *
 * Copyright 2008-2023, GreenSock. All rights reserved.
 * Subject to the terms at https://greensock.com/standard-license or for
 * Club GreenSock members, the agreement issued with that membership.
 * @author: Jack Doyle, jack@greensock.com
*/
var Lt, ne, xr, ye, De, Je, ui, Ie, xt = "transform", Qi = xt + "Origin", is, vr = function(t) {
  var e = t.ownerDocument || t;
  for (!(xt in t.style) && ("msTransform" in t.style) && (xt = "msTransform", Qi = xt + "Origin"); e.parentNode && (e = e.parentNode); )
    ;
  if (ne = window, ui = new ae(), e) {
    Lt = e, xr = e.documentElement, ye = e.body, Ie = Lt.createElementNS("http://www.w3.org/2000/svg", "g"), Ie.style.transform = "none";
    var i = e.createElement("div"), r = e.createElement("div");
    ye.appendChild(i), i.appendChild(r), i.style.position = "static", i.style[xt] = "translate3d(0,0,1px)", is = r.offsetParent !== i, ye.removeChild(i);
  }
  return e;
}, Ba = function(t) {
  for (var e, i; t && t !== ye; )
    i = t._gsap, i && i.uncache && i.get(t, "x"), i && !i.scaleX && !i.scaleY && i.renderTransform && (i.scaleX = i.scaleY = 1e-4, i.renderTransform(1, i), e ? e.push(i) : e = [i]), t = t.parentNode;
  return e;
}, rs = [], ns = [], br = function() {
  return ne.pageYOffset || Lt.scrollTop || xr.scrollTop || ye.scrollTop || 0;
}, wr = function() {
  return ne.pageXOffset || Lt.scrollLeft || xr.scrollLeft || ye.scrollLeft || 0;
}, Tr = function(t) {
  return t.ownerSVGElement || ((t.tagName + "").toLowerCase() === "svg" ? t : null);
}, za = function l(t) {
  if (ne.getComputedStyle(t).position === "fixed")
    return !0;
  if (t = t.parentNode, t && t.nodeType === 1)
    return l(t);
}, Mi = function l(t, e) {
  if (t.parentNode && (Lt || vr(t))) {
    var i = Tr(t), r = i ? i.getAttribute("xmlns") || "http://www.w3.org/2000/svg" : "http://www.w3.org/1999/xhtml", n = i ? e ? "rect" : "g" : "div", s = e !== 2 ? 0 : 100, a = e === 3 ? 100 : 0, u = "position:absolute;display:block;pointer-events:none;margin:0;padding:0;", o = Lt.createElementNS ? Lt.createElementNS(r.replace(/^https/, "http"), n) : Lt.createElement(n);
    return e && (i ? (Je || (Je = l(t)), o.setAttribute("width", 0.01), o.setAttribute("height", 0.01), o.setAttribute("transform", "translate(" + s + "," + a + ")"), Je.appendChild(o)) : (De || (De = l(t), De.style.cssText = u), o.style.cssText = u + "width:0.1px;height:0.1px;top:" + a + "px;left:" + s + "px", De.appendChild(o))), o;
  }
  throw "Need document and parent.";
}, Va = function(t) {
  for (var e = new ae(), i = 0; i < t.numberOfItems; i++)
    e.multiply(t.getItem(i).matrix);
  return e;
}, ss = function(t) {
  var e = t.getCTM(), i;
  return e || (i = t.style[xt], t.style[xt] = "none", t.appendChild(Ie), e = Ie.getCTM(), t.removeChild(Ie), i ? t.style[xt] = i : t.style.removeProperty(xt.replace(/([A-Z])/g, "-$1").toLowerCase())), e || ui.clone();
}, Na = function(t, e) {
  var i = Tr(t), r = t === i, n = i ? rs : ns, s = t.parentNode, a, u, o, f, h, _;
  if (t === ne)
    return t;
  if (n.length || n.push(Mi(t, 1), Mi(t, 2), Mi(t, 3)), a = i ? Je : De, i)
    r ? (o = ss(t), f = -o.e / o.a, h = -o.f / o.d, u = ui) : t.getBBox ? (o = t.getBBox(), u = t.transform ? t.transform.baseVal : {}, u = u.numberOfItems ? u.numberOfItems > 1 ? Va(u) : u.getItem(0).matrix : ui, f = u.a * o.x + u.c * o.y, h = u.b * o.x + u.d * o.y) : (u = new ae(), f = h = 0), e && t.tagName.toLowerCase() === "g" && (f = h = 0), (r ? i : s).appendChild(a), a.setAttribute("transform", "matrix(" + u.a + "," + u.b + "," + u.c + "," + u.d + "," + (u.e + f) + "," + (u.f + h) + ")");
  else {
    if (f = h = 0, is)
      for (u = t.offsetParent, o = t; o && (o = o.parentNode) && o !== u && o.parentNode; )
        (ne.getComputedStyle(o)[xt] + "").length > 4 && (f = o.offsetLeft, h = o.offsetTop, o = 0);
    if (_ = ne.getComputedStyle(t), _.position !== "absolute" && _.position !== "fixed")
      for (u = t.offsetParent; s && s !== u; )
        f += s.scrollLeft || 0, h += s.scrollTop || 0, s = s.parentNode;
    o = a.style, o.top = t.offsetTop - h + "px", o.left = t.offsetLeft - f + "px", o[xt] = _[xt], o[Qi] = _[Qi], o.position = _.position === "fixed" ? "fixed" : "absolute", t.parentNode.appendChild(a);
  }
  return a;
}, Ei = function(t, e, i, r, n, s, a) {
  return t.a = e, t.b = i, t.c = r, t.d = n, t.e = s, t.f = a, t;
}, ae = /* @__PURE__ */ function() {
  function l(e, i, r, n, s, a) {
    e === void 0 && (e = 1), i === void 0 && (i = 0), r === void 0 && (r = 0), n === void 0 && (n = 1), s === void 0 && (s = 0), a === void 0 && (a = 0), Ei(this, e, i, r, n, s, a);
  }
  var t = l.prototype;
  return t.inverse = function() {
    var i = this.a, r = this.b, n = this.c, s = this.d, a = this.e, u = this.f, o = i * s - r * n || 1e-10;
    return Ei(this, s / o, -r / o, -n / o, i / o, (n * u - s * a) / o, -(i * u - r * a) / o);
  }, t.multiply = function(i) {
    var r = this.a, n = this.b, s = this.c, a = this.d, u = this.e, o = this.f, f = i.a, h = i.c, _ = i.b, d = i.d, p = i.e, c = i.f;
    return Ei(this, f * r + _ * s, f * n + _ * a, h * r + d * s, h * n + d * a, u + p * r + c * s, o + p * n + c * a);
  }, t.clone = function() {
    return new l(this.a, this.b, this.c, this.d, this.e, this.f);
  }, t.equals = function(i) {
    var r = this.a, n = this.b, s = this.c, a = this.d, u = this.e, o = this.f;
    return r === i.a && n === i.b && s === i.c && a === i.d && u === i.e && o === i.f;
  }, t.apply = function(i, r) {
    r === void 0 && (r = {});
    var n = i.x, s = i.y, a = this.a, u = this.b, o = this.c, f = this.d, h = this.e, _ = this.f;
    return r.x = n * a + s * o + h || 0, r.y = n * u + s * f + _ || 0, r;
  }, l;
}();
function Et(l, t, e, i) {
  if (!l || !l.parentNode || (Lt || vr(l)).documentElement === l)
    return new ae();
  var r = Ba(l), n = Tr(l), s = n ? rs : ns, a = Na(l, e), u = s[0].getBoundingClientRect(), o = s[1].getBoundingClientRect(), f = s[2].getBoundingClientRect(), h = a.parentNode, _ = !i && za(l), d = new ae((o.left - u.left) / 100, (o.top - u.top) / 100, (f.left - u.left) / 100, (f.top - u.top) / 100, u.left + (_ ? 0 : wr()), u.top + (_ ? 0 : br()));
  if (h.removeChild(a), r)
    for (u = r.length; u--; )
      o = r[u], o.scaleX = o.scaleY = 0, o.renderTransform(1, o);
  return t ? d.inverse() : d;
}
/*!
 * Flip 3.12.2
 * https://greensock.com
 *
 * @license Copyright 2008-2023, GreenSock. All rights reserved.
 * Subject to the terms at https://greensock.com/standard-license or for
 * Club GreenSock members, the agreement issued with that membership.
 * @author: Jack Doyle, jack@greensock.com
*/
var Xa = 1, Se, rt, B, Le, Nt, Bt, Ji, Wr = function(t, e) {
  return t.actions.forEach(function(i) {
    return i.vars[e] && i.vars[e](i);
  });
}, tr = {}, Hr = 180 / Math.PI, Ya = Math.PI / 180, li = {}, Zr = {}, di = {}, Pr = function(t) {
  return typeof t == "string" ? t.split(" ").join("").split(",") : t;
}, Ua = Pr("onStart,onUpdate,onComplete,onReverseComplete,onInterrupt"), pi = Pr("transform,transformOrigin,width,height,position,top,left,opacity,zIndex,maxWidth,maxHeight,minWidth,minHeight"), Be = function(t) {
  return Se(t)[0] || console.warn("Element not found:", t);
}, _e = function(t) {
  return Math.round(t * 1e4) / 1e4 || 0;
}, Di = function(t, e, i) {
  return t.forEach(function(r) {
    return r.classList[i](e);
  });
}, jr = {
  zIndex: 1,
  kill: 1,
  simple: 1,
  spin: 1,
  clearProps: 1,
  targets: 1,
  toggleClass: 1,
  onComplete: 1,
  onUpdate: 1,
  onInterrupt: 1,
  onStart: 1,
  delay: 1,
  repeat: 1,
  repeatDelay: 1,
  yoyo: 1,
  scale: 1,
  fade: 1,
  absolute: 1,
  props: 1,
  onEnter: 1,
  onLeave: 1,
  custom: 1,
  paused: 1,
  nested: 1,
  prune: 1,
  absoluteOnLeave: 1
}, as = {
  zIndex: 1,
  simple: 1,
  clearProps: 1,
  scale: 1,
  absolute: 1,
  fitChild: 1,
  getVars: 1,
  props: 1
}, os = function(t) {
  return t.replace(/([A-Z])/g, "-$1").toLowerCase();
}, de = function(t, e) {
  var i = {}, r;
  for (r in t)
    e[r] || (i[r] = t[r]);
  return i;
}, kr = {}, us = function(t) {
  var e = kr[t] = Pr(t);
  return di[t] = e.concat(pi), e;
}, qa = function(t) {
  var e = t._gsap || rt.core.getCache(t);
  return e.gmCache === rt.ticker.frame ? e.gMatrix : (e.gmCache = rt.ticker.frame, e.gMatrix = Et(t, !0, !1, !0));
}, Ga = function l(t, e, i) {
  i === void 0 && (i = 0);
  for (var r = t.parentNode, n = 1e3 * Math.pow(10, i) * (e ? -1 : 1), s = e ? -n * 900 : 0; t; )
    s += n, t = t.previousSibling;
  return r ? s + l(r, e, i + 1) : s;
}, fi = function(t, e, i) {
  return t.forEach(function(r) {
    return r.d = Ga(i ? r.element : r.t, e);
  }), t.sort(function(r, n) {
    return r.d - n.d;
  }), t;
}, Ge = function(t, e) {
  for (var i = t.element.style, r = t.css = t.css || [], n = e.length, s, a; n--; )
    s = e[n], a = i[s] || i.getPropertyValue(s), r.push(a ? s : Zr[s] || (Zr[s] = os(s)), a);
  return i;
}, Sr = function(t) {
  var e = t.css, i = t.element.style, r = 0;
  for (t.cache.uncache = 1; r < e.length; r += 2)
    e[r + 1] ? i[e[r]] = e[r + 1] : i.removeProperty(e[r]);
  !e[e.indexOf("transform") + 1] && i.translate && (i.removeProperty("translate"), i.removeProperty("scale"), i.removeProperty("rotate"));
}, Kr = function(t, e) {
  t.forEach(function(i) {
    return i.a.cache.uncache = 1;
  }), e || t.finalStates.forEach(Sr);
}, Ai = "paddingTop,paddingRight,paddingBottom,paddingLeft,gridArea,transition".split(","), Cr = function(t, e, i) {
  var r = t.element, n = t.width, s = t.height, a = t.uncache, u = t.getProp, o = r.style, f = 4, h, _, d;
  if (typeof e != "object" && (e = t), B && i !== 1)
    return B._abs.push({
      t: r,
      b: t,
      a: t,
      sd: 0
    }), B._final.push(function() {
      return (t.cache.uncache = 1) && Sr(t);
    }), r;
  for (_ = u("display") === "none", (!t.isVisible || _) && (_ && (Ge(t, ["display"]).display = e.display), t.matrix = e.matrix, t.width = n = t.width || e.width, t.height = s = t.height || e.height), Ge(t, Ai), d = window.getComputedStyle(r); f--; )
    o[Ai[f]] = d[Ai[f]];
  if (o.gridArea = "1 / 1 / 1 / 1", o.transition = "none", o.position = "absolute", o.width = n + "px", o.height = s + "px", o.top || (o.top = "0px"), o.left || (o.left = "0px"), a)
    h = new oe(r);
  else if (h = de(t, li), h.position = "absolute", t.simple) {
    var p = r.getBoundingClientRect();
    h.matrix = new ae(1, 0, 0, 1, p.left + wr(), p.top + br());
  } else
    h.matrix = Et(r, !1, !1, !0);
  return h = xe(h, t, !0), t.x = Bt(h.x, 0.01), t.y = Bt(h.y, 0.01), r;
}, Qr = function(t, e) {
  return e !== !0 && (e = Se(e), t = t.filter(function(i) {
    if (e.indexOf((i.sd < 0 ? i.b : i.a).element) !== -1)
      return !0;
    i.t._gsap.renderTransform(1), i.b.isVisible && (i.t.style.width = i.b.width + "px", i.t.style.height = i.b.height + "px");
  })), t;
}, ls = function(t) {
  return fi(t, !0).forEach(function(e) {
    return (e.a.isVisible || e.b.isVisible) && Cr(e.sd < 0 ? e.b : e.a, e.b, 1);
  });
}, $a = function(t, e) {
  return e && t.idLookup[er(e).id] || t.elementStates[0];
}, er = function(t, e, i, r) {
  return t instanceof oe ? t : t instanceof Tt ? $a(t, r) : new oe(typeof t == "string" ? Be(t) || console.warn(t + " not found") : t, e, i);
}, Wa = function(t, e) {
  for (var i = rt.getProperty(t.element, null, "native"), r = t.props = {}, n = e.length; n--; )
    r[e[n]] = (i(e[n]) + "").trim();
  return r.zIndex && (r.zIndex = parseFloat(r.zIndex) || 0), t;
}, fs = function(t, e) {
  var i = t.style || t, r;
  for (r in e)
    i[r] = e[r];
}, Ha = function(t) {
  var e = t.getAttribute("data-flip-id");
  return e || t.setAttribute("data-flip-id", e = "auto-" + Xa++), e;
}, hs = function(t) {
  return t.map(function(e) {
    return e.element;
  });
}, Jr = function(t, e, i) {
  return t && e.length && i.add(t(hs(e), i, new Tt(e, 0, !0)), 0);
}, xe = function(t, e, i, r, n, s) {
  var a = t.element, u = t.cache, o = t.parent, f = t.x, h = t.y, _ = e.width, d = e.height, p = e.scaleX, c = e.scaleY, m = e.rotation, g = e.bounds, v = s && Ji && Ji(a, "transform"), y = t, b = e.matrix, x = b.e, P = b.f, k = t.bounds.width !== g.width || t.bounds.height !== g.height || t.scaleX !== p || t.scaleY !== c || t.rotation !== m, T = !k && t.simple && e.simple && !n, w, S, O, A, R, E, C;
  return T || !o ? (p = c = 1, m = w = 0) : (R = qa(o), E = R.clone().multiply(e.ctm ? e.matrix.clone().multiply(e.ctm) : e.matrix), m = _e(Math.atan2(E.b, E.a) * Hr), w = _e(Math.atan2(E.c, E.d) * Hr + m) % 360, p = Math.sqrt(Math.pow(E.a, 2) + Math.pow(E.b, 2)), c = Math.sqrt(Math.pow(E.c, 2) + Math.pow(E.d, 2)) * Math.cos(w * Ya), n && (n = Se(n)[0], A = rt.getProperty(n), C = n.getBBox && typeof n.getBBox == "function" && n.getBBox(), y = {
    scaleX: A("scaleX"),
    scaleY: A("scaleY"),
    width: C ? C.width : Math.ceil(parseFloat(A("width", "px"))),
    height: C ? C.height : parseFloat(A("height", "px"))
  }), u.rotation = m + "deg", u.skewX = w + "deg"), i ? (p *= _ === y.width || !y.width ? 1 : _ / y.width, c *= d === y.height || !y.height ? 1 : d / y.height, u.scaleX = p, u.scaleY = c) : (_ = Bt(_ * p / y.scaleX, 0), d = Bt(d * c / y.scaleY, 0), a.style.width = _ + "px", a.style.height = d + "px"), r && fs(a, e.props), T || !o ? (f += x - t.matrix.e, h += P - t.matrix.f) : k || o !== e.parent ? (u.renderTransform(1, u), E = Et(n || a, !1, !1, !0), S = R.apply({
    x: E.e,
    y: E.f
  }), O = R.apply({
    x,
    y: P
  }), f += O.x - S.x, h += O.y - S.y) : (R.e = R.f = 0, O = R.apply({
    x: x - t.matrix.e,
    y: P - t.matrix.f
  }), f += O.x, h += O.y), f = Bt(f, 0.02), h = Bt(h, 0.02), s && !(s instanceof oe) ? v && v.revert() : (u.x = f + "px", u.y = h + "px", u.renderTransform(1, u)), s && (s.x = f, s.y = h, s.rotation = m, s.skewX = w, i ? (s.scaleX = p, s.scaleY = c) : (s.width = _, s.height = d)), s || u;
}, Ri = function(t, e) {
  return t instanceof Tt ? t : new Tt(t, e);
}, cs = function(t, e, i) {
  var r = t.idLookup[i], n = t.alt[i];
  return n.isVisible && (!(e.getElementState(n.element) || n).isVisible || !r.isVisible) ? n : r;
}, Fi = [], Ii = "width,height,overflowX,overflowY".split(","), He, tn = function(t) {
  if (t !== He) {
    var e = Nt.style, i = Nt.clientWidth === window.outerWidth, r = Nt.clientHeight === window.outerHeight, n = 4;
    if (t && (i || r)) {
      for (; n--; )
        Fi[n] = e[Ii[n]];
      i && (e.width = Nt.clientWidth + "px", e.overflowY = "hidden"), r && (e.height = Nt.clientHeight + "px", e.overflowX = "hidden"), He = t;
    } else if (He) {
      for (; n--; )
        Fi[n] ? e[Ii[n]] = Fi[n] : e.removeProperty(os(Ii[n]));
      He = t;
    }
  }
}, Li = function(t, e, i, r) {
  t instanceof Tt && e instanceof Tt || console.warn("Not a valid state object."), i = i || {};
  var n = i, s = n.clearProps, a = n.onEnter, u = n.onLeave, o = n.absolute, f = n.absoluteOnLeave, h = n.custom, _ = n.delay, d = n.paused, p = n.repeat, c = n.repeatDelay, m = n.yoyo, g = n.toggleClass, v = n.nested, y = n.zIndex, b = n.scale, x = n.fade, P = n.stagger, k = n.spin, T = n.prune, w = ("props" in i ? i : t).props, S = de(i, jr), O = rt.timeline({
    delay: _,
    paused: d,
    repeat: p,
    repeatDelay: c,
    yoyo: m,
    data: "isFlip"
  }), A = S, R = [], E = [], C = [], z = [], X = k === !0 ? 1 : k || 0, K = typeof k == "function" ? k : function() {
    return X;
  }, bt = t.interrupted || e.interrupted, Pt = O[r !== 1 ? "to" : "from"], _t, G, Ce, Z, F, Y, le, kt, mi, Dt, At, gi, W, it;
  for (G in e.idLookup)
    At = e.alt[G] ? cs(e, t, G) : e.idLookup[G], F = At.element, Dt = t.idLookup[G], t.alt[G] && F === Dt.element && (t.alt[G].isVisible || !At.isVisible) && (Dt = t.alt[G]), Dt ? (Y = {
      t: F,
      b: Dt,
      a: At,
      sd: Dt.element === F ? 0 : At.isVisible ? 1 : -1
    }, C.push(Y), Y.sd && (Y.sd < 0 && (Y.b = At, Y.a = Dt), bt && Ge(Y.b, w ? di[w] : pi), x && C.push(Y.swap = {
      t: Dt.element,
      b: Y.b,
      a: Y.a,
      sd: -Y.sd,
      swap: Y
    })), F._flip = Dt.element._flip = B ? B.timeline : O) : At.isVisible && (C.push({
      t: F,
      b: de(At, {
        isVisible: 1
      }),
      a: At,
      sd: 0,
      entering: 1
    }), F._flip = B ? B.timeline : O);
  if (w && (kr[w] || us(w)).forEach(function(Rt) {
    return S[Rt] = function(Zt) {
      return C[Zt].a.props[Rt];
    };
  }), C.finalStates = mi = [], gi = function() {
    for (fi(C), tn(!0), Z = 0; Z < C.length; Z++)
      Y = C[Z], W = Y.a, it = Y.b, T && !W.isDifferent(it) && !Y.entering ? C.splice(Z--, 1) : (F = Y.t, v && !(Y.sd < 0) && Z && (W.matrix = Et(F, !1, !1, !0)), it.isVisible && W.isVisible ? (Y.sd < 0 ? (le = new oe(F, w, t.simple), xe(le, W, b, 0, 0, le), le.matrix = Et(F, !1, !1, !0), le.css = Y.b.css, Y.a = W = le, x && (F.style.opacity = bt ? it.opacity : W.opacity), P && z.push(F)) : Y.sd > 0 && x && (F.style.opacity = bt ? W.opacity - it.opacity : "0"), xe(W, it, b, w)) : it.isVisible !== W.isVisible && (it.isVisible ? W.isVisible || (it.css = W.css, E.push(it), C.splice(Z--, 1), o && v && xe(W, it, b, w)) : (W.isVisible && R.push(W), C.splice(Z--, 1))), b || (F.style.maxWidth = Math.max(W.width, it.width) + "px", F.style.maxHeight = Math.max(W.height, it.height) + "px", F.style.minWidth = Math.min(W.width, it.width) + "px", F.style.minHeight = Math.min(W.height, it.height) + "px"), v && g && F.classList.add(g)), mi.push(W);
    var Zt;
    if (g && (Zt = mi.map(function(M) {
      return M.element;
    }), v && Zt.forEach(function(M) {
      return M.classList.remove(g);
    })), tn(!1), b ? (S.scaleX = function(M) {
      return C[M].a.scaleX;
    }, S.scaleY = function(M) {
      return C[M].a.scaleY;
    }) : (S.width = function(M) {
      return C[M].a.width + "px";
    }, S.height = function(M) {
      return C[M].a.height + "px";
    }, S.autoRound = i.autoRound || !1), S.x = function(M) {
      return C[M].a.x + "px";
    }, S.y = function(M) {
      return C[M].a.y + "px";
    }, S.rotation = function(M) {
      return C[M].a.rotation + (k ? K(M, kt[M], kt) * 360 : 0);
    }, S.skewX = function(M) {
      return C[M].a.skewX;
    }, kt = C.map(function(M) {
      return M.t;
    }), (y || y === 0) && (S.modifiers = {
      zIndex: function() {
        return y;
      }
    }, S.zIndex = y, S.immediateRender = i.immediateRender !== !1), x && (S.opacity = function(M) {
      return C[M].sd < 0 ? 0 : C[M].sd > 0 ? C[M].a.opacity : "+=0";
    }), z.length) {
      P = rt.utils.distribute(P);
      var _s = kt.slice(z.length);
      S.stagger = function(M, Er) {
        return P(~z.indexOf(Er) ? kt.indexOf(C[M].swap.t) : M, Er, _s);
      };
    }
    if (Ua.forEach(function(M) {
      return i[M] && O.eventCallback(M, i[M], i[M + "Params"]);
    }), h && kt.length) {
      A = de(S, jr), "scale" in h && (h.scaleX = h.scaleY = h.scale, delete h.scale);
      for (G in h)
        _t = de(h[G], as), _t[G] = S[G], !("duration" in _t) && "duration" in S && (_t.duration = S.duration), _t.stagger = S.stagger, Pt.call(O, kt, _t, 0), delete A[G];
    }
    (kt.length || E.length || R.length) && (g && O.add(function() {
      return Di(Zt, g, O._zTime < 0 ? "remove" : "add");
    }, 0) && !d && Di(Zt, g, "add"), kt.length && Pt.call(O, kt, A, 0)), Jr(a, R, O), Jr(u, E, O);
    var xi = B && B.timeline;
    xi && (xi.add(O, 0), B._final.push(function() {
      return Kr(C, !s);
    })), Ce = O.duration(), O.call(function() {
      var M = O.time() >= Ce;
      M && !xi && Kr(C, !s), g && Di(Zt, g, M ? "remove" : "add");
    });
  }, f && (o = C.filter(function(Rt) {
    return !Rt.sd && !Rt.a.isVisible && Rt.b.isVisible;
  }).map(function(Rt) {
    return Rt.a.element;
  })), B) {
    var Mr;
    o && (Mr = B._abs).push.apply(Mr, Qr(C, o)), B._run.push(gi);
  } else
    o && ls(Qr(C, o)), gi();
  var yi = B ? B.timeline : O;
  return yi.revert = function() {
    return Or(yi, 1, 1);
  }, yi;
}, Za = function l(t) {
  t.vars.onInterrupt && t.vars.onInterrupt.apply(t, t.vars.onInterruptParams || []), t.getChildren(!0, !1, !0).forEach(l);
}, Or = function(t, e, i) {
  if (t && t.progress() < 1 && (!t.paused() || i))
    return e && (Za(t), e < 2 && t.progress(1), t.kill()), !0;
}, Ze = function(t) {
  for (var e = t.idLookup = {}, i = t.alt = {}, r = t.elementStates, n = r.length, s; n--; )
    s = r[n], e[s.id] ? i[s.id] = s : e[s.id] = s;
}, Tt = /* @__PURE__ */ function() {
  function l(e, i, r) {
    if (this.props = i && i.props, this.simple = !!(i && i.simple), r)
      this.targets = hs(e), this.elementStates = e, Ze(this);
    else {
      this.targets = Se(e);
      var n = i && (i.kill === !1 || i.batch && !i.kill);
      B && !n && B._kill.push(this), this.update(n || !!B);
    }
  }
  var t = l.prototype;
  return t.update = function(i) {
    var r = this;
    return this.elementStates = this.targets.map(function(n) {
      return new oe(n, r.props, r.simple);
    }), Ze(this), this.interrupt(i), this.recordInlineStyles(), this;
  }, t.clear = function() {
    return this.targets.length = this.elementStates.length = 0, Ze(this), this;
  }, t.fit = function(i, r, n) {
    for (var s = fi(this.elementStates.slice(0), !1, !0), a = (i || this).idLookup, u = 0, o, f; u < s.length; u++)
      o = s[u], n && (o.matrix = Et(o.element, !1, !1, !0)), f = a[o.id], f && xe(o, f, r, !0, 0, o), o.matrix = Et(o.element, !1, !1, !0);
    return this;
  }, t.getProperty = function(i, r) {
    var n = this.getElementState(i) || li;
    return (r in n ? n : n.props || li)[r];
  }, t.add = function(i) {
    for (var r = i.targets.length, n = this.idLookup, s = this.alt, a, u, o; r--; )
      u = i.elementStates[r], o = n[u.id], o && (u.element === o.element || s[u.id] && s[u.id].element === u.element) ? (a = this.elementStates.indexOf(u.element === o.element ? o : s[u.id]), this.targets.splice(a, 1, i.targets[r]), this.elementStates.splice(a, 1, u)) : (this.targets.push(i.targets[r]), this.elementStates.push(u));
    return i.interrupted && (this.interrupted = !0), i.simple || (this.simple = !1), Ze(this), this;
  }, t.compare = function(i) {
    var r = i.idLookup, n = this.idLookup, s = [], a = [], u = [], o = [], f = [], h = i.alt, _ = this.alt, d = function(T, w, S) {
      return (T.isVisible !== w.isVisible ? T.isVisible ? u : o : T.isVisible ? a : s).push(S) && f.push(S);
    }, p = function(T, w, S) {
      return f.indexOf(S) < 0 && d(T, w, S);
    }, c, m, g, v, y, b, x, P;
    for (g in r)
      y = h[g], b = _[g], c = y ? cs(i, this, g) : r[g], v = c.element, m = n[g], b ? (P = m.isVisible || !b.isVisible && v === m.element ? m : b, x = y && !c.isVisible && !y.isVisible && P.element === y.element ? y : c, x.isVisible && P.isVisible && x.element !== P.element ? ((x.isDifferent(P) ? a : s).push(x.element, P.element), f.push(x.element, P.element)) : d(x, P, x.element), y && x.element === y.element && (y = r[g]), p(x.element !== m.element && y ? y : x, m, m.element), p(y && y.element === b.element ? y : x, b, b.element), y && p(y, b.element === y.element ? b : m, y.element)) : (m ? m.isDifferent(c) ? d(c, m, v) : s.push(v) : u.push(v), y && p(y, m, y.element));
    for (g in n)
      r[g] || (o.push(n[g].element), _[g] && o.push(_[g].element));
    return {
      changed: a,
      unchanged: s,
      enter: u,
      leave: o
    };
  }, t.recordInlineStyles = function() {
    for (var i = di[this.props] || pi, r = this.elementStates.length; r--; )
      Ge(this.elementStates[r], i);
  }, t.interrupt = function(i) {
    var r = this, n = [];
    this.targets.forEach(function(s) {
      var a = s._flip, u = Or(a, i ? 0 : 1);
      i && u && n.indexOf(a) < 0 && a.add(function() {
        return r.updateVisibility();
      }), u && n.push(a);
    }), !i && n.length && this.updateVisibility(), this.interrupted || (this.interrupted = !!n.length);
  }, t.updateVisibility = function() {
    this.elementStates.forEach(function(i) {
      var r = i.element.getBoundingClientRect();
      i.isVisible = !!(r.width || r.height || r.top || r.left), i.uncache = 1;
    });
  }, t.getElementState = function(i) {
    return this.elementStates[this.targets.indexOf(Be(i))];
  }, t.makeAbsolute = function() {
    return fi(this.elementStates.slice(0), !0, !0).map(Cr);
  }, l;
}(), oe = /* @__PURE__ */ function() {
  function l(e, i, r) {
    this.element = e, this.update(i, r);
  }
  var t = l.prototype;
  return t.isDifferent = function(i) {
    var r = this.bounds, n = i.bounds;
    return r.top !== n.top || r.left !== n.left || r.width !== n.width || r.height !== n.height || !this.matrix.equals(i.matrix) || this.opacity !== i.opacity || this.props && i.props && JSON.stringify(this.props) !== JSON.stringify(i.props);
  }, t.update = function(i, r) {
    var n = this, s = n.element, a = rt.getProperty(s), u = rt.core.getCache(s), o = s.getBoundingClientRect(), f = s.getBBox && typeof s.getBBox == "function" && s.nodeName.toLowerCase() !== "svg" && s.getBBox(), h = r ? new ae(1, 0, 0, 1, o.left + wr(), o.top + br()) : Et(s, !1, !1, !0);
    n.getProp = a, n.element = s, n.id = Ha(s), n.matrix = h, n.cache = u, n.bounds = o, n.isVisible = !!(o.width || o.height || o.left || o.top), n.display = a("display"), n.position = a("position"), n.parent = s.parentNode, n.x = a("x"), n.y = a("y"), n.scaleX = u.scaleX, n.scaleY = u.scaleY, n.rotation = a("rotation"), n.skewX = a("skewX"), n.opacity = a("opacity"), n.width = f ? f.width : Bt(a("width", "px"), 0.04), n.height = f ? f.height : Bt(a("height", "px"), 0.04), i && Wa(n, kr[i] || us(i)), n.ctm = s.getCTM && s.nodeName.toLowerCase() === "svg" && ss(s).inverse(), n.simple = r || _e(h.a) === 1 && !_e(h.b) && !_e(h.c) && _e(h.d) === 1, n.uncache = 0;
  }, l;
}(), ja = /* @__PURE__ */ function() {
  function l(e, i) {
    this.vars = e, this.batch = i, this.states = [], this.timeline = i.timeline;
  }
  var t = l.prototype;
  return t.getStateById = function(i) {
    for (var r = this.states.length; r--; )
      if (this.states[r].idLookup[i])
        return this.states[r];
  }, t.kill = function() {
    this.batch.remove(this);
  }, l;
}(), Ka = /* @__PURE__ */ function() {
  function l(e) {
    this.id = e, this.actions = [], this._kill = [], this._final = [], this._abs = [], this._run = [], this.data = {}, this.state = new Tt(), this.timeline = rt.timeline();
  }
  var t = l.prototype;
  return t.add = function(i) {
    var r = this.actions.filter(function(n) {
      return n.vars === i;
    });
    return r.length ? r[0] : (r = new ja(typeof i == "function" ? {
      animate: i
    } : i, this), this.actions.push(r), r);
  }, t.remove = function(i) {
    var r = this.actions.indexOf(i);
    return r >= 0 && this.actions.splice(r, 1), this;
  }, t.getState = function(i) {
    var r = this, n = B, s = Le;
    return B = this, this.state.clear(), this._kill.length = 0, this.actions.forEach(function(a) {
      a.vars.getState && (a.states.length = 0, Le = a, a.state = a.vars.getState(a)), i && a.states.forEach(function(u) {
        return r.state.add(u);
      });
    }), Le = s, B = n, this.killConflicts(), this;
  }, t.animate = function() {
    var i = this, r = B, n = this.timeline, s = this.actions.length, a, u;
    for (B = this, n.clear(), this._abs.length = this._final.length = this._run.length = 0, this.actions.forEach(function(o) {
      o.vars.animate && o.vars.animate(o);
      var f = o.vars.onEnter, h = o.vars.onLeave, _ = o.targets, d, p;
      _ && _.length && (f || h) && (d = new Tt(), o.states.forEach(function(c) {
        return d.add(c);
      }), p = d.compare(ve.getState(_)), p.enter.length && f && f(p.enter), p.leave.length && h && h(p.leave));
    }), ls(this._abs), this._run.forEach(function(o) {
      return o();
    }), u = n.duration(), a = this._final.slice(0), n.add(function() {
      u <= n.time() && (a.forEach(function(o) {
        return o();
      }), Wr(i, "onComplete"));
    }), B = r; s--; )
      this.actions[s].vars.once && this.actions[s].kill();
    return Wr(this, "onStart"), n.restart(), this;
  }, t.loadState = function(i) {
    i || (i = function() {
      return 0;
    });
    var r = [];
    return this.actions.forEach(function(n) {
      if (n.vars.loadState) {
        var s, a = function u(o) {
          o && (n.targets = o), s = r.indexOf(u), ~s && (r.splice(s, 1), r.length || i());
        };
        r.push(a), n.vars.loadState(a);
      }
    }), r.length || i(), this;
  }, t.setState = function() {
    return this.actions.forEach(function(i) {
      return i.targets = i.vars.setState && i.vars.setState(i);
    }), this;
  }, t.killConflicts = function(i) {
    return this.state.interrupt(i), this._kill.forEach(function(r) {
      return r.interrupt(i);
    }), this;
  }, t.run = function(i, r) {
    var n = this;
    return this !== B && (i || this.getState(r), this.loadState(function() {
      n._killed || (n.setState(), n.animate());
    })), this;
  }, t.clear = function(i) {
    this.state.clear(), i || (this.actions.length = 0);
  }, t.getStateById = function(i) {
    for (var r = this.actions.length, n; r--; )
      if (n = this.actions[r].getStateById(i), n)
        return n;
    return this.state.idLookup[i] && this.state;
  }, t.kill = function() {
    this._killed = 1, this.clear(), delete tr[this.id];
  }, l;
}(), ve = /* @__PURE__ */ function() {
  function l() {
  }
  return l.getState = function(e, i) {
    var r = Ri(e, i);
    return Le && Le.states.push(r), i && i.batch && l.batch(i.batch).state.add(r), r;
  }, l.from = function(e, i) {
    return i = i || {}, "clearProps" in i || (i.clearProps = !0), Li(e, Ri(i.targets || e.targets, {
      props: i.props || e.props,
      simple: i.simple,
      kill: !!i.kill
    }), i, -1);
  }, l.to = function(e, i) {
    return Li(e, Ri(i.targets || e.targets, {
      props: i.props || e.props,
      simple: i.simple,
      kill: !!i.kill
    }), i, 1);
  }, l.fromTo = function(e, i, r) {
    return Li(e, i, r);
  }, l.fit = function(e, i, r) {
    var n = r ? de(r, as) : {}, s = r || n, a = s.absolute, u = s.scale, o = s.getVars, f = s.props, h = s.runBackwards, _ = s.onComplete, d = s.simple, p = r && r.fitChild && Be(r.fitChild), c = er(i, f, d, e), m = er(e, 0, d, c), g = f ? di[f] : pi;
    return f && fs(n, c.props), h && (Ge(m, g), "immediateRender" in n || (n.immediateRender = !0), n.onComplete = function() {
      Sr(m), _ && _.apply(this, arguments);
    }), a && Cr(m, c), n = xe(m, c, u || p, f, p, n.duration || o ? n : 0), o ? n : n.duration ? rt.to(m.element, n) : null;
  }, l.makeAbsolute = function(e, i) {
    return (e instanceof Tt ? e : new Tt(e, i)).makeAbsolute();
  }, l.batch = function(e) {
    return e || (e = "default"), tr[e] || (tr[e] = new Ka(e));
  }, l.killFlipsOf = function(e, i) {
    (e instanceof Tt ? e.targets : Se(e)).forEach(function(r) {
      return r && Or(r._flip, i !== !1 ? 1 : 2);
    });
  }, l.isFlipping = function(e) {
    var i = l.getByTarget(e);
    return !!i && i.isActive();
  }, l.getByTarget = function(e) {
    return (Be(e) || li)._flip;
  }, l.getElementState = function(e, i) {
    return new oe(Be(e), i);
  }, l.convertCoordinates = function(e, i, r) {
    var n = Et(i, !0, !0).multiply(Et(e));
    return r ? n.apply(r) : n;
  }, l.register = function(e) {
    if (Nt = typeof document < "u" && document.body, Nt) {
      rt = e, vr(Nt), Se = rt.utils.toArray, Ji = rt.core.getStyleSaver;
      var i = rt.utils.snap(0.1);
      Bt = function(n, s) {
        return i(parseFloat(n) + s);
      };
    }
  }, l;
}();
ve.version = "3.12.2";
typeof window < "u" && window.gsap && window.gsap.registerPlugin(ve);
const Ja = /* @__PURE__ */ ds({
  __name: "AnimateGrider",
  props: {
    columnsTemplate: { default: "repeat(10,1fr)" },
    rowsTemplate: { default: "repeat(10,1fr)" }
  },
  emits: ["onAnimationFinish"],
  setup(l, { expose: t, emit: e }) {
    const i = l;
    es.registerPlugin(ve);
    const r = ps(() => ({
      "grid-template-columns": i.columnsTemplate,
      "grid-template-rows": i.rowsTemplate
    })), n = ms(null);
    function s(a, u, o, f, h) {
      if (n.value === null)
        return;
      let _ = null;
      const d = `c${a}`;
      if (u === "Input") {
        const p = n.value.querySelector(`[list="${d}-datalist"]`);
        _ = p == null ? void 0 : p.closest(`[for="${p.id}"]`);
      } else
        _ = n.value.querySelector(`#${d}`);
      if (_) {
        const p = ve.getState(_, { props: "opacity" });
        _.style.gridArea = o, _.style.opacity = f.toString(), ws(() => {
          ve.from(p, {
            duration: h.duration,
            ease: h.ease,
            // fade: true,
            // absolute: true,
            onComplete: (c) => {
              e("onAnimationFinish", {
                id: a,
                style: `grid-area:${o};opacity:${f}`,
                resultProps: {
                  opacity: f
                }
              });
            }
          });
        });
      }
    }
    return t({
      changePosition: s
    }), (a, u) => (gs(), ys("div", {
      class: "grid w-full",
      ref_key: "boxRef",
      ref: n,
      style: xs(vs(r))
    }, [
      bs(a.$slots, "default")
    ], 4));
  }
});
export {
  Ja as default
};