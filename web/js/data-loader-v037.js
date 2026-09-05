(()=>{'use strict';
const BASE='../data/runtime-v037/';
let manifestPromise=null;const cache=new Map();
async function manifest(){
 if(!manifestPromise)manifestPromise=fetch(BASE+'manifest.json',{cache:'no-store'}).then(r=>{if(!r.ok)throw new Error('runtime manifest load failed');return r.json()});
 return manifestPromise;
}
async function gunzipJson(resp){
 if(!('DecompressionStream' in window))throw new Error('이 브라우저는 압축 데이터 로더를 지원하지 않습니다. 브라우저를 최신 버전으로 업데이트해 주세요.');
 const ds=new DecompressionStream('gzip');
 const stream=resp.body.pipeThrough(ds);
 const text=await new Response(stream).text();
 return JSON.parse(text);
}
async function load(key){
 if(cache.has(key))return cache.get(key);
 const p=(async()=>{const m=await manifest(),meta=m.files?.[key];if(!meta)throw new Error('runtime key not found: '+key);const r=await fetch(BASE+meta.file,{cache:'no-store'});if(!r.ok)throw new Error(key+' load failed');return meta.compression==='gzip'?gunzipJson(r):r.json()})();
 cache.set(key,p);return p;
}
function clear(){cache.clear();manifestPromise=null}
window.SWBattleCatsDataLoaderV037={load,manifest,clear};
})();
