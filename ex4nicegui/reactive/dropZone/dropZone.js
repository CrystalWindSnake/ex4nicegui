const h = Vue.getCurrentScope
const _ = Vue.onScopeDispose
const b = Vue.unref
const v = Vue.watch
const w = Vue.defineComponent
const D = Vue.onMounted
function E(t) {
  return h() ? (_(t), !0) : !1;
}
function g(t) {
  return typeof t == "function" ? t() : b(t);
}
const Z = typeof window < "u", S = () => {
};
function T(t) {
  var a;
  const n = g(t);
  return (a = n == null ? void 0 : n.$el) != null ? a : n;
}
const K = Z ? window : void 0;
function y(...t) {
  let a, n, i, l;
  if (typeof t[0] == "string" || Array.isArray(t[0]) ? ([n, i, l] = t, a = K) : [a, n, i, l] = t, !a)
    return S;
  Array.isArray(n) || (n = [n]), Array.isArray(i) || (i = [i]);
  const d = [], s = () => {
    d.forEach((u) => u()), d.length = 0;
  }, p = (u, c, e, r) => (u.addEventListener(c, e, r), () => u.removeEventListener(c, e, r)), f = v(
    () => [T(a), g(l)],
    ([u, c]) => {
      s(), u && d.push(
        ...n.flatMap((e) => i.map((r) => p(u, e, r, c)))
      );
    },
    { immediate: !0, flush: "post" }
  ), A = () => {
    f(), s();
  };
  return E(A), A;
}
const B = /* @__PURE__ */ w({
  __name: "DropZone",
  props: {
    dropZoneId: null
  },
  emits: ["onDraggableKeysUpdated"],
  setup(t, { expose: a, emit: n }) {
    const i = t, l = "data-drag-zone-id", d = "data-draggable-key";
    let s = null;
    const p = /* @__PURE__ */ new Set(), f = /* @__PURE__ */ new Set();
    function A(e, r) {
      if (console.log("apply:", e, r), p.has(e))
        return;
      const o = document.getElementById(e);
      if (!o)
        throw new Error(`not found draggable item[id = ${e}]`);
      o.setAttribute("draggable", "true"), o.setAttribute(l, i.dropZoneId), o.setAttribute(d, r), y(o, "dragstart", (m) => {
        s = o;
      }), y(o, "dragend", (m) => {
        s = null;
      }), p.add(e);
    }
    function u() {
      n("onDraggableKeysUpdated", { keys: Array.from(f.values()) });
    }
    function c(e) {
      f.has(e) && (f.delete(e), u());
    }
    return a({
      apply: A,
      removeKey: c
    }), D(() => {
      const e = document.getElementById(i.dropZoneId);
      if (!e)
        throw new Error(`not found drop zone[id = ${i.dropZoneId}]`);
      y(e, "dragover", (r) => {
        if (!s || i.dropZoneId !== s.getAttribute(l) || !s.hasAttribute(d))
          return;
        const o = s.getAttribute(d);
        f.has(o) || r.preventDefault();
      }), y(e, "drop", (r) => {
        if (!s)
          return;
        r.preventDefault();
        const o = s.getAttribute(d);
        f.has(o) || (f.add(o), u());
      });
    }), (e, r) => null;
  }
});
export {
  B as default
};