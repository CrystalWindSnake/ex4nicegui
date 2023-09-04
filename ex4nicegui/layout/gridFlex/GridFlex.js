const g = Vue.getCurrentScope
const x = Vue.onScopeDispose
const b = Vue.toRef
const S = Vue.readonly
const M = Vue.customRef
const f = Vue.ref
const d = Vue.computed
const $ = Vue.watchEffect
const O = Vue.getCurrentInstance
const k = Vue.onMounted
const E = Vue.defineComponent
const j = Vue.effect
const B = Vue.openBlock
const L = Vue.createElementBlock
const _ = Vue.normalizeStyle
const q = Vue.unref
const C = Vue.renderSlot
function N(n) {
  return g() ? (x(n), !0) : !1;
}
const R = typeof window < "u", G = () => {
};
function W(n, o) {
  var t;
  if (typeof n == "number")
    return n + o;
  const u = ((t = n.match(/^-?[0-9]+\.?[0-9]*/)) == null ? void 0 : t[0]) || "", r = n.slice(u.length), l = Number.parseFloat(u) + o;
  return Number.isNaN(l) ? n : l + r;
}
function z(...n) {
  if (n.length !== 1)
    return b(...n);
  const o = n[0];
  return typeof o == "function" ? S(M(() => ({ get: o, set: G }))) : f(o);
}
const h = R ? window : void 0;
function D() {
  const n = f(!1);
  return O() && k(() => {
    n.value = !0;
  }), n;
}
function F(n) {
  const o = D();
  return d(() => (o.value, !!n()));
}
function c(n, o = {}) {
  const { window: t = h } = o, u = F(() => t && "matchMedia" in t && typeof t.matchMedia == "function");
  let r;
  const l = f(!1), a = () => {
    r && ("removeEventListener" in r ? r.removeEventListener("change", e) : r.removeListener(e));
  }, e = () => {
    u.value && (a(), r = t.matchMedia(z(n).value), l.value = !!(r != null && r.matches), r && ("addEventListener" in r ? r.addEventListener("change", e) : r.addListener(e)));
  };
  return $(e), N(() => a()), l;
}
const I = {
  sm: 640,
  md: 768,
  lg: 1024,
  xl: 1280,
  "2xl": 1536
};
function Q(n, o = {}) {
  function t(e, s) {
    let i = n[e];
    return s != null && (i = W(i, s)), typeof i == "number" && (i = `${i}px`), i;
  }
  const { window: u = h } = o;
  function r(e) {
    return u ? u.matchMedia(e).matches : !1;
  }
  const l = (e) => c(`(min-width: ${t(e)})`, o), a = Object.keys(n).reduce((e, s) => (Object.defineProperty(e, s, {
    get: () => l(s),
    enumerable: !0,
    configurable: !0
  }), e), {});
  return Object.assign(a, {
    greater(e) {
      return c(`(min-width: ${t(e, 0.1)})`, o);
    },
    greaterOrEqual: l,
    smaller(e) {
      return c(`(max-width: ${t(e, -0.1)})`, o);
    },
    smallerOrEqual(e) {
      return c(`(max-width: ${t(e)})`, o);
    },
    between(e, s) {
      return c(`(min-width: ${t(e)}) and (max-width: ${t(s, -0.1)})`, o);
    },
    isGreater(e) {
      return r(`(min-width: ${t(e, 0.1)})`);
    },
    isGreaterOrEqual(e) {
      return r(`(min-width: ${t(e)})`);
    },
    isSmaller(e) {
      return r(`(max-width: ${t(e, -0.1)})`);
    },
    isSmallerOrEqual(e) {
      return r(`(max-width: ${t(e)})`);
    },
    isInBetween(e, s) {
      return r(`(min-width: ${t(e)}) and (max-width: ${t(s, -0.1)})`);
    },
    current() {
      const e = Object.keys(n).map((s) => [s, l(s)]);
      return d(() => e.filter(([, s]) => s.value).map(([s]) => s));
    }
  });
}
const U = /* @__PURE__ */ E({
  __name: "GridFlex",
  props: {
    normalStyles: null,
    breakpointStyleMap: null
  },
  setup(n) {
    const o = n, t = d(() => new Map(
      Object.entries(o.breakpointStyleMap)
    ));
    function u() {
      const l = Q(I), a = l.smaller("sm"), e = l.smaller("md"), s = l.smaller("lg"), i = l.smaller("xl"), v = l.smaller("2xl"), w = l["2xl"], y = {
        xs: a,
        sm: e,
        md: s,
        lg: i,
        xl: v,
        xxl: w
      };
      return d(() => {
        if (console.log("breakpointStyleMap", t.value), t.value.size === 0)
          return o.normalStyles;
        for (const [m, p] of Object.entries(y))
          if (p.value && (console.log("bp targging", m, p.value), t.value.has(m)))
            return console.log("trigg done:", t.value.get(m)), t.value.get(m);
        return o.normalStyles;
      });
    }
    const r = u();
    return j(() => {
      console.log("style:", r.value);
    }), (l, a) => (B(), L("div", {
      class: "grid",
      style: _(q(r))
    }, [
      C(l.$slots, "default")
    ], 4));
  }
});
export {
  U as default
};