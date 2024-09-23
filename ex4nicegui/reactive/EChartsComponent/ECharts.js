import 'echarts'
import { convertDynamicProperties } from "../../static/utils/dynamic_properties.js";

function collectMapRegisterTask() {
  const tasks = new Map();

  if (typeof window.ex4ngEchartsMapTasks !== "undefined") {

    for (const [mapName, opt] of window.ex4ngEchartsMapTasks.entries()) {
      const { src, type: mapDataType, specialAreas } = opt;
      const registerPromise = new Promise((resolve, reject) => {
        fetch(src)
          .then((response) => {
            if (mapDataType === "genJSON") {
              return response.json();
            }

            return response.text();
          })
          .then((data) => {
            if (mapDataType === "svg") {
              data = { svg: data }
            }

            echarts.registerMap(mapName, data, specialAreas);
            resolve();
          });

      });

      tasks.set(mapName, registerPromise);
    }
  }

  return tasks;
}

function hasMapOrGeo(options) {
  if (options) {
    const hasMapSeries = options.series && Array.isArray(options.series) &&
      options.series.some(seriesItem =>
        seriesItem.type === 'map' ||
        seriesItem.type === 'lines'
      );

    const hasGeoConfig = options.geo && (typeof options.geo === 'object' || Array.isArray(options.geo));

    return hasMapSeries || hasGeoConfig;
  }
  return false;
}

const mapRegisterTasks = collectMapRegisterTask();

export default {
  template: "<div></div>",
  async mounted() {
    await new Promise((resolve) => setTimeout(resolve, 0)); // wait for Tailwind classes to be applied
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
      if (hasMapOrGeo(this.options)) {
        await Promise.all(Array.from(mapRegisterTasks.values()));
      }
      this.update_chart();
    } else {
      const fn = new Function('return ' + this.code)()
      await Promise.all(Array.from(mapRegisterTasks.values()));
      fn(this.chart, echarts)
      this.$emit("__update_options_from_client", this.chart.getOption())
    }
    this.chart.getZr().on("click", (e) => {
      if (!e.target) {
        this.$emit("clickBlank")
      }
    });

    // 
    await new Promise((resolve) => setTimeout(resolve, 0));
    this.$emit("_chartsCreated")
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

    echarts_on(eventName, query) {
      this.chart.on(eventName.replace(/^chart:/, ''), query, (e) => {
        this.$emit(eventName, e);
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
