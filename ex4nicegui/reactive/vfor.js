const { h, TransitionGroup } = Vue;

export default {
    props: { itemIds: Array },

    render() {
        const slotBox = this.$slots.default()
        const slots = this.itemIds.map(({ elementId }) => {
            return slotBox.find(v => v.key === elementId)
        });

        console.log('solts:', slots, 'itemIds:', this.itemIds);

        return h(TransitionGroup, { name: 'list' }, slots)
    }
}