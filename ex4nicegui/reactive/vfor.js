const { h, TransitionGroup } = Vue;

export default {
    props: { itemIds: Array, transitionProps: Object },
    render() {
        const is_transition = !!this.transitionProps;
        const slotBox = this.$slots.default()
        const slots = this.itemIds.map(({ elementId }) => {
            return slotBox.find(v => v.key === elementId)
        });

        return is_transition ? h(TransitionGroup, { ...this.transitionProps }, slots) : slots;
    }
}