(()=>{'use strict';
const KEY='swbattlecats:roster:v035';
let memory={};
function normalize(v){return v&&typeof v==='object'&&!Array.isArray(v)?v:{}}
function read(){try{const raw=localStorage.getItem(KEY);if(raw!=null){memory=normalize(JSON.parse(raw));return {...memory}}}catch{}return {...memory}}
function persist(v){memory={...normalize(v)};try{localStorage.setItem(KEY,JSON.stringify(memory))}catch{}try{window.dispatchEvent(new CustomEvent('swbattlecats:roster-changed',{detail:{...memory}}))}catch{}return {...memory}}
function setOwned(unitId,maxFormNo){const r=read(),k=String(unitId),n=Math.max(Number(maxFormNo)||1,Number(r[k])||0);r[k]=n;return persist(r)}
function remove(unitId){const r=read();delete r[String(unitId)];return persist(r)}
function isOwned(unitId,formNo=1){const r=read(),m=Number(r[String(unitId)]||0);return m>=Number(formNo)}
function count(){return Object.keys(read()).length}
function clear(){return persist({})}
const api={read,setOwned,remove,isOwned,count,clear,_resetMemoryForTest(){memory={}}};
if(typeof module!=='undefined'&&module.exports)module.exports=api;else window.SWBattleCatsRosterV035=api;
})();
