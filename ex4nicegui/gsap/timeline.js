import { gsap } from "gsap";
import { convertDynamicProperties } from "../../static/utils/dynamic_properties.js";


export default {
  template: `<template></template>`,
  data() {

    const tl = gsap.timeline(this.defaults)
    this.tl = tl

    return {
    }

  },
  mounted() {
    document.addEventListener('DOMContentLoaded', () => {
      /**
       * @type any[]
       */
      const tasks = this.tasks
      tasks.forEach(t => {
        this[t.method](t.targets, t.vars, t.position)
      })

      this.scriptTasks.forEach(script => {
        const fn = new Function('return ' + script)()
        fn(this.tl, gsap)
      })

    })
  },

  methods: {
    from(targets, vars, position) {
      convertDynamicProperties(vars, false)
      this.tl.from(targets, vars, position)
    },
    to(targets, vars, position) {
      convertDynamicProperties(vars, false)
      this.tl.to(targets, vars, position)
    },
    runScript(script) {
      const fn = new Function('return ' + script)()
      fn(this.tl, gsap)
    },
    callTimeline(name, ...args) {
      this.tl[name](...args)
    }
  },
  props: {
    defaults: Object,
    tasks: Array,
    scriptTasks: Array,
  },
};
