import { convertDynamicProperties } from "../../static/utils/dynamic_properties.js";

export default {
  template: "<div></div>",
  mounted() {
    this.chart = echarts.init(this.$el, this.theme);
    this.chart.on("click", (e) => this.$emit("chartClick", e));
    this.chart.getZr().on("click", (e) => {
      if (!e.target) {
        this.$emit("chartClickBlank")
      }
    });
    this.updateOptions(this.options);

    this.resizeObs = new ResizeObserver(this.chart.resize)
    this.resizeObs.observe(this.$el);
  },
  beforeDestroy() {
    this.chart.dispose();
    this.resizeObs.unobserve();
  },
  beforeUnmount() {
    this.chart.dispose();
  },
  methods: {
    updateOptions(options, opts) {
      convertDynamicProperties(options, true);
      this.chart.setOption(options, opts);
    },
  },
  props: {
    options: Object,
    theme: String | Object | undefined
  },
};
