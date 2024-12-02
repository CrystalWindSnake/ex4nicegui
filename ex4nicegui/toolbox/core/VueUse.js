var ne = Object.defineProperty;
var re = (t, e, r) => e in t ? ne(t, e, { enumerable: !0, configurable: !0, writable: !0, value: r }) : t[e] = r;
var bt = (t, e, r) => (re(t, typeof e != "symbol" ? e + "" : e, r), r);
const oe = Vue.isRef;
const L = Vue.ref;
const ie = Vue.getCurrentScope;
const se = Vue.onScopeDispose;
const ue = Vue.unref;
const Tt = Vue.toRef;
const ht = Vue.readonly;
const It = Vue.customRef;
const Rt = Vue.onMounted;
const gt = Vue.nextTick;
const Pt = Vue.getCurrentInstance;
const k = Vue.watch;
const D = Vue.computed;
const ae = Vue.watchEffect;
const ce = Vue.shallowRef;
const le = Vue.defineComponent;

function Lt(t) {
  return ie() ? (se(t), !0) : !1;
}
function U(t) {
  return typeof t == "function" ? t() : ue(t);
}
const fe = typeof window < "u" && typeof document < "u";
typeof WorkerGlobalScope < "u" && globalThis instanceof WorkerGlobalScope;
const de = Object.prototype.toString, he = (t) => de.call(t) === "[object Object]", _t = () => {
};
function ge(t, e) {
  function r(...o) {
    return new Promise((n, i) => {
      Promise.resolve(t(() => e.apply(this, o), { fn: e, thisArg: this, args: o })).then(n).catch(i);
    });
  }
  return r;
}
const Dt = (t) => t();
function me(t = Dt) {
  const e = L(!0);
  function r() {
    e.value = !1;
  }
  function o() {
    e.value = !0;
  }
  const n = (...i) => {
    e.value && t(...i);
  };
  return { isActive: ht(e), pause: r, resume: o, eventFilter: n };
}
function we(t, e) {
  var r;
  if (typeof t == "number")
    return t + e;
  const o = ((r = t.match(/^-?\d+\.?\d*/)) == null ? void 0 : r[0]) || "", n = t.slice(o.length), i = Number.parseFloat(o) + e;
  return Number.isNaN(i) ? t : i + n;
}
function pe(t) {
  return t || Pt();
}
function ye(...t) {
  if (t.length !== 1)
    return Tt(...t);
  const e = t[0];
  return typeof e == "function" ? ht(It(() => ({ get: e, set: _t }))) : L(e);
}
function Ce(t, e, r = {}) {
  const {
    eventFilter: o = Dt,
    ...n
  } = r;
  return k(
    t,
    ge(
      o,
      e
    ),
    n
  );
}
function Ee(t, e, r = {}) {
  const {
    eventFilter: o,
    ...n
  } = r, { eventFilter: i, pause: s, resume: u, isActive: a } = me(o);
  return { stop: Ce(
    t,
    e,
    {
      ...n,
      eventFilter: i
    }
  ), pause: s, resume: u, isActive: a };
}
function kt(t, e = !0, r) {
  pe() ? Rt(t, r) : e ? t() : gt(t);
}
function be(t = !1, e = {}) {
  const {
    truthyValue: r = !0,
    falsyValue: o = !1
  } = e, n = oe(t), i = L(t);
  function s(u) {
    if (arguments.length)
      return i.value = u, i.value;
    {
      const a = U(r);
      return i.value = i.value === a ? U(o) : a, i.value;
    }
  }
  return n ? s : [i, s];
}
function Ut(t) {
  var e;
  const r = U(t);
  return (e = r == null ? void 0 : r.$el) != null ? e : r;
}
const O = fe ? window : void 0;
function Bt(...t) {
  let e, r, o, n;
  if (typeof t[0] == "string" || Array.isArray(t[0]) ? ([r, o, n] = t, e = O) : [e, r, o, n] = t, !e)
    return _t;
  Array.isArray(r) || (r = [r]), Array.isArray(o) || (o = [o]);
  const i = [], s = () => {
    i.forEach((c) => c()), i.length = 0;
  }, u = (c, h, g, d) => (c.addEventListener(h, g, d), () => c.removeEventListener(h, g, d)), a = k(
    () => [Ut(e), U(n)],
    ([c, h]) => {
      if (s(), !c)
        return;
      const g = he(h) ? { ...h } : h;
      i.push(
        ...r.flatMap((d) => o.map((w) => u(c, d, w, g)))
      );
    },
    { immediate: !0, flush: "post" }
  ), l = () => {
    a(), s();
  };
  return Lt(l), l;
}
function Be() {
  const t = L(!1), e = Pt();
  return e && Rt(() => {
    t.value = !0;
  }, e), t;
}
function Se(t) {
  const e = Be();
  return D(() => (e.value, !!t()));
}
function z(t, e = {}) {
  const { window: r = O } = e, o = Se(() => r && "matchMedia" in r && typeof r.matchMedia == "function");
  let n;
  const i = L(!1), s = (l) => {
    i.value = l.matches;
  }, u = () => {
    n && ("removeEventListener" in n ? n.removeEventListener("change", s) : n.removeListener(s));
  }, a = ae(() => {
    o.value && (u(), n = r.matchMedia(U(t)), "addEventListener" in n ? n.addEventListener("change", s) : n.addListener(s), i.value = n.matches);
  });
  return Lt(() => {
    a(), u(), n = void 0;
  }), i;
}
function Ae(t, e = {}) {
  function r(c, h) {
    let g = U(t[U(c)]);
    return h != null && (g = we(g, h)), typeof g == "number" && (g = `${g}px`), g;
  }
  const { window: o = O, strategy: n = "min-width" } = e;
  function i(c) {
    return o ? o.matchMedia(c).matches : !1;
  }
  const s = (c) => z(() => `(min-width: ${r(c)})`, e), u = (c) => z(() => `(max-width: ${r(c)})`, e), a = Object.keys(t).reduce((c, h) => (Object.defineProperty(c, h, {
    get: () => n === "min-width" ? s(h) : u(h),
    enumerable: !0,
    configurable: !0
  }), c), {});
  function l() {
    const c = Object.keys(t).map((h) => [h, s(h)]);
    return D(() => c.filter(([, h]) => h.value).map(([h]) => h));
  }
  return Object.assign(a, {
    greaterOrEqual: s,
    smallerOrEqual: u,
    greater(c) {
      return z(() => `(min-width: ${r(c, 0.1)})`, e);
    },
    smaller(c) {
      return z(() => `(max-width: ${r(c, -0.1)})`, e);
    },
    between(c, h) {
      return z(() => `(min-width: ${r(c)}) and (max-width: ${r(h, -0.1)})`, e);
    },
    isGreater(c) {
      return i(`(min-width: ${r(c, 0.1)})`);
    },
    isGreaterOrEqual(c) {
      return i(`(min-width: ${r(c)})`);
    },
    isSmaller(c) {
      return i(`(max-width: ${r(c, -0.1)})`);
    },
    isSmallerOrEqual(c) {
      return i(`(max-width: ${r(c)})`);
    },
    isInBetween(c, h) {
      return i(`(min-width: ${r(c)}) and (max-width: ${r(h, -0.1)})`);
    },
    current: l,
    active() {
      const c = l();
      return D(() => c.value.length === 0 ? "" : c.value.at(-1));
    }
  });
}
const W = typeof globalThis < "u" ? globalThis : typeof window < "u" ? window : typeof global < "u" ? global : typeof self < "u" ? self : {}, q = "__vueuse_ssr_handlers__", Me = /* @__PURE__ */ ve();
function ve() {
  return q in W || (W[q] = W[q] || {}), W[q];
}
function Ft(t, e) {
  return Me[t] || e;
}
function Ne(t) {
  return t == null ? "any" : t instanceof Set ? "set" : t instanceof Map ? "map" : t instanceof Date ? "date" : typeof t == "boolean" ? "boolean" : typeof t == "string" ? "string" : typeof t == "object" ? "object" : Number.isNaN(t) ? "any" : "number";
}
const Te = {
  boolean: {
    read: (t) => t === "true",
    write: (t) => String(t)
  },
  object: {
    read: (t) => JSON.parse(t),
    write: (t) => JSON.stringify(t)
  },
  number: {
    read: (t) => Number.parseFloat(t),
    write: (t) => String(t)
  },
  any: {
    read: (t) => t,
    write: (t) => String(t)
  },
  string: {
    read: (t) => t,
    write: (t) => String(t)
  },
  map: {
    read: (t) => new Map(JSON.parse(t)),
    write: (t) => JSON.stringify(Array.from(t.entries()))
  },
  set: {
    read: (t) => new Set(JSON.parse(t)),
    write: (t) => JSON.stringify(Array.from(t))
  },
  date: {
    read: (t) => new Date(t),
    write: (t) => t.toISOString()
  }
}, St = "vueuse-storage";
function Ie(t, e, r, o = {}) {
  var n;
  const {
    flush: i = "pre",
    deep: s = !0,
    listenToStorageChanges: u = !0,
    writeDefaults: a = !0,
    mergeDefaults: l = !1,
    shallow: c,
    window: h = O,
    eventFilter: g,
    onError: d = (C) => {
      console.error(C);
    },
    initOnMounted: w
  } = o, p = (c ? ce : L)(typeof e == "function" ? e() : e);
  if (!r)
    try {
      r = Ft("getDefaultStorage", () => {
        var C;
        return (C = O) == null ? void 0 : C.localStorage;
      })();
    } catch (C) {
      d(C);
    }
  if (!r)
    return p;
  const B = U(e), y = Ne(B), E = (n = o.serializer) != null ? n : Te[y], { pause: m, resume: f } = Ee(
    p,
    () => S(p.value),
    { flush: i, deep: s, eventFilter: g }
  );
  h && u && kt(() => {
    Bt(h, "storage", M), Bt(h, St, N), w && M();
  }), w || M();
  function b(C, v) {
    h && h.dispatchEvent(new CustomEvent(St, {
      detail: {
        key: t,
        oldValue: C,
        newValue: v,
        storageArea: r
      }
    }));
  }
  function S(C) {
    try {
      const v = r.getItem(t);
      if (C == null)
        b(v, null), r.removeItem(t);
      else {
        const I = E.write(C);
        v !== I && (r.setItem(t, I), b(v, I));
      }
    } catch (v) {
      d(v);
    }
  }
  function A(C) {
    const v = C ? C.newValue : r.getItem(t);
    if (v == null)
      return a && B != null && r.setItem(t, E.write(B)), B;
    if (!C && l) {
      const I = E.read(v);
      return typeof l == "function" ? l(I, B) : y === "object" && !Array.isArray(I) ? { ...B, ...I } : I;
    } else
      return typeof v != "string" ? v : E.read(v);
  }
  function M(C) {
    if (!(C && C.storageArea !== r)) {
      if (C && C.key == null) {
        p.value = B;
        return;
      }
      if (!(C && C.key !== t)) {
        m();
        try {
          (C == null ? void 0 : C.newValue) !== E.write(p.value) && (p.value = A(C));
        } catch (v) {
          d(v);
        } finally {
          C ? gt(f) : f();
        }
      }
    }
  }
  function N(C) {
    M(C.detail);
  }
  return p;
}
function Ot(t) {
  return z("(prefers-color-scheme: dark)", t);
}
function Re(t = {}) {
  const {
    selector: e = "html",
    attribute: r = "class",
    initialValue: o = "auto",
    window: n = O,
    storage: i,
    storageKey: s = "vueuse-color-scheme",
    listenToStorageChanges: u = !0,
    storageRef: a,
    emitAuto: l,
    disableTransition: c = !0
  } = t, h = {
    auto: "",
    light: "light",
    dark: "dark",
    ...t.modes || {}
  }, g = Ot({ window: n }), d = D(() => g.value ? "dark" : "light"), w = a || (s == null ? ye(o) : Ie(s, o, i, { window: n, listenToStorageChanges: u })), p = D(() => w.value === "auto" ? d.value : w.value), B = Ft(
    "updateHTMLAttrs",
    (f, b, S) => {
      const A = typeof f == "string" ? n == null ? void 0 : n.document.querySelector(f) : Ut(f);
      if (!A)
        return;
      let M;
      if (c) {
        M = n.document.createElement("style");
        const N = "*,*::before,*::after{-webkit-transition:none!important;-moz-transition:none!important;-o-transition:none!important;-ms-transition:none!important;transition:none!important}";
        M.appendChild(document.createTextNode(N)), n.document.head.appendChild(M);
      }
      if (b === "class") {
        const N = S.split(/\s/g);
        Object.values(h).flatMap((C) => (C || "").split(/\s/g)).filter(Boolean).forEach((C) => {
          N.includes(C) ? A.classList.add(C) : A.classList.remove(C);
        });
      } else
        A.setAttribute(b, S);
      c && (n.getComputedStyle(M).opacity, document.head.removeChild(M));
    }
  );
  function y(f) {
    var b;
    B(e, r, (b = h[f]) != null ? b : f);
  }
  function E(f) {
    t.onChanged ? t.onChanged(f, y) : y(f);
  }
  k(p, E, { flush: "post", immediate: !0 }), kt(() => E(p.value));
  const m = D({
    get() {
      return l ? w.value : p.value;
    },
    set(f) {
      w.value = f;
    }
  });
  try {
    return Object.assign(m, { store: w, system: d, state: p });
  } catch {
    return m;
  }
}
function Pe(t = {}) {
  const {
    valueDark: e = "dark",
    valueLight: r = "",
    window: o = O
  } = t, n = Re({
    ...t,
    onChanged: (u, a) => {
      var l;
      t.onChanged ? (l = t.onChanged) == null || l.call(t, u === "dark", a, u) : a(u);
    },
    modes: {
      dark: e,
      light: r
    }
  }), i = D(() => n.system ? n.system.value : Ot({ window: o }).value ? "dark" : "light");
  return D({
    get() {
      return n.value === "dark";
    },
    set(u) {
      const a = u ? "dark" : "light";
      i.value === a ? n.value = "auto" : n.value = a;
    }
  });
}
function zt(t) {
  gt(() => {
    window.socket.on("connect", t);
  });
}
function Le(t, e) {
  const r = Ae(t), o = r.active(), n = () => {
    e("change", {
      eventName: "activeWithMounted",
      value: o.value
    });
  }, i = new Et();
  return i.addMethod("active", () => o.value), i.addMethod(
    "between",
    (s, u) => r.between(s, u).value
  ), i.addMethod(
    "betweenReactively",
    (s, u, a) => {
      const l = r.between(s, u);
      k(l, (c) => {
        e("change", {
          eventName: a,
          value: c
        });
      });
    }
  ), zt(n), k(o, (s) => {
    e("change", {
      eventName: "active",
      value: s
    }), n();
  }), i;
}
function _e(t, e, r) {
  const o = Pe(t);
  o.value = e;
  const n = be(o), i = new Et();
  return i.addMethod("toggleDark", (s) => {
    if (o.value !== s) {
      if (s === null) {
        n();
        return;
      }
      n(s);
    }
  }), k(o, (s) => {
    r("change", {
      eventName: "isDark",
      value: s
    });
  }), i;
}
const De = typeof window < "u" && typeof document < "u";
typeof WorkerGlobalScope < "u" && globalThis instanceof WorkerGlobalScope;
const ke = () => {
};
function Ue(...t) {
  if (t.length !== 1)
    return Tt(...t);
  const e = t[0];
  return typeof e == "function" ? ht(It(() => ({ get: e, set: ke }))) : L(e);
}
var Y = {}, Fe = function() {
  return typeof Promise == "function" && Promise.prototype && Promise.prototype.then;
}, Vt = {}, T = {};
let mt;
const Oe = [
  0,
  // Not used
  26,
  44,
  70,
  100,
  134,
  172,
  196,
  242,
  292,
  346,
  404,
  466,
  532,
  581,
  655,
  733,
  815,
  901,
  991,
  1085,
  1156,
  1258,
  1364,
  1474,
  1588,
  1706,
  1828,
  1921,
  2051,
  2185,
  2323,
  2465,
  2611,
  2761,
  2876,
  3034,
  3196,
  3362,
  3532,
  3706
];
T.getSymbolSize = function(e) {
  if (!e)
    throw new Error('"version" cannot be null or undefined');
  if (e < 1 || e > 40)
    throw new Error('"version" should be in range from 1 to 40');
  return e * 4 + 17;
};
T.getSymbolTotalCodewords = function(e) {
  return Oe[e];
};
T.getBCHDigit = function(t) {
  let e = 0;
  for (; t !== 0; )
    e++, t >>>= 1;
  return e;
};
T.setToSJISFunction = function(e) {
  if (typeof e != "function")
    throw new Error('"toSJISFunc" is not a valid function.');
  mt = e;
};
T.isKanjiModeEnabled = function() {
  return typeof mt < "u";
};
T.toSJIS = function(e) {
  return mt(e);
};
var tt = {};
(function(t) {
  t.L = { bit: 1 }, t.M = { bit: 0 }, t.Q = { bit: 3 }, t.H = { bit: 2 };
  function e(r) {
    if (typeof r != "string")
      throw new Error("Param is not a string");
    switch (r.toLowerCase()) {
      case "l":
      case "low":
        return t.L;
      case "m":
      case "medium":
        return t.M;
      case "q":
      case "quartile":
        return t.Q;
      case "h":
      case "high":
        return t.H;
      default:
        throw new Error("Unknown EC Level: " + r);
    }
  }
  t.isValid = function(o) {
    return o && typeof o.bit < "u" && o.bit >= 0 && o.bit < 4;
  }, t.from = function(o, n) {
    if (t.isValid(o))
      return o;
    try {
      return e(o);
    } catch {
      return n;
    }
  };
})(tt);
function $t() {
  this.buffer = [], this.length = 0;
}
$t.prototype = {
  get: function(t) {
    const e = Math.floor(t / 8);
    return (this.buffer[e] >>> 7 - t % 8 & 1) === 1;
  },
  put: function(t, e) {
    for (let r = 0; r < e; r++)
      this.putBit((t >>> e - r - 1 & 1) === 1);
  },
  getLengthInBits: function() {
    return this.length;
  },
  putBit: function(t) {
    const e = Math.floor(this.length / 8);
    this.buffer.length <= e && this.buffer.push(0), t && (this.buffer[e] |= 128 >>> this.length % 8), this.length++;
  }
};
var ze = $t;
function G(t) {
  if (!t || t < 1)
    throw new Error("BitMatrix size must be defined and greater than 0");
  this.size = t, this.data = new Uint8Array(t * t), this.reservedBit = new Uint8Array(t * t);
}
G.prototype.set = function(t, e, r, o) {
  const n = t * this.size + e;
  this.data[n] = r, o && (this.reservedBit[n] = !0);
};
G.prototype.get = function(t, e) {
  return this.data[t * this.size + e];
};
G.prototype.xor = function(t, e, r) {
  this.data[t * this.size + e] ^= r;
};
G.prototype.isReserved = function(t, e) {
  return this.reservedBit[t * this.size + e];
};
var Ve = G, jt = {};
(function(t) {
  const e = T.getSymbolSize;
  t.getRowColCoords = function(o) {
    if (o === 1)
      return [];
    const n = Math.floor(o / 7) + 2, i = e(o), s = i === 145 ? 26 : Math.ceil((i - 13) / (2 * n - 2)) * 2, u = [i - 7];
    for (let a = 1; a < n - 1; a++)
      u[a] = u[a - 1] - s;
    return u.push(6), u.reverse();
  }, t.getPositions = function(o) {
    const n = [], i = t.getRowColCoords(o), s = i.length;
    for (let u = 0; u < s; u++)
      for (let a = 0; a < s; a++)
        u === 0 && a === 0 || // top-left
        u === 0 && a === s - 1 || // bottom-left
        u === s - 1 && a === 0 || n.push([i[u], i[a]]);
    return n;
  };
})(jt);
var Ht = {};
const $e = T.getSymbolSize, At = 7;
Ht.getPositions = function(e) {
  const r = $e(e);
  return [
    // top-left
    [0, 0],
    // top-right
    [r - At, 0],
    // bottom-left
    [0, r - At]
  ];
};
var Jt = {};
(function(t) {
  t.Patterns = {
    PATTERN000: 0,
    PATTERN001: 1,
    PATTERN010: 2,
    PATTERN011: 3,
    PATTERN100: 4,
    PATTERN101: 5,
    PATTERN110: 6,
    PATTERN111: 7
  };
  const e = {
    N1: 3,
    N2: 3,
    N3: 40,
    N4: 10
  };
  t.isValid = function(n) {
    return n != null && n !== "" && !isNaN(n) && n >= 0 && n <= 7;
  }, t.from = function(n) {
    return t.isValid(n) ? parseInt(n, 10) : void 0;
  }, t.getPenaltyN1 = function(n) {
    const i = n.size;
    let s = 0, u = 0, a = 0, l = null, c = null;
    for (let h = 0; h < i; h++) {
      u = a = 0, l = c = null;
      for (let g = 0; g < i; g++) {
        let d = n.get(h, g);
        d === l ? u++ : (u >= 5 && (s += e.N1 + (u - 5)), l = d, u = 1), d = n.get(g, h), d === c ? a++ : (a >= 5 && (s += e.N1 + (a - 5)), c = d, a = 1);
      }
      u >= 5 && (s += e.N1 + (u - 5)), a >= 5 && (s += e.N1 + (a - 5));
    }
    return s;
  }, t.getPenaltyN2 = function(n) {
    const i = n.size;
    let s = 0;
    for (let u = 0; u < i - 1; u++)
      for (let a = 0; a < i - 1; a++) {
        const l = n.get(u, a) + n.get(u, a + 1) + n.get(u + 1, a) + n.get(u + 1, a + 1);
        (l === 4 || l === 0) && s++;
      }
    return s * e.N2;
  }, t.getPenaltyN3 = function(n) {
    const i = n.size;
    let s = 0, u = 0, a = 0;
    for (let l = 0; l < i; l++) {
      u = a = 0;
      for (let c = 0; c < i; c++)
        u = u << 1 & 2047 | n.get(l, c), c >= 10 && (u === 1488 || u === 93) && s++, a = a << 1 & 2047 | n.get(c, l), c >= 10 && (a === 1488 || a === 93) && s++;
    }
    return s * e.N3;
  }, t.getPenaltyN4 = function(n) {
    let i = 0;
    const s = n.data.length;
    for (let a = 0; a < s; a++)
      i += n.data[a];
    return Math.abs(Math.ceil(i * 100 / s / 5) - 10) * e.N4;
  };
  function r(o, n, i) {
    switch (o) {
      case t.Patterns.PATTERN000:
        return (n + i) % 2 === 0;
      case t.Patterns.PATTERN001:
        return n % 2 === 0;
      case t.Patterns.PATTERN010:
        return i % 3 === 0;
      case t.Patterns.PATTERN011:
        return (n + i) % 3 === 0;
      case t.Patterns.PATTERN100:
        return (Math.floor(n / 2) + Math.floor(i / 3)) % 2 === 0;
      case t.Patterns.PATTERN101:
        return n * i % 2 + n * i % 3 === 0;
      case t.Patterns.PATTERN110:
        return (n * i % 2 + n * i % 3) % 2 === 0;
      case t.Patterns.PATTERN111:
        return (n * i % 3 + (n + i) % 2) % 2 === 0;
      default:
        throw new Error("bad maskPattern:" + o);
    }
  }
  t.applyMask = function(n, i) {
    const s = i.size;
    for (let u = 0; u < s; u++)
      for (let a = 0; a < s; a++)
        i.isReserved(a, u) || i.xor(a, u, r(n, a, u));
  }, t.getBestMask = function(n, i) {
    const s = Object.keys(t.Patterns).length;
    let u = 0, a = 1 / 0;
    for (let l = 0; l < s; l++) {
      i(l), t.applyMask(l, n);
      const c = t.getPenaltyN1(n) + t.getPenaltyN2(n) + t.getPenaltyN3(n) + t.getPenaltyN4(n);
      t.applyMask(l, n), c < a && (a = c, u = l);
    }
    return u;
  };
})(Jt);
var et = {};
const _ = tt, Q = [
  // L  M  Q  H
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  2,
  2,
  1,
  2,
  2,
  4,
  1,
  2,
  4,
  4,
  2,
  4,
  4,
  4,
  2,
  4,
  6,
  5,
  2,
  4,
  6,
  6,
  2,
  5,
  8,
  8,
  4,
  5,
  8,
  8,
  4,
  5,
  8,
  11,
  4,
  8,
  10,
  11,
  4,
  9,
  12,
  16,
  4,
  9,
  16,
  16,
  6,
  10,
  12,
  18,
  6,
  10,
  17,
  16,
  6,
  11,
  16,
  19,
  6,
  13,
  18,
  21,
  7,
  14,
  21,
  25,
  8,
  16,
  20,
  25,
  8,
  17,
  23,
  25,
  9,
  17,
  23,
  34,
  9,
  18,
  25,
  30,
  10,
  20,
  27,
  32,
  12,
  21,
  29,
  35,
  12,
  23,
  34,
  37,
  12,
  25,
  34,
  40,
  13,
  26,
  35,
  42,
  14,
  28,
  38,
  45,
  15,
  29,
  40,
  48,
  16,
  31,
  43,
  51,
  17,
  33,
  45,
  54,
  18,
  35,
  48,
  57,
  19,
  37,
  51,
  60,
  19,
  38,
  53,
  63,
  20,
  40,
  56,
  66,
  21,
  43,
  59,
  70,
  22,
  45,
  62,
  74,
  24,
  47,
  65,
  77,
  25,
  49,
  68,
  81
], Z = [
  // L  M  Q  H
  7,
  10,
  13,
  17,
  10,
  16,
  22,
  28,
  15,
  26,
  36,
  44,
  20,
  36,
  52,
  64,
  26,
  48,
  72,
  88,
  36,
  64,
  96,
  112,
  40,
  72,
  108,
  130,
  48,
  88,
  132,
  156,
  60,
  110,
  160,
  192,
  72,
  130,
  192,
  224,
  80,
  150,
  224,
  264,
  96,
  176,
  260,
  308,
  104,
  198,
  288,
  352,
  120,
  216,
  320,
  384,
  132,
  240,
  360,
  432,
  144,
  280,
  408,
  480,
  168,
  308,
  448,
  532,
  180,
  338,
  504,
  588,
  196,
  364,
  546,
  650,
  224,
  416,
  600,
  700,
  224,
  442,
  644,
  750,
  252,
  476,
  690,
  816,
  270,
  504,
  750,
  900,
  300,
  560,
  810,
  960,
  312,
  588,
  870,
  1050,
  336,
  644,
  952,
  1110,
  360,
  700,
  1020,
  1200,
  390,
  728,
  1050,
  1260,
  420,
  784,
  1140,
  1350,
  450,
  812,
  1200,
  1440,
  480,
  868,
  1290,
  1530,
  510,
  924,
  1350,
  1620,
  540,
  980,
  1440,
  1710,
  570,
  1036,
  1530,
  1800,
  570,
  1064,
  1590,
  1890,
  600,
  1120,
  1680,
  1980,
  630,
  1204,
  1770,
  2100,
  660,
  1260,
  1860,
  2220,
  720,
  1316,
  1950,
  2310,
  750,
  1372,
  2040,
  2430
];
et.getBlocksCount = function(e, r) {
  switch (r) {
    case _.L:
      return Q[(e - 1) * 4 + 0];
    case _.M:
      return Q[(e - 1) * 4 + 1];
    case _.Q:
      return Q[(e - 1) * 4 + 2];
    case _.H:
      return Q[(e - 1) * 4 + 3];
    default:
      return;
  }
};
et.getTotalCodewordsCount = function(e, r) {
  switch (r) {
    case _.L:
      return Z[(e - 1) * 4 + 0];
    case _.M:
      return Z[(e - 1) * 4 + 1];
    case _.Q:
      return Z[(e - 1) * 4 + 2];
    case _.H:
      return Z[(e - 1) * 4 + 3];
    default:
      return;
  }
};
var Kt = {}, nt = {};
const J = new Uint8Array(512), X = new Uint8Array(256);
(function() {
  let e = 1;
  for (let r = 0; r < 255; r++)
    J[r] = e, X[e] = r, e <<= 1, e & 256 && (e ^= 285);
  for (let r = 255; r < 512; r++)
    J[r] = J[r - 255];
})();
nt.log = function(e) {
  if (e < 1)
    throw new Error("log(" + e + ")");
  return X[e];
};
nt.exp = function(e) {
  return J[e];
};
nt.mul = function(e, r) {
  return e === 0 || r === 0 ? 0 : J[X[e] + X[r]];
};
(function(t) {
  const e = nt;
  t.mul = function(o, n) {
    const i = new Uint8Array(o.length + n.length - 1);
    for (let s = 0; s < o.length; s++)
      for (let u = 0; u < n.length; u++)
        i[s + u] ^= e.mul(o[s], n[u]);
    return i;
  }, t.mod = function(o, n) {
    let i = new Uint8Array(o);
    for (; i.length - n.length >= 0; ) {
      const s = i[0];
      for (let a = 0; a < n.length; a++)
        i[a] ^= e.mul(n[a], s);
      let u = 0;
      for (; u < i.length && i[u] === 0; )
        u++;
      i = i.slice(u);
    }
    return i;
  }, t.generateECPolynomial = function(o) {
    let n = new Uint8Array([1]);
    for (let i = 0; i < o; i++)
      n = t.mul(n, new Uint8Array([1, e.exp(i)]));
    return n;
  };
})(Kt);
const Yt = Kt;
function wt(t) {
  this.genPoly = void 0, this.degree = t, this.degree && this.initialize(this.degree);
}
wt.prototype.initialize = function(e) {
  this.degree = e, this.genPoly = Yt.generateECPolynomial(this.degree);
};
wt.prototype.encode = function(e) {
  if (!this.genPoly)
    throw new Error("Encoder not initialized");
  const r = new Uint8Array(e.length + this.degree);
  r.set(e);
  const o = Yt.mod(r, this.genPoly), n = this.degree - o.length;
  if (n > 0) {
    const i = new Uint8Array(this.degree);
    return i.set(o, n), i;
  }
  return o;
};
var je = wt, Gt = {}, F = {}, pt = {};
pt.isValid = function(e) {
  return !isNaN(e) && e >= 1 && e <= 40;
};
var R = {};
const Wt = "[0-9]+", He = "[A-Z $%*+\\-./:]+";
let K = "(?:[u3000-u303F]|[u3040-u309F]|[u30A0-u30FF]|[uFF00-uFFEF]|[u4E00-u9FAF]|[u2605-u2606]|[u2190-u2195]|u203B|[u2010u2015u2018u2019u2025u2026u201Cu201Du2225u2260]|[u0391-u0451]|[u00A7u00A8u00B1u00B4u00D7u00F7])+";
K = K.replace(/u/g, "\\u");
const Je = "(?:(?![A-Z0-9 $%*+\\-./:]|" + K + `)(?:.|[\r
]))+`;
R.KANJI = new RegExp(K, "g");
R.BYTE_KANJI = new RegExp("[^A-Z0-9 $%*+\\-./:]+", "g");
R.BYTE = new RegExp(Je, "g");
R.NUMERIC = new RegExp(Wt, "g");
R.ALPHANUMERIC = new RegExp(He, "g");
const Ke = new RegExp("^" + K + "$"), Ye = new RegExp("^" + Wt + "$"), Ge = new RegExp("^[A-Z0-9 $%*+\\-./:]+$");
R.testKanji = function(e) {
  return Ke.test(e);
};
R.testNumeric = function(e) {
  return Ye.test(e);
};
R.testAlphanumeric = function(e) {
  return Ge.test(e);
};
(function(t) {
  const e = pt, r = R;
  t.NUMERIC = {
    id: "Numeric",
    bit: 1,
    ccBits: [10, 12, 14]
  }, t.ALPHANUMERIC = {
    id: "Alphanumeric",
    bit: 2,
    ccBits: [9, 11, 13]
  }, t.BYTE = {
    id: "Byte",
    bit: 4,
    ccBits: [8, 16, 16]
  }, t.KANJI = {
    id: "Kanji",
    bit: 8,
    ccBits: [8, 10, 12]
  }, t.MIXED = {
    bit: -1
  }, t.getCharCountIndicator = function(i, s) {
    if (!i.ccBits)
      throw new Error("Invalid mode: " + i);
    if (!e.isValid(s))
      throw new Error("Invalid version: " + s);
    return s >= 1 && s < 10 ? i.ccBits[0] : s < 27 ? i.ccBits[1] : i.ccBits[2];
  }, t.getBestModeForData = function(i) {
    return r.testNumeric(i) ? t.NUMERIC : r.testAlphanumeric(i) ? t.ALPHANUMERIC : r.testKanji(i) ? t.KANJI : t.BYTE;
  }, t.toString = function(i) {
    if (i && i.id)
      return i.id;
    throw new Error("Invalid mode");
  }, t.isValid = function(i) {
    return i && i.bit && i.ccBits;
  };
  function o(n) {
    if (typeof n != "string")
      throw new Error("Param is not a string");
    switch (n.toLowerCase()) {
      case "numeric":
        return t.NUMERIC;
      case "alphanumeric":
        return t.ALPHANUMERIC;
      case "kanji":
        return t.KANJI;
      case "byte":
        return t.BYTE;
      default:
        throw new Error("Unknown mode: " + n);
    }
  }
  t.from = function(i, s) {
    if (t.isValid(i))
      return i;
    try {
      return o(i);
    } catch {
      return s;
    }
  };
})(F);
(function(t) {
  const e = T, r = et, o = tt, n = F, i = pt, s = 7973, u = e.getBCHDigit(s);
  function a(g, d, w) {
    for (let p = 1; p <= 40; p++)
      if (d <= t.getCapacity(p, w, g))
        return p;
  }
  function l(g, d) {
    return n.getCharCountIndicator(g, d) + 4;
  }
  function c(g, d) {
    let w = 0;
    return g.forEach(function(p) {
      const B = l(p.mode, d);
      w += B + p.getBitsLength();
    }), w;
  }
  function h(g, d) {
    for (let w = 1; w <= 40; w++)
      if (c(g, w) <= t.getCapacity(w, d, n.MIXED))
        return w;
  }
  t.from = function(d, w) {
    return i.isValid(d) ? parseInt(d, 10) : w;
  }, t.getCapacity = function(d, w, p) {
    if (!i.isValid(d))
      throw new Error("Invalid QR Code version");
    typeof p > "u" && (p = n.BYTE);
    const B = e.getSymbolTotalCodewords(d), y = r.getTotalCodewordsCount(d, w), E = (B - y) * 8;
    if (p === n.MIXED)
      return E;
    const m = E - l(p, d);
    switch (p) {
      case n.NUMERIC:
        return Math.floor(m / 10 * 3);
      case n.ALPHANUMERIC:
        return Math.floor(m / 11 * 2);
      case n.KANJI:
        return Math.floor(m / 13);
      case n.BYTE:
      default:
        return Math.floor(m / 8);
    }
  }, t.getBestVersionForData = function(d, w) {
    let p;
    const B = o.from(w, o.M);
    if (Array.isArray(d)) {
      if (d.length > 1)
        return h(d, B);
      if (d.length === 0)
        return 1;
      p = d[0];
    } else
      p = d;
    return a(p.mode, p.getLength(), B);
  }, t.getEncodedBits = function(d) {
    if (!i.isValid(d) || d < 7)
      throw new Error("Invalid QR Code version");
    let w = d << 12;
    for (; e.getBCHDigit(w) - u >= 0; )
      w ^= s << e.getBCHDigit(w) - u;
    return d << 12 | w;
  };
})(Gt);
var qt = {};
const ct = T, Qt = 1335, We = 21522, Mt = ct.getBCHDigit(Qt);
qt.getEncodedBits = function(e, r) {
  const o = e.bit << 3 | r;
  let n = o << 10;
  for (; ct.getBCHDigit(n) - Mt >= 0; )
    n ^= Qt << ct.getBCHDigit(n) - Mt;
  return (o << 10 | n) ^ We;
};
var Zt = {};
const qe = F;
function V(t) {
  this.mode = qe.NUMERIC, this.data = t.toString();
}
V.getBitsLength = function(e) {
  return 10 * Math.floor(e / 3) + (e % 3 ? e % 3 * 3 + 1 : 0);
};
V.prototype.getLength = function() {
  return this.data.length;
};
V.prototype.getBitsLength = function() {
  return V.getBitsLength(this.data.length);
};
V.prototype.write = function(e) {
  let r, o, n;
  for (r = 0; r + 3 <= this.data.length; r += 3)
    o = this.data.substr(r, 3), n = parseInt(o, 10), e.put(n, 10);
  const i = this.data.length - r;
  i > 0 && (o = this.data.substr(r), n = parseInt(o, 10), e.put(n, i * 3 + 1));
};
var Qe = V;
const Ze = F, ot = [
  "0",
  "1",
  "2",
  "3",
  "4",
  "5",
  "6",
  "7",
  "8",
  "9",
  "A",
  "B",
  "C",
  "D",
  "E",
  "F",
  "G",
  "H",
  "I",
  "J",
  "K",
  "L",
  "M",
  "N",
  "O",
  "P",
  "Q",
  "R",
  "S",
  "T",
  "U",
  "V",
  "W",
  "X",
  "Y",
  "Z",
  " ",
  "$",
  "%",
  "*",
  "+",
  "-",
  ".",
  "/",
  ":"
];
function $(t) {
  this.mode = Ze.ALPHANUMERIC, this.data = t;
}
$.getBitsLength = function(e) {
  return 11 * Math.floor(e / 2) + 6 * (e % 2);
};
$.prototype.getLength = function() {
  return this.data.length;
};
$.prototype.getBitsLength = function() {
  return $.getBitsLength(this.data.length);
};
$.prototype.write = function(e) {
  let r;
  for (r = 0; r + 2 <= this.data.length; r += 2) {
    let o = ot.indexOf(this.data[r]) * 45;
    o += ot.indexOf(this.data[r + 1]), e.put(o, 11);
  }
  this.data.length % 2 && e.put(ot.indexOf(this.data[r]), 6);
};
var Xe = $;
const xe = F;
function j(t) {
  this.mode = xe.BYTE, typeof t == "string" ? this.data = new TextEncoder().encode(t) : this.data = new Uint8Array(t);
}
j.getBitsLength = function(e) {
  return e * 8;
};
j.prototype.getLength = function() {
  return this.data.length;
};
j.prototype.getBitsLength = function() {
  return j.getBitsLength(this.data.length);
};
j.prototype.write = function(t) {
  for (let e = 0, r = this.data.length; e < r; e++)
    t.put(this.data[e], 8);
};
var tn = j;
const en = F, nn = T;
function H(t) {
  this.mode = en.KANJI, this.data = t;
}
H.getBitsLength = function(e) {
  return e * 13;
};
H.prototype.getLength = function() {
  return this.data.length;
};
H.prototype.getBitsLength = function() {
  return H.getBitsLength(this.data.length);
};
H.prototype.write = function(t) {
  let e;
  for (e = 0; e < this.data.length; e++) {
    let r = nn.toSJIS(this.data[e]);
    if (r >= 33088 && r <= 40956)
      r -= 33088;
    else if (r >= 57408 && r <= 60351)
      r -= 49472;
    else
      throw new Error(
        "Invalid SJIS character: " + this.data[e] + `
Make sure your charset is UTF-8`
      );
    r = (r >>> 8 & 255) * 192 + (r & 255), t.put(r, 13);
  }
};
var rn = H, Xt = { exports: {} };
(function(t) {
  var e = {
    single_source_shortest_paths: function(r, o, n) {
      var i = {}, s = {};
      s[o] = 0;
      var u = e.PriorityQueue.make();
      u.push(o, 0);
      for (var a, l, c, h, g, d, w, p, B; !u.empty(); ) {
        a = u.pop(), l = a.value, h = a.cost, g = r[l] || {};
        for (c in g)
          g.hasOwnProperty(c) && (d = g[c], w = h + d, p = s[c], B = typeof s[c] > "u", (B || p > w) && (s[c] = w, u.push(c, w), i[c] = l));
      }
      if (typeof n < "u" && typeof s[n] > "u") {
        var y = ["Could not find a path from ", o, " to ", n, "."].join("");
        throw new Error(y);
      }
      return i;
    },
    extract_shortest_path_from_predecessor_list: function(r, o) {
      for (var n = [], i = o; i; )
        n.push(i), r[i], i = r[i];
      return n.reverse(), n;
    },
    find_path: function(r, o, n) {
      var i = e.single_source_shortest_paths(r, o, n);
      return e.extract_shortest_path_from_predecessor_list(
        i,
        n
      );
    },
    /**
     * A very naive priority queue implementation.
     */
    PriorityQueue: {
      make: function(r) {
        var o = e.PriorityQueue, n = {}, i;
        r = r || {};
        for (i in o)
          o.hasOwnProperty(i) && (n[i] = o[i]);
        return n.queue = [], n.sorter = r.sorter || o.default_sorter, n;
      },
      default_sorter: function(r, o) {
        return r.cost - o.cost;
      },
      /**
       * Add a new item to the queue and ensure the highest priority element
       * is at the front of the queue.
       */
      push: function(r, o) {
        var n = { value: r, cost: o };
        this.queue.push(n), this.queue.sort(this.sorter);
      },
      /**
       * Return the highest priority element in the queue.
       */
      pop: function() {
        return this.queue.shift();
      },
      empty: function() {
        return this.queue.length === 0;
      }
    }
  };
  t.exports = e;
})(Xt);
var on = Xt.exports;
(function(t) {
  const e = F, r = Qe, o = Xe, n = tn, i = rn, s = R, u = T, a = on;
  function l(y) {
    return unescape(encodeURIComponent(y)).length;
  }
  function c(y, E, m) {
    const f = [];
    let b;
    for (; (b = y.exec(m)) !== null; )
      f.push({
        data: b[0],
        index: b.index,
        mode: E,
        length: b[0].length
      });
    return f;
  }
  function h(y) {
    const E = c(s.NUMERIC, e.NUMERIC, y), m = c(s.ALPHANUMERIC, e.ALPHANUMERIC, y);
    let f, b;
    return u.isKanjiModeEnabled() ? (f = c(s.BYTE, e.BYTE, y), b = c(s.KANJI, e.KANJI, y)) : (f = c(s.BYTE_KANJI, e.BYTE, y), b = []), E.concat(m, f, b).sort(function(A, M) {
      return A.index - M.index;
    }).map(function(A) {
      return {
        data: A.data,
        mode: A.mode,
        length: A.length
      };
    });
  }
  function g(y, E) {
    switch (E) {
      case e.NUMERIC:
        return r.getBitsLength(y);
      case e.ALPHANUMERIC:
        return o.getBitsLength(y);
      case e.KANJI:
        return i.getBitsLength(y);
      case e.BYTE:
        return n.getBitsLength(y);
    }
  }
  function d(y) {
    return y.reduce(function(E, m) {
      const f = E.length - 1 >= 0 ? E[E.length - 1] : null;
      return f && f.mode === m.mode ? (E[E.length - 1].data += m.data, E) : (E.push(m), E);
    }, []);
  }
  function w(y) {
    const E = [];
    for (let m = 0; m < y.length; m++) {
      const f = y[m];
      switch (f.mode) {
        case e.NUMERIC:
          E.push([
            f,
            { data: f.data, mode: e.ALPHANUMERIC, length: f.length },
            { data: f.data, mode: e.BYTE, length: f.length }
          ]);
          break;
        case e.ALPHANUMERIC:
          E.push([
            f,
            { data: f.data, mode: e.BYTE, length: f.length }
          ]);
          break;
        case e.KANJI:
          E.push([
            f,
            { data: f.data, mode: e.BYTE, length: l(f.data) }
          ]);
          break;
        case e.BYTE:
          E.push([
            { data: f.data, mode: e.BYTE, length: l(f.data) }
          ]);
      }
    }
    return E;
  }
  function p(y, E) {
    const m = {}, f = { start: {} };
    let b = ["start"];
    for (let S = 0; S < y.length; S++) {
      const A = y[S], M = [];
      for (let N = 0; N < A.length; N++) {
        const C = A[N], v = "" + S + N;
        M.push(v), m[v] = { node: C, lastCount: 0 }, f[v] = {};
        for (let I = 0; I < b.length; I++) {
          const P = b[I];
          m[P] && m[P].node.mode === C.mode ? (f[P][v] = g(m[P].lastCount + C.length, C.mode) - g(m[P].lastCount, C.mode), m[P].lastCount += C.length) : (m[P] && (m[P].lastCount = C.length), f[P][v] = g(C.length, C.mode) + 4 + e.getCharCountIndicator(C.mode, E));
        }
      }
      b = M;
    }
    for (let S = 0; S < b.length; S++)
      f[b[S]].end = 0;
    return { map: f, table: m };
  }
  function B(y, E) {
    let m;
    const f = e.getBestModeForData(y);
    if (m = e.from(E, f), m !== e.BYTE && m.bit < f.bit)
      throw new Error('"' + y + '" cannot be encoded with mode ' + e.toString(m) + `.
 Suggested mode is: ` + e.toString(f));
    switch (m === e.KANJI && !u.isKanjiModeEnabled() && (m = e.BYTE), m) {
      case e.NUMERIC:
        return new r(y);
      case e.ALPHANUMERIC:
        return new o(y);
      case e.KANJI:
        return new i(y);
      case e.BYTE:
        return new n(y);
    }
  }
  t.fromArray = function(E) {
    return E.reduce(function(m, f) {
      return typeof f == "string" ? m.push(B(f, null)) : f.data && m.push(B(f.data, f.mode)), m;
    }, []);
  }, t.fromString = function(E, m) {
    const f = h(E, u.isKanjiModeEnabled()), b = w(f), S = p(b, m), A = a.find_path(S.map, "start", "end"), M = [];
    for (let N = 1; N < A.length - 1; N++)
      M.push(S.table[A[N]].node);
    return t.fromArray(d(M));
  }, t.rawSplit = function(E) {
    return t.fromArray(
      h(E, u.isKanjiModeEnabled())
    );
  };
})(Zt);
const rt = T, it = tt, sn = ze, un = Ve, an = jt, cn = Ht, lt = Jt, ft = et, ln = je, x = Gt, fn = qt, dn = F, st = Zt;
function hn(t, e) {
  const r = t.size, o = cn.getPositions(e);
  for (let n = 0; n < o.length; n++) {
    const i = o[n][0], s = o[n][1];
    for (let u = -1; u <= 7; u++)
      if (!(i + u <= -1 || r <= i + u))
        for (let a = -1; a <= 7; a++)
          s + a <= -1 || r <= s + a || (u >= 0 && u <= 6 && (a === 0 || a === 6) || a >= 0 && a <= 6 && (u === 0 || u === 6) || u >= 2 && u <= 4 && a >= 2 && a <= 4 ? t.set(i + u, s + a, !0, !0) : t.set(i + u, s + a, !1, !0));
  }
}
function gn(t) {
  const e = t.size;
  for (let r = 8; r < e - 8; r++) {
    const o = r % 2 === 0;
    t.set(r, 6, o, !0), t.set(6, r, o, !0);
  }
}
function mn(t, e) {
  const r = an.getPositions(e);
  for (let o = 0; o < r.length; o++) {
    const n = r[o][0], i = r[o][1];
    for (let s = -2; s <= 2; s++)
      for (let u = -2; u <= 2; u++)
        s === -2 || s === 2 || u === -2 || u === 2 || s === 0 && u === 0 ? t.set(n + s, i + u, !0, !0) : t.set(n + s, i + u, !1, !0);
  }
}
function wn(t, e) {
  const r = t.size, o = x.getEncodedBits(e);
  let n, i, s;
  for (let u = 0; u < 18; u++)
    n = Math.floor(u / 3), i = u % 3 + r - 8 - 3, s = (o >> u & 1) === 1, t.set(n, i, s, !0), t.set(i, n, s, !0);
}
function ut(t, e, r) {
  const o = t.size, n = fn.getEncodedBits(e, r);
  let i, s;
  for (i = 0; i < 15; i++)
    s = (n >> i & 1) === 1, i < 6 ? t.set(i, 8, s, !0) : i < 8 ? t.set(i + 1, 8, s, !0) : t.set(o - 15 + i, 8, s, !0), i < 8 ? t.set(8, o - i - 1, s, !0) : i < 9 ? t.set(8, 15 - i - 1 + 1, s, !0) : t.set(8, 15 - i - 1, s, !0);
  t.set(o - 8, 8, 1, !0);
}
function pn(t, e) {
  const r = t.size;
  let o = -1, n = r - 1, i = 7, s = 0;
  for (let u = r - 1; u > 0; u -= 2)
    for (u === 6 && u--; ; ) {
      for (let a = 0; a < 2; a++)
        if (!t.isReserved(n, u - a)) {
          let l = !1;
          s < e.length && (l = (e[s] >>> i & 1) === 1), t.set(n, u - a, l), i--, i === -1 && (s++, i = 7);
        }
      if (n += o, n < 0 || r <= n) {
        n -= o, o = -o;
        break;
      }
    }
}
function yn(t, e, r) {
  const o = new sn();
  r.forEach(function(a) {
    o.put(a.mode.bit, 4), o.put(a.getLength(), dn.getCharCountIndicator(a.mode, t)), a.write(o);
  });
  const n = rt.getSymbolTotalCodewords(t), i = ft.getTotalCodewordsCount(t, e), s = (n - i) * 8;
  for (o.getLengthInBits() + 4 <= s && o.put(0, 4); o.getLengthInBits() % 8 !== 0; )
    o.putBit(0);
  const u = (s - o.getLengthInBits()) / 8;
  for (let a = 0; a < u; a++)
    o.put(a % 2 ? 17 : 236, 8);
  return Cn(o, t, e);
}
function Cn(t, e, r) {
  const o = rt.getSymbolTotalCodewords(e), n = ft.getTotalCodewordsCount(e, r), i = o - n, s = ft.getBlocksCount(e, r), u = o % s, a = s - u, l = Math.floor(o / s), c = Math.floor(i / s), h = c + 1, g = l - c, d = new ln(g);
  let w = 0;
  const p = new Array(s), B = new Array(s);
  let y = 0;
  const E = new Uint8Array(t.buffer);
  for (let A = 0; A < s; A++) {
    const M = A < a ? c : h;
    p[A] = E.slice(w, w + M), B[A] = d.encode(p[A]), w += M, y = Math.max(y, M);
  }
  const m = new Uint8Array(o);
  let f = 0, b, S;
  for (b = 0; b < y; b++)
    for (S = 0; S < s; S++)
      b < p[S].length && (m[f++] = p[S][b]);
  for (b = 0; b < g; b++)
    for (S = 0; S < s; S++)
      m[f++] = B[S][b];
  return m;
}
function En(t, e, r, o) {
  let n;
  if (Array.isArray(t))
    n = st.fromArray(t);
  else if (typeof t == "string") {
    let l = e;
    if (!l) {
      const c = st.rawSplit(t);
      l = x.getBestVersionForData(c, r);
    }
    n = st.fromString(t, l || 40);
  } else
    throw new Error("Invalid data");
  const i = x.getBestVersionForData(n, r);
  if (!i)
    throw new Error("The amount of data is too big to be stored in a QR Code");
  if (!e)
    e = i;
  else if (e < i)
    throw new Error(
      `
The chosen QR Code version cannot contain this amount of data.
Minimum version required to store current data is: ` + i + `.
`
    );
  const s = yn(e, r, n), u = rt.getSymbolSize(e), a = new un(u);
  return hn(a, e), gn(a), mn(a, e), ut(a, r, 0), e >= 7 && wn(a, e), pn(a, s), isNaN(o) && (o = lt.getBestMask(
    a,
    ut.bind(null, a, r)
  )), lt.applyMask(o, a), ut(a, r, o), {
    modules: a,
    version: e,
    errorCorrectionLevel: r,
    maskPattern: o,
    segments: n
  };
}
Vt.create = function(e, r) {
  if (typeof e > "u" || e === "")
    throw new Error("No input text");
  let o = it.M, n, i;
  return typeof r < "u" && (o = it.from(r.errorCorrectionLevel, it.M), n = x.from(r.version), i = lt.from(r.maskPattern), r.toSJISFunc && rt.setToSJISFunction(r.toSJISFunc)), En(e, n, o, i);
};
var xt = {}, yt = {};
(function(t) {
  function e(r) {
    if (typeof r == "number" && (r = r.toString()), typeof r != "string")
      throw new Error("Color should be defined as hex string");
    let o = r.slice().replace("#", "").split("");
    if (o.length < 3 || o.length === 5 || o.length > 8)
      throw new Error("Invalid hex color: " + r);
    (o.length === 3 || o.length === 4) && (o = Array.prototype.concat.apply([], o.map(function(i) {
      return [i, i];
    }))), o.length === 6 && o.push("F", "F");
    const n = parseInt(o.join(""), 16);
    return {
      r: n >> 24 & 255,
      g: n >> 16 & 255,
      b: n >> 8 & 255,
      a: n & 255,
      hex: "#" + o.slice(0, 6).join("")
    };
  }
  t.getOptions = function(o) {
    o || (o = {}), o.color || (o.color = {});
    const n = typeof o.margin > "u" || o.margin === null || o.margin < 0 ? 4 : o.margin, i = o.width && o.width >= 21 ? o.width : void 0, s = o.scale || 4;
    return {
      width: i,
      scale: i ? 4 : s,
      margin: n,
      color: {
        dark: e(o.color.dark || "#000000ff"),
        light: e(o.color.light || "#ffffffff")
      },
      type: o.type,
      rendererOpts: o.rendererOpts || {}
    };
  }, t.getScale = function(o, n) {
    return n.width && n.width >= o + n.margin * 2 ? n.width / (o + n.margin * 2) : n.scale;
  }, t.getImageWidth = function(o, n) {
    const i = t.getScale(o, n);
    return Math.floor((o + n.margin * 2) * i);
  }, t.qrToImageData = function(o, n, i) {
    const s = n.modules.size, u = n.modules.data, a = t.getScale(s, i), l = Math.floor((s + i.margin * 2) * a), c = i.margin * a, h = [i.color.light, i.color.dark];
    for (let g = 0; g < l; g++)
      for (let d = 0; d < l; d++) {
        let w = (g * l + d) * 4, p = i.color.light;
        if (g >= c && d >= c && g < l - c && d < l - c) {
          const B = Math.floor((g - c) / a), y = Math.floor((d - c) / a);
          p = h[u[B * s + y] ? 1 : 0];
        }
        o[w++] = p.r, o[w++] = p.g, o[w++] = p.b, o[w] = p.a;
      }
  };
})(yt);
(function(t) {
  const e = yt;
  function r(n, i, s) {
    n.clearRect(0, 0, i.width, i.height), i.style || (i.style = {}), i.height = s, i.width = s, i.style.height = s + "px", i.style.width = s + "px";
  }
  function o() {
    try {
      return document.createElement("canvas");
    } catch {
      throw new Error("You need to specify a canvas element");
    }
  }
  t.render = function(i, s, u) {
    let a = u, l = s;
    typeof a > "u" && (!s || !s.getContext) && (a = s, s = void 0), s || (l = o()), a = e.getOptions(a);
    const c = e.getImageWidth(i.modules.size, a), h = l.getContext("2d"), g = h.createImageData(c, c);
    return e.qrToImageData(g.data, i, a), r(h, l, c), h.putImageData(g, 0, 0), l;
  }, t.renderToDataURL = function(i, s, u) {
    let a = u;
    typeof a > "u" && (!s || !s.getContext) && (a = s, s = void 0), a || (a = {});
    const l = t.render(i, s, a), c = a.type || "image/png", h = a.rendererOpts || {};
    return l.toDataURL(c, h.quality);
  };
})(xt);
var te = {};
const bn = yt;
function vt(t, e) {
  const r = t.a / 255, o = e + '="' + t.hex + '"';
  return r < 1 ? o + " " + e + '-opacity="' + r.toFixed(2).slice(1) + '"' : o;
}
function at(t, e, r) {
  let o = t + e;
  return typeof r < "u" && (o += " " + r), o;
}
function Bn(t, e, r) {
  let o = "", n = 0, i = !1, s = 0;
  for (let u = 0; u < t.length; u++) {
    const a = Math.floor(u % e), l = Math.floor(u / e);
    !a && !i && (i = !0), t[u] ? (s++, u > 0 && a > 0 && t[u - 1] || (o += i ? at("M", a + r, 0.5 + l + r) : at("m", n, 0), n = 0, i = !1), a + 1 < e && t[u + 1] || (o += at("h", s), s = 0)) : n++;
  }
  return o;
}
te.render = function(e, r, o) {
  const n = bn.getOptions(r), i = e.modules.size, s = e.modules.data, u = i + n.margin * 2, a = n.color.light.a ? "<path " + vt(n.color.light, "fill") + ' d="M0 0h' + u + "v" + u + 'H0z"/>' : "", l = "<path " + vt(n.color.dark, "stroke") + ' d="' + Bn(s, i, n.margin) + '"/>', c = 'viewBox="0 0 ' + u + " " + u + '"', g = '<svg xmlns="http://www.w3.org/2000/svg" ' + (n.width ? 'width="' + n.width + '" height="' + n.width + '" ' : "") + c + ' shape-rendering="crispEdges">' + a + l + `</svg>
`;
  return typeof o == "function" && o(null, g), g;
};
const Sn = Fe, dt = Vt, ee = xt, An = te;
function Ct(t, e, r, o, n) {
  const i = [].slice.call(arguments, 1), s = i.length, u = typeof i[s - 1] == "function";
  if (!u && !Sn())
    throw new Error("Callback required as last argument");
  if (u) {
    if (s < 2)
      throw new Error("Too few arguments provided");
    s === 2 ? (n = r, r = e, e = o = void 0) : s === 3 && (e.getContext && typeof n > "u" ? (n = o, o = void 0) : (n = o, o = r, r = e, e = void 0));
  } else {
    if (s < 1)
      throw new Error("Too few arguments provided");
    return s === 1 ? (r = e, e = o = void 0) : s === 2 && !e.getContext && (o = r, r = e, e = void 0), new Promise(function(a, l) {
      try {
        const c = dt.create(r, o);
        a(t(c, e, o));
      } catch (c) {
        l(c);
      }
    });
  }
  try {
    const a = dt.create(r, o);
    n(null, t(a, e, o));
  } catch (a) {
    n(a);
  }
}
Y.create = dt.create;
Y.toCanvas = Ct.bind(null, ee.render);
Y.toDataURL = Ct.bind(null, ee.renderToDataURL);
Y.toString = Ct.bind(null, function(t, e, r) {
  return An.render(t, r);
});
function Mn(t, e) {
  const r = Ue(t), o = L("");
  return k(
    r,
    async (n) => {
      r.value && De && (o.value = await Y.toDataURL(n, e));
    },
    { immediate: !0 }
  ), o;
}
function vn(t, e) {
  const r = L(t), o = Mn(r), n = new Et();
  return n.addMethod("updateText", (i) => {
    r.value = i;
  }), n.addMethod("getQRCode", () => o.value), zt(() => {
    e("change", {
      eventName: "qrcode",
      value: o.value
    });
  }), k(o, (i) => {
    e("change", {
      eventName: "qrcode",
      value: i
    });
  }), n;
}
class Et {
  constructor() {
    bt(this, "methods", /* @__PURE__ */ new Map());
  }
  addMethod(e, r) {
    this.methods.set(e, r);
  }
  getAllMethods() {
    return Object.fromEntries(this.methods.entries());
  }
}
const Nt = /* @__PURE__ */ new Map([
  ["useBreakpoints", Le],
  ["useDark", _e],
  ["useQRCode", vn]
]);
function Nn(t, e = [], r) {
  if (!Nt.has(t))
    throw new Error(`Method ${t} not found`);
  return Nt.get(t)(...e, r);
}
const Rn = /* @__PURE__ */ le({
  __name: "VueUse",
  props: {
    method: {},
    args: {}
  },
  emits: ["change"],
  setup(t, { expose: e, emit: r }) {
    const o = t, n = r, i = Nn(o.method, o.args, n);
    return e(i.getAllMethods()), (s, u) => null;
  }
});
export {
  Rn as default
};