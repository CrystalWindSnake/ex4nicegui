export default {
    props: {
        // childOrderKey: Array,
        // transitionGroupArgs: Array,
    },
    data() {
        return {
        }
    },
    mounted() {
    },
    render() {
        // debugger
        const h = Vue.h
        const vfgt = Vue.Fragment
        const slotBox = this.$slots.default()
        console.log('tg:', slotBox);
        const wrap = () => [h(vfgt, slotBox)]
        // const wrap = slotBox
        console.log(wrap);


        // slotBox[0].children = this.childOrderKey.map(idx => {
        //     return slotBox[0].children[idx]
        // })
        // console.log(slots);

        return h(
            Vue.TransitionGroup,
            {
                tag: 'span',
                name: 'list',
                // css: false,
                // ...this.transitionGroupArgs
            }, wrap
        )

    }
}