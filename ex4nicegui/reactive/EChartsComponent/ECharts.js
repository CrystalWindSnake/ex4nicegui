import { convertDynamicProperties } from "../../static/utils/dynamic_properties.js";

export default {
  template: "<div></div>",
  mounted() {
    this.chart = echarts.init(this.$el, this.theme);
    this.chart.getZr().on("click", (e) => {
      if (!e.target) {
        this.$emit("clickBlank")
      }
    });


    this.update_chart();

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
    update_chart(opts) {
      convertDynamicProperties(this.options, true);
      this.chart.setOption(this.options, opts ?? { notMerge: this.chart.options?.series.length != this.options.series.length });
    },


    echarts_on(eventName, query, callbackId) {
      this.chart.on(eventName, query, (e) => {
        const eventParams = {
          componentType: e.componentType,
          seriesType: e.seriesType,
          seriesIndex: e.seriesIndex,
          seriesName: e.seriesName,
          name: e.name,
          dataIndex: e.dataIndex,
          data: e.data,
          dataType: e.dataType,
          value: e.value,
          color: e.color,
        }

        this.$emit('event_on', { params: eventParams, callbackId })
      })
    },

    run_chart_method(name, ...args) {
      if (name.startsWith(":")) {
        name = name.slice(1);
        args = args.map((arg) => new Function("return " + arg)());
      }
      return this.chart[name](...args);
    },
  },
  props: {
    options: Object,
    theme: String | Object | undefined
  },
};
