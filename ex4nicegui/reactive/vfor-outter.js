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
    mounted() {
        // const slots = this.$slots.default()



        // slots.forEach((slot, index) => {
        //     slot.props.key = this.childOrderKey[index]
        // })
        // console.log(this.$slots.default());
    },
    render() {
        // debugger
        const h = Vue.h
        const slotBox = this.$slots.default()
        if (this.applyTransitionGroup) {

            console.log(slotBox);

            slotBox[0].children = this.childOrderKey.map(idx => {
                return slotBox[0].children[idx]
            })
            // console.log(slots);

            return h(
                Vue.TransitionGroup,
                {
                    tag: 'span',
                    name: 'list',
                    // css: false,
                    // ...this.transitionGroupArgs
                }, slotBox
            )
        }

        return slotBox
    }
}