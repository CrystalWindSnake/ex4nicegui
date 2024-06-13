
function getClasses(id) {
    return `ex4ng-scoped-style-${id}`;
}


export default {
    template: `<template></template>`,


    methods: {
        createStyle(id, css) {
            const classes = getClasses(id);
            const target = document.querySelector(`style.${classes}`);
            if (target) {
                target.innerHTML = css;
            } else {
                const style = document.createElement('style');
                style.classList.add(classes);
                style.innerHTML = css;
                document.head.appendChild(style);
            }
        },
        removeStyle(id) {
            const classes = getClasses(id);
            const target = document.querySelector(`style.${classes}`);
            if (target) {
                target.remove();
            }
        },
    },
};