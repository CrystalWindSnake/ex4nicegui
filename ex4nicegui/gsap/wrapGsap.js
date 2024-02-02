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
        this[t.method](t.targets, t.options)
      })

      this.scriptTasks.forEach(script => {
        const fn = new Function('return ' + script)()
        fn(gsap)
      })

    })
  },

  methods: {
    from(targets, options) {
      convertDynamicProperties(options, false)
      gsap.from(targets, options)
    },
    to(targets, options) {
      convertDynamicProperties(options, false)
      gsap.to(targets, options)
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
