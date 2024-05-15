import { convertDynamicProperties } from "../../static/utils/dynamic_properties.js";

function collectMapRegisterTask() {
  const tasks = new Map();

  if (typeof window.ex4ngEchartsMapTasks !== "undefined") {

    for (const [mapName, src] of window.ex4ngEchartsMapTasks.entries()) {

      const registerPromise = new Promise((resolve, reject) => {
        fetch(src)
          .then((response) => response.json())
          .then((data) => {
            echarts.registerMap(mapName, data);
            resolve();
          });

      });

      tasks.set(mapName, registerPromise);
    }
  }

  return tasks;
}

const mapRegisterTasks = collectMapRegisterTask();

export default {
  template: "<div></div>",
  async mounted() {
    await this.$nextTick(); // wait for Tailwind classes to be applied
    await Promise.all(Array.from(mapRegisterTasks.values()));

    this.chart = echarts.init(this.$el, this.theme);

    this.resizeObs = new ResizeObserver(this.chart.resize)

    // Prevent interruption of chart animations due to resize operations.
    // It is recommended to register the callbacks for such an event before setOption.
    const createResizeObserver = () => {
      this.resizeObs.observe(this.$el);
      this.chart.off("finished", createResizeObserver);
    };
    this.chart.on("finished", createResizeObserver);

    if (this.options) {
      this.update_chart();
    } else {
      const fn = new Function('return ' + this.code)()
      fn(this.chart)
      this.$emit("__update_options_from_client", this.chart.getOption())
    }
    this.chart.getZr().on("click", (e) => {
      if (!e.target) {
        this.$emit("clickBlank")
      }
    });

  },
  beforeDestroy() {
    this.chart.dispose();
    this.resizeObs.unobserve();
  },
  beforeUnmount() {
    this.chart.dispose();
    this.resizeObs.unobserve();
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
        };

        this.$emit('event_on', { params: eventParams, callbackId });
      });


    },

    run_chart_method(name, ...args) {
      if (name.startsWith(":")) {
        name = name.slice(1);
        args = args.map((arg) => new Function("return " + arg)());
      }
      return runMethod(this.chart, name, args);
    },
  },
  props: {
    options: Object | undefined,
    theme: String | Object | undefined,
    code: String | undefined,
  },
};
