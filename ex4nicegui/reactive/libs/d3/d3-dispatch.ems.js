/**
 * Bundled by jsDelivr using Rollup v2.79.1 and Terser v5.19.2.
 * Original file: /npm/d3-dispatch@3.0.1/src/index.js
 *
 * Do NOT use SRI with dynamically generated files! More information: https://www.jsdelivr.com/using-sri-with-dynamic-files
 */
var n={value:()=>{}};function r(){for(var n,r=0,e=arguments.length,o={};r<e;++r){if(!(n=arguments[r]+"")||n in o||/[\s.]/.test(n))throw new Error("illegal type: "+n);o[n]=[]}return new t(o)}function t(n){this._=n}function e(n,r){for(var t,e=0,o=n.length;e<o;++e)if((t=n[e]).name===r)return t.value}function o(r,t,e){for(var o=0,i=r.length;o<i;++o)if(r[o].name===t){r[o]=n,r=r.slice(0,o).concat(r.slice(o+1));break}return null!=e&&r.push({name:t,value:e}),r}t.prototype=r.prototype={constructor:t,on:function(n,r){var t,i,l=this._,a=(i=l,(n+"").trim().split(/^|\s+/).map((function(n){var r="",t=n.indexOf(".");if(t>=0&&(r=n.slice(t+1),n=n.slice(0,t)),n&&!i.hasOwnProperty(n))throw new Error("unknown type: "+n);return{type:n,name:r}}))),f=-1,u=a.length;if(!(arguments.length<2)){if(null!=r&&"function"!=typeof r)throw new Error("invalid callback: "+r);for(;++f<u;)if(t=(n=a[f]).type)l[t]=o(l[t],n.name,r);else if(null==r)for(t in l)l[t]=o(l[t],n.name,null);return this}for(;++f<u;)if((t=(n=a[f]).type)&&(t=e(l[t],n.name)))return t},copy:function(){var n={},r=this._;for(var e in r)n[e]=r[e].slice();return new t(n)},call:function(n,r){if((t=arguments.length-2)>0)for(var t,e,o=new Array(t),i=0;i<t;++i)o[i]=arguments[i+2];if(!this._.hasOwnProperty(n))throw new Error("unknown type: "+n);for(i=0,t=(e=this._[n]).length;i<t;++i)e[i].value.apply(r,o)},apply:function(n,r,t){if(!this._.hasOwnProperty(n))throw new Error("unknown type: "+n);for(var e=this._[n],o=0,i=e.length;o<i;++o)e[o].value.apply(r,t)}};export{r as dispatch};export default null;
//# sourceMappingURL=/sm/75cc224f72e2b9915d579f2f2e560e1ac4b9bf901f3fc6431ea7165364174b7f.map