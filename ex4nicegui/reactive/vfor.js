/**
         return h(
                Vue.TransitionGroup,
                {
                    tag: 'div',
                    name: 'list',
                    // css: false,
                    // ...this.transitionGroupArgs
                },
                this.$slots.default().map((slot, index) => {
                    slot.props.key = this.childOrderKey[index]
                    return slot
                })
            )
 */


export default {
    props: {
        childOrderKey: Array,
        applyTransitionGroup: Boolean,
        transitionGroupArgs: Array,
    },
    data() {
        return {
        }
    },
    render() {
        const h = Vue.h
        const slots = this.$slots.default()
        if (this.applyTransitionGroup) {

            console.log(slots);

            return h(
                Vue.TransitionGroup,
                {
                    tag: 'span',
                    name: 'list',
                    // css: false,
                    // ...this.transitionGroupArgs
                },
                slots.map((slot, index) => {
                    slot.props.key = this.childOrderKey[index]
                    return slot
                })
            )
        }

        return slots
    }
}