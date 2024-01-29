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
    }
  },
  props: {
    defaults: Object,
    tasks: Array,
  },
};
