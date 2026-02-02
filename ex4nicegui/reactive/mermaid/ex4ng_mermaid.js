import { mermaid } from "nicegui-mermaid";
import { select as d3Select } from "d3-selection";
import { zoom as d3Zoom, zoomIdentity } from "d3-zoom";


let is_running = false;
const queue = [];

export default {
  template: `<div></div>`,
  data: () => ({
    last_content: "",
  }),
  mounted() {
    // 
    let content = this.content


    if (this.clickableNodes.length > 0) {
      // The event triggered by mermaid must be global, but there may be multiple mermaid components on the page.
      // Therefore, we need a unique function name for each component scenario.
      const actionCallback = `mermaid_${this.currentId}_action`

      const actionStem = this.clickableNodes.map(n => `click ${n} ${actionCallback}`).join('\n')
      content = [content, actionStem].join('\n')

      window[actionCallback] = (nodeId) => {
        this.$emit('onNodeClick', { nodeId })
      }

      this.actionCallback = actionCallback
    }

    this.update(content);
  },
  unmounted() {
    if (this.actionCallback && window[this.actionCallback]) {
      delete window[this.actionCallback]
    }
  },
  methods: {
    async update(content) {
      if (this.last_content === content) return;
      this.last_content = content;
      this.$el.innerHTML = content;
      this.$el.removeAttribute("data-processed");
      queue.push(this.$el);
      if (is_running) return;
      is_running = true;

      // startOnLoad prevents auto-execution of run, and securityLevel: 'loose' is required to execute click events.
      mermaid.initialize({ startOnLoad: false, securityLevel: 'loose' });
      while (queue.length) {
        await mermaid.run({ nodes: [queue.shift()] });
      }
      is_running = false;

      if (this.zoomMode) {
        const svg = d3Select(this.$el).select('svg')
        const zoomBox = svg.select('g.root')

        var zoom = d3Zoom().on("zoom", function ({ transform }) {
          zoomBox.attr("transform", transform);
        });

        svg.call(zoom);

        svg.on('dblclick.zoom', () => {
          svg.transition().duration(750).call(zoom.transform, zoomIdentity);
        })
      }
    }
  },
  props: {
    content: String,
    currentId: String,
    clickableNodes: Array,
    zoomMode: Boolean
  },
};
