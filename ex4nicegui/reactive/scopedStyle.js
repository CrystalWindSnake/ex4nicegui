
const REGEX_NEWLINE = /[\r\n]/g;
const REGEX_START_SPACES = /^\s+/gm;

function getClasses(id) {
    return `ex4ng-scoped-style-${id}`;
}

function removeInvalidChars(str) {
    str = str.replace(REGEX_START_SPACES, '');
    return str.replace(REGEX_NEWLINE, '');
}

function appendCSS(styleElement, cssText) {
    // 获取已有的 CSS 内容
    let existingCSS = styleElement.textContent || '';

    // 如果已有的 CSS 内容不为空，添加一个空行作为分隔符
    if (existingCSS.trim() !== '') {
        existingCSS += '\n';
    }

    // 拼接新的 CSS 内容
    existingCSS += cssText;

    // 将新的 CSS 内容设置回 style 标签
    styleElement.textContent = existingCSS;
}

export default {
    template: `<template></template>`,
    methods: {
        createStyle(id, css) {
            css = removeInvalidChars(css);

            const classes = getClasses(id);
            const target = document.querySelector(`style.${classes}`);
            if (target) {
                appendCSS(target, css);
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