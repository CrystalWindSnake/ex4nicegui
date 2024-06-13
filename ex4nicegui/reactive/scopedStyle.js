
const REGEX_NEWLINE = /[\r\n]/g;
const REGEX_START_SPACES = /^\s+/gm;

function getClasses(id) {
    return `ex4ng-scoped-style-${id}`;
}

function removeInvalidChars(str) {
    str = str.replace(REGEX_START_SPACES, '');
    return str.replace(REGEX_NEWLINE, '');
}


export default {
    template: `<template></template>`,


    methods: {
        createStyle(id, css) {
            const classes = getClasses(id);
            const target = document.querySelector(`style.${classes}`);
            css = removeInvalidChars(css);
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