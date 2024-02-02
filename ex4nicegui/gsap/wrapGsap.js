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
        convertDynamicProperties(t.options, false)
        gsap[t.method](t.target, t.options)
      })

      this.scriptTasks.forEach(script => {
        const fn = new Function('return ' + script)()
        fn(gsap)
      })

    })
  },

  methods: {
    from(target, options) {
      convertDynamicProperties(options, false)
      gsap.from(target, options)
    },
    to(target, options) {
      convertDynamicProperties(options, false)
      gsap.to(target, options)
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
