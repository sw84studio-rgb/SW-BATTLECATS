(()=>{'use strict';
const state={map:new Map(),loaded:false};
const DATA_URL='../data/IMAGE_ASSET_MANIFEST_V032.json';
async function load(){if(state.loaded)return state.map;const r=await fetch(DATA_URL,{cache:'no-store'});if(!r.ok)throw new Error('image manifest load failed');const d=await r.json();state.map=new Map((d.assets||[]).map(x=>[x.entry_id,x]));state.loaded=true;return state.map}
function record(entryId){return state.map.get(entryId)||null}
function resolve(entryId,{allowRemote=false}={}){const x=record(entryId);if(!x)return null;if(x.available&&x.locked&&x.sha256&&x.local_path)return {src:x.local_path,kind:'local',record:x};if(allowRemote&&x.remote_url)return {src:x.remote_url,kind:'remote-preview',record:x};return null}
function candidate(entryId){const x=record(entryId);return x?{provider_id:x.provider_id,remote_path:x.remote_path,verification_status:x.verification_status}:null}
window.SWBattleCatsImageResolverV032={load,record,resolve,candidate,_setForTest(items){state.map=new Map(items.map(x=>[x.entry_id,x]));state.loaded=true}};
})();
