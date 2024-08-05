const { h, TransitionGroup } = Vue;

export default {
    props: { itemIds: Array, transitionProps: Object },
    render() {
        const is_transition = !!this.transitionProps;
        const slotBox = this.$slots.default()
        const slots = this.itemIds.map(({ elementId }) => {
            return slotBox.find(v => v.key === elementId)
        });

        function beforeLeave(el) {
            const { marginLeft, marginTop, width, height } = window.getComputedStyle(el)
            console.log('beforeLeave');
            el.style.left = `${el.offsetLeft - parseFloat(marginLeft, 10)}px`
            el.style.top = `${el.offsetTop - parseFloat(marginTop, 10)}px`
            el.style.width = width
            el.style.height = height
        }

        return is_transition ? h(TransitionGroup, { ...this.transitionProps, onBeforeLeave: beforeLeave }, slots) : slots;
    }
}