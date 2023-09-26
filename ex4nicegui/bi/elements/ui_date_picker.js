export default {
    template: `
        <div :id="'cus-'+id" class="q-pa-md" style="max-width: 300px">
        <q-input filled v-model="value" mask="date" :rules="['date']">
        <template v-slot:append>
            <q-icon name="event" class="cursor-pointer">
            <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                <q-date v-model="value" >
                </q-date>
            </q-popup-proxy>
            </q-icon>
        </template>
        </q-input>
    </div>
    `,
    props: {
        id: String,
        date: String,
    },
    data() {
        return {
            value: this.date
        }
    },
    watch: {
        value(newValue) {
            this.$emit("update:value", newValue);
        },
    },
    computed: {
    },
    methods: {

    },
};
