var Z = Object.defineProperty;
var ee = (e, n, t) => n in e ? Z(e, n, { enumerable: !0, configurable: !0, writable: !0, value: t }) : e[n] = t;
var W = (e, n, t) => (ee(e, typeof n != "symbol" ? n + "" : n, t), t);
const te = Vue.isRef;
const N = Vue.ref;
const ne = Vue.getCurrentScope;
const re = Vue.onScopeDispose;
const oe = Vue.unref;
const ae = Vue.toRef;
const z = Vue.readonly;
const ie = Vue.customRef;
const I = Vue.onMounted;
const J = Vue.nextTick;
const q = Vue.getCurrentInstance;
const _ = Vue.watch;
const k = Vue.computed;
const se = Vue.watchEffect;
const ue = Vue.shallowRef;
const le = Vue.defineComponent;

function P(e) {
  return ne() ? (re(e), !0) : !1;
}
function E(e) {
  return typeof e == "function" ? e() : oe(e);
}
const ce = typeof window < "u" && typeof document < "u";
typeof WorkerGlobalScope < "u" && globalThis instanceof WorkerGlobalScope;
const fe = Object.prototype.toString, de = (e) => fe.call(e) === "[object Object]", G = () => {
};
function he(e, n) {
  function t(...a) {
    return new Promise((r, o) => {
      Promise.resolve(e(() => n.apply(this, a), { fn: n, thisArg: this, args: a })).then(r).catch(o);
    });
  }
  return t;
}
const H = (e) => e();
function me(e = H) {
  const n = N(!0);
  function t() {
    n.value = !1;
  }
  function a() {
    n.value = !0;
  }
  const r = (...o) => {
    n.value && e(...o);
  };
  return { isActive: z(n), pause: t, resume: a, eventFilter: r };
}
function pe(e, n) {
  var t;
  if (typeof e == "number")
    return e + n;
  const a = ((t = e.match(/^-?\d+\.?\d*/)) == null ? void 0 : t[0]) || "", r = e.slice(a.length), o = Number.parseFloat(a) + n;
  return Number.isNaN(o) ? e : o + r;
}
function ge(e) {
  return e || q();
}
function ve(...e) {
  if (e.length !== 1)
    return ae(...e);
  const n = e[0];
  return typeof n == "function" ? z(ie(() => ({ get: n, set: G }))) : N(n);
}
function we(e, n, t = {}) {
  const {
    eventFilter: a = H,
    ...r
  } = t;
  return _(
    e,
    he(
      a,
      n
    ),
    r
  );
}
function ye(e, n, t = {}) {
  const {
    eventFilter: a,
    ...r
  } = t, { eventFilter: o, pause: u, resume: c, isActive: f } = me(a);
  return { stop: we(
    e,
    n,
    {
      ...r,
      eventFilter: o
    }
  ), pause: u, resume: c, isActive: f };
}
function U(e, n = !0, t) {
  ge() ? I(e, t) : n ? e() : J(e);
}
function be(e = !1, n = {}) {
  const {
    truthyValue: t = !0,
    falsyValue: a = !1
  } = n, r = te(e), o = N(e);
  function u(c) {
    if (arguments.length)
      return o.value = c, o.value;
    {
      const f = E(t);
      return o.value = o.value === f ? E(a) : f, o.value;
    }
  }
  return r ? u : [o, u];
}
function K(e) {
  var n;
  const t = E(e);
  return (n = t == null ? void 0 : t.$el) != null ? n : t;
}
const A = ce ? window : void 0;
function R(...e) {
  let n, t, a, r;
  if (typeof e[0] == "string" || Array.isArray(e[0]) ? ([t, a, r] = e, n = A) : [n, t, a, r] = e, !n)
    return G;
  Array.isArray(t) || (t = [t]), Array.isArray(a) || (a = [a]);
  const o = [], u = () => {
    o.forEach((i) => i()), o.length = 0;
  }, c = (i, l, h, v) => (i.addEventListener(l, h, v), () => i.removeEventListener(l, h, v)), f = _(
    () => [K(n), E(r)],
    ([i, l]) => {
      if (u(), !i)
        return;
      const h = de(l) ? { ...l } : l;
      o.push(
        ...t.flatMap((v) => a.map((w) => c(i, v, w, h)))
      );
    },
    { immediate: !0, flush: "post" }
  ), d = () => {
    f(), u();
  };
  return P(d), d;
}
function Se() {
  const e = N(!1), n = q();
  return n && I(() => {
    e.value = !0;
  }, n), e;
}
function Me(e) {
  const n = Se();
  return k(() => (n.value, !!e()));
}
function D(e, n = {}) {
  const { window: t = A } = n, a = Me(() => t && "matchMedia" in t && typeof t.matchMedia == "function");
  let r;
  const o = N(!1), u = (d) => {
    o.value = d.matches;
  }, c = () => {
    r && ("removeEventListener" in r ? r.removeEventListener("change", u) : r.removeListener(u));
  }, f = se(() => {
    a.value && (c(), r = t.matchMedia(E(e)), "addEventListener" in r ? r.addEventListener("change", u) : r.addListener(u), o.value = r.matches);
  });
  return P(() => {
    f(), c(), r = void 0;
  }), o;
}
function Oe(e, n = {}) {
  function t(i, l) {
    let h = E(e[E(i)]);
    return l != null && (h = pe(h, l)), typeof h == "number" && (h = `${h}px`), h;
  }
  const { window: a = A, strategy: r = "min-width" } = n;
  function o(i) {
    return a ? a.matchMedia(i).matches : !1;
  }
  const u = (i) => D(() => `(min-width: ${t(i)})`, n), c = (i) => D(() => `(max-width: ${t(i)})`, n), f = Object.keys(e).reduce((i, l) => (Object.defineProperty(i, l, {
    get: () => r === "min-width" ? u(l) : c(l),
    enumerable: !0,
    configurable: !0
  }), i), {});
  function d() {
    const i = Object.keys(e).map((l) => [l, u(l)]);
    return k(() => i.filter(([, l]) => l.value).map(([l]) => l));
  }
  return Object.assign(f, {
    greaterOrEqual: u,
    smallerOrEqual: c,
    greater(i) {
      return D(() => `(min-width: ${t(i, 0.1)})`, n);
    },
    smaller(i) {
      return D(() => `(max-width: ${t(i, -0.1)})`, n);
    },
    between(i, l) {
      return D(() => `(min-width: ${t(i)}) and (max-width: ${t(l, -0.1)})`, n);
    },
    isGreater(i) {
      return o(`(min-width: ${t(i, 0.1)})`);
    },
    isGreaterOrEqual(i) {
      return o(`(min-width: ${t(i)})`);
    },
    isSmaller(i) {
      return o(`(max-width: ${t(i, -0.1)})`);
    },
    isSmallerOrEqual(i) {
      return o(`(max-width: ${t(i)})`);
    },
    isInBetween(i, l) {
      return o(`(min-width: ${t(i)}) and (max-width: ${t(l, -0.1)})`);
    },
    current: d,
    active() {
      const i = d();
      return k(() => i.value.length === 0 ? "" : i.value.at(-1));
    }
  });
}
const x = typeof globalThis < "u" ? globalThis : typeof window < "u" ? window : typeof global < "u" ? global : typeof self < "u" ? self : {}, F = "__vueuse_ssr_handlers__", ke = /* @__PURE__ */ Ee();
function Ee() {
  return F in x || (x[F] = x[F] || {}), x[F];
}
function Q(e, n) {
  return ke[e] || n;
}
function Ae(e) {
  return e == null ? "any" : e instanceof Set ? "set" : e instanceof Map ? "map" : e instanceof Date ? "date" : typeof e == "boolean" ? "boolean" : typeof e == "string" ? "string" : typeof e == "object" ? "object" : Number.isNaN(e) ? "any" : "number";
}
const Ce = {
  boolean: {
    read: (e) => e === "true",
    write: (e) => String(e)
  },
  object: {
    read: (e) => JSON.parse(e),
    write: (e) => JSON.stringify(e)
  },
  number: {
    read: (e) => Number.parseFloat(e),
    write: (e) => String(e)
  },
  any: {
    read: (e) => e,
    write: (e) => String(e)
  },
  string: {
    read: (e) => e,
    write: (e) => String(e)
  },
  map: {
    read: (e) => new Map(JSON.parse(e)),
    write: (e) => JSON.stringify(Array.from(e.entries()))
  },
  set: {
    read: (e) => new Set(JSON.parse(e)),
    write: (e) => JSON.stringify(Array.from(e))
  },
  date: {
    read: (e) => new Date(e),
    write: (e) => e.toISOString()
  }
}, V = "vueuse-storage";
function De(e, n, t, a = {}) {
  var r;
  const {
    flush: o = "pre",
    deep: u = !0,
    listenToStorageChanges: c = !0,
    writeDefaults: f = !0,
    mergeDefaults: d = !1,
    shallow: i,
    window: l = A,
    eventFilter: h,
    onError: v = (s) => {
      console.error(s);
    },
    initOnMounted: w
  } = a, g = (i ? ue : N)(typeof n == "function" ? n() : n);
  if (!t)
    try {
      t = Q("getDefaultStorage", () => {
        var s;
        return (s = A) == null ? void 0 : s.localStorage;
      })();
    } catch (s) {
      v(s);
    }
  if (!t)
    return g;
  const b = E(n), $ = Ae(b), S = (r = a.serializer) != null ? r : Ce[$], { pause: L, resume: m } = ye(
    g,
    () => T(g.value),
    { flush: o, deep: u, eventFilter: h }
  );
  l && c && U(() => {
    R(l, "storage", y), R(l, V, j), w && y();
  }), w || y();
  function M(s, p) {
    l && l.dispatchEvent(new CustomEvent(V, {
      detail: {
        key: e,
        oldValue: s,
        newValue: p,
        storageArea: t
      }
    }));
  }
  function T(s) {
    try {
      const p = t.getItem(e);
      if (s == null)
        M(p, null), t.removeItem(e);
      else {
        const O = S.write(s);
        p !== O && (t.setItem(e, O), M(p, O));
      }
    } catch (p) {
      v(p);
    }
  }
  function C(s) {
    const p = s ? s.newValue : t.getItem(e);
    if (p == null)
      return f && b != null && t.setItem(e, S.write(b)), b;
    if (!s && d) {
      const O = S.read(p);
      return typeof d == "function" ? d(O, b) : $ === "object" && !Array.isArray(O) ? { ...b, ...O } : O;
    } else
      return typeof p != "string" ? p : S.read(p);
  }
  function y(s) {
    if (!(s && s.storageArea !== t)) {
      if (s && s.key == null) {
        g.value = b;
        return;
      }
      if (!(s && s.key !== e)) {
        L();
        try {
          (s == null ? void 0 : s.newValue) !== S.write(g.value) && (g.value = C(s));
        } catch (p) {
          v(p);
        } finally {
          s ? J(m) : m();
        }
      }
    }
  }
  function j(s) {
    y(s.detail);
  }
  return g;
}
function X(e) {
  return D("(prefers-color-scheme: dark)", e);
}
function _e(e = {}) {
  const {
    selector: n = "html",
    attribute: t = "class",
    initialValue: a = "auto",
    window: r = A,
    storage: o,
    storageKey: u = "vueuse-color-scheme",
    listenToStorageChanges: c = !0,
    storageRef: f,
    emitAuto: d,
    disableTransition: i = !0
  } = e, l = {
    auto: "",
    light: "light",
    dark: "dark",
    ...e.modes || {}
  }, h = X({ window: r }), v = k(() => h.value ? "dark" : "light"), w = f || (u == null ? ve(a) : De(u, a, o, { window: r, listenToStorageChanges: c })), g = k(() => w.value === "auto" ? v.value : w.value), b = Q(
    "updateHTMLAttrs",
    (m, M, T) => {
      const C = typeof m == "string" ? r == null ? void 0 : r.document.querySelector(m) : K(m);
      if (!C)
        return;
      let y;
      if (i) {
        y = r.document.createElement("style");
        const j = "*,*::before,*::after{-webkit-transition:none!important;-moz-transition:none!important;-o-transition:none!important;-ms-transition:none!important;transition:none!important}";
        y.appendChild(document.createTextNode(j)), r.document.head.appendChild(y);
      }
      if (M === "class") {
        const j = T.split(/\s/g);
        Object.values(l).flatMap((s) => (s || "").split(/\s/g)).filter(Boolean).forEach((s) => {
          j.includes(s) ? C.classList.add(s) : C.classList.remove(s);
        });
      } else
        C.setAttribute(M, T);
      i && (r.getComputedStyle(y).opacity, document.head.removeChild(y));
    }
  );
  function $(m) {
    var M;
    b(n, t, (M = l[m]) != null ? M : m);
  }
  function S(m) {
    e.onChanged ? e.onChanged(m, $) : $(m);
  }
  _(g, S, { flush: "post", immediate: !0 }), U(() => S(g.value));
  const L = k({
    get() {
      return d ? w.value : g.value;
    },
    set(m) {
      w.value = m;
    }
  });
  try {
    return Object.assign(L, { store: w, system: v, state: g });
  } catch {
    return L;
  }
}
function Ne(e = {}) {
  const {
    valueDark: n = "dark",
    valueLight: t = "",
    window: a = A
  } = e, r = _e({
    ...e,
    onChanged: (c, f) => {
      var d;
      e.onChanged ? (d = e.onChanged) == null || d.call(e, c === "dark", f, c) : f(c);
    },
    modes: {
      dark: n,
      light: t
    }
  }), o = k(() => r.system ? r.system.value : X({ window: a }).value ? "dark" : "light");
  return k({
    get() {
      return r.value === "dark";
    },
    set(c) {
      const f = c ? "dark" : "light";
      o.value === f ? r.value = "auto" : r.value = f;
    }
  });
}
function $e(e, n) {
  const t = Oe(e), a = t.active(), r = new Y();
  return r.addMethod("active", () => a.value), r.addMethod(
    "between",
    (o, u) => t.between(o, u).value
  ), r.addMethod(
    "betweenReactively",
    (o, u, c) => {
      const f = t.between(o, u);
      _(f, (d) => {
        n("change", {
          eventName: c,
          value: d
        });
      });
    }
  ), _(a, (o) => {
    n("change", {
      eventName: "active",
      value: o
    });
  }), r;
}
function je(e, n, t) {
  const a = Ne(e);
  a.value = n;
  const r = be(a), o = new Y();
  return o.addMethod("toggleDark", (u) => {
    if (a.value !== u) {
      if (u === null) {
        r();
        return;
      }
      r(u);
    }
  }), _(a, (u) => {
    t("change", {
      eventName: "isDark",
      value: u
    });
  }), o;
}
class Y {
  constructor() {
    W(this, "methods", /* @__PURE__ */ new Map());
  }
  addMethod(n, t) {
    this.methods.set(n, t);
  }
  getAllMethods() {
    return Object.fromEntries(this.methods.entries());
  }
}
const B = /* @__PURE__ */ new Map([
  ["useBreakpoints", $e],
  ["useDark", je]
]);
function Le(e, n = [], t) {
  if (!B.has(e))
    throw new Error(`Method ${e} not found`);
  return B.get(e)(...n, t);
}
const Fe = /* @__PURE__ */ le({
  __name: "VueUse",
  props: {
    method: {},
    args: {}
  },
  emits: ["change"],
  setup(e, { expose: n, emit: t }) {
    const a = e, r = t, o = Le(a.method, a.args, r);
    return n(o.getAllMethods()), (u, c) => null;
  }
});
export {
  Fe as default
};