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
  },
  props: {
    options: Object,
    theme: String | Object | undefined
  },
};
