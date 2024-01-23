import { convertDynamicProperties } from "../../static/utils/dynamic_properties.js";


function retry(fn, options = {}) {

  options = {
    error: 'Maximum number of tries exceeded',
    tryMaxTimes: 5,
    intervalMs: 800,
    ...options
  }

  let tryTimes = 0
  let isDone = false

  const doneFn = () => {
    isDone = true
  }

  const task = setInterval(() => {
    tryTimes += 1

    if (tryTimes <= options.tryMaxTimes) {
      fn(doneFn)

      if (isDone) {
        clearInterval(task)
      }

    } else {
      console.error(options.error)
      clearInterval(task)
    }


  }, options.intervalMs);
}


export default {
  template: "<div></div>",
  mounted() {

    function initChart() {
      this.chart = echarts.init(this.$el, this.theme);
      this.update_chart();
      this.chart.getZr().on("click", (e) => {
        if (!e.target) {
          this.$emit("clickBlank")
        }
      });
      this.resizeObs = new ResizeObserver(this.chart.resize)
      this.resizeObs.observe(this.$el);
    }

    initChart = initChart.bind(this)

    retry((done) => {
      try {
        initChart()
        done()
      } catch (e) {
        if (e instanceof TypeError && e.message === `Cannot read properties of undefined (reading 'regions')`) {
          echarts.dispose(this.chart)
          return
        } else {
          clearInterval(tryInit)
          done()
          throw e;
        }
      }
    }, { error: 'Maximum number of retries echart init' })

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

      retry((done) => {
        if (this.chart) {

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

          done()
        }
      }, { error: 'Maximum number of retries on echarts event' })

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
