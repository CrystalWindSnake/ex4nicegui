import { gsap } from "gsap";
import { convertDynamicProperties } from "../../static/utils/dynamic_properties.js";


export default {
  template: `<template></template>`,
  data: () => ({
  }),
  mounted() {
    gsap.defaults(this.defaults)

    document.addEventListener('DOMContentLoaded', () => {
      /**
       * @type any[]
       */
      const tasks = this.tasks
      tasks.forEach(t => {
        this[t.method](t.targets, t.vars)
      })

      this.scriptTasks.forEach(script => {
        const fn = new Function('return ' + script)()
        fn(gsap)
      })

    })
  },

  methods: {
    from(targets, vars) {
      convertDynamicProperties(vars, false)
      gsap.from(targets, vars)
    },
    to(targets, vars) {
      convertDynamicProperties(vars, false)
      gsap.to(targets, vars)
    },
    runScript(script) {
      const fn = new Function('return ' + script)()
      fn(gsap)
    }
  },
  props: {
    defaults: Object,
    tasks: Array,
    scriptTasks: Array,
  },
};
