export default {
    template: `<span v-html="content"></span>`,

    props: {
        content: String,
    },
};