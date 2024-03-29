export default {
    props: { itemIds: Array },

    render() {
        const slotBox = this.$slots.default()

        const slots = this.itemIds.map(({ elementId }) => {
            return slotBox.find(v => v.key === elementId)
        });

        return slots
    }
}