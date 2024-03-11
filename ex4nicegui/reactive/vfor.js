export default {
    props: { itemIds: Array },

    render() {
        // debugger
        const slotBox = this.$slots.default()
        console.log(slotBox, this.itemIds);

        const slots = this.itemIds.map(({ elementId }) => {
            return slotBox.find(v => v.key === elementId)
        });

        console.log(slots);

        return slots
    }
}