const M = Vue.getCurrentScope
const _ = Vue.onScopeDispose
const k = Vue.toRef
const q = Vue.readonly
const j = Vue.customRef
const d = Vue.ref
const m = Vue.computed
const B = Vue.watchEffect
const L = Vue.getCurrentInstance
const C = Vue.onMounted
const N = Vue.defineComponent
const R = Vue.openBlock
const G = Vue.createElementBlock
const W = Vue.normalizeStyle
const z = Vue.unref
const D = Vue.renderSlot
function F(n) {
  return M() ? (_(n), !0) : !1;
}
const I = typeof window < "u", Q = () => {
};
function P(n, s) {
  var r;
  if (typeof n == "number")
    return n + s;
  const o = ((r = n.match(/^-?[0-9]+\.?[0-9]*/)) == null ? void 0 : r[0]) || "", l = n.slice(o.length), t = Number.parseFloat(o) + s;
  return Number.isNaN(t) ? n : t + l;
}
function U(...n) {
  if (n.length !== 1)
    return k(...n);
  const s = n[0];
  return typeof s == "function" ? q(j(() => ({ get: s, set: Q }))) : d(s);
}
const p = I ? window : void 0;
function V() {
  const n = d(!1);
  return L() && C(() => {
    n.value = !0;
  }), n;
}
function A(n) {
  const s = V();
  return m(() => (s.value, !!n()));
}
function c(n, s = {}) {
  const { window: r = p } = s, o = A(() => r && "matchMedia" in r && typeof r.matchMedia == "function");
  let l;
  const t = d(!1), i = () => {
    l && ("removeEventListener" in l ? l.removeEventListener("change", e) : l.removeListener(e));
  }, e = () => {
    o.value && (i(), l = r.matchMedia(U(n).value), t.value = !!(l != null && l.matches), l && ("addEventListener" in l ? l.addEventListener("change", e) : l.addListener(e)));
  };
  return B(e), F(() => i()), t;
}
function H(n, s = {}) {
  function r(e, u) {
    let a = n[e];
    return u != null && (a = P(a, u)), typeof a == "number" && (a = `${a}px`), a;
  }
  const { window: o = p } = s;
  function l(e) {
    return o ? o.matchMedia(e).matches : !1;
  }
  const t = (e) => c(`(min-width: ${r(e)})`, s), i = Object.keys(n).reduce((e, u) => (Object.defineProperty(e, u, {
    get: () => t(u),
    enumerable: !0,
    configurable: !0
  }), e), {});
  return Object.assign(i, {
    greater(e) {
      return c(`(min-width: ${r(e, 0.1)})`, s);
    },
    greaterOrEqual: t,
    smaller(e) {
      return c(`(max-width: ${r(e, -0.1)})`, s);
    },
    smallerOrEqual(e) {
      return c(`(max-width: ${r(e)})`, s);
    },
    between(e, u) {
      return c(`(min-width: ${r(e)}) and (max-width: ${r(u, -0.1)})`, s);
    },
    isGreater(e) {
      return l(`(min-width: ${r(e, 0.1)})`);
    },
    isGreaterOrEqual(e) {
      return l(`(min-width: ${r(e)})`);
    },
    isSmaller(e) {
      return l(`(max-width: ${r(e, -0.1)})`);
    },
    isSmallerOrEqual(e) {
      return l(`(max-width: ${r(e)})`);
    },
    isInBetween(e, u) {
      return l(`(min-width: ${r(e)}) and (max-width: ${r(u, -0.1)})`);
    },
    current() {
      const e = Object.keys(n).map((u) => [u, t(u)]);
      return m(() => e.filter(([, u]) => u.value).map(([u]) => u));
    }
  });
}
const T = /* @__PURE__ */ N({
  __name: "GridFlex",
  props: {
    normalStyles: null,
    breakpointStyleMap: null
  },
  setup(n) {
    const s = n, r = m(() => new Map(
      Object.entries(s.breakpointStyleMap)
    ));
    function o() {
      const t = H({
        sm: 600,
        md: 1024,
        lg: 1440,
        xl: 1920
      }), i = t.smaller("sm"), e = t.between("sm", "md"), u = t.between("md", "lg"), a = t.between("lg", "xl"), g = t.greaterOrEqual("xl"), h = t.smaller("sm"), w = t.smaller("md"), v = t.smaller("lg"), y = t.smaller("xl"), x = t.greaterOrEqual("sm"), b = t.greaterOrEqual("md"), O = t.greaterOrEqual("lg"), S = t.greaterOrEqual("xl"), E = {
        xs: i,
        sm: e,
        md: u,
        lg: a,
        xl: g,
        "lt-sm": h,
        "lt-md": w,
        "lt-lg": v,
        "lt-xl": y,
        "gt-xs": x,
        "gt-sm": b,
        "gt-md": O,
        "gt-lg": S
      };
      return m(() => {
        if (r.value.size === 0)
          return s.normalStyles;
        for (const [f, $] of Object.entries(E))
          if ($.value && r.value.has(f))
            return r.value.get(f);
        return s.normalStyles;
      });
    }
    const l = o();
    return (t, i) => (R(), G("div", {
      class: "grid",
      style: W(z(l))
    }, [
      D(t.$slots, "default")
    ], 4));
  }
});
export {
  T as default
};