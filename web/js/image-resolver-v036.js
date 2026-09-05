(()=>{'use strict';
const state={explicit:new Map(),loaded:false};
const BASE='https://battlecatsinfo.github.io/img/';
async function load(){if(state.loaded)return;await window.SWBattleCatsImageResolverV032.load();try{const r=await fetch('../data/ENEMY_IMAGE_EXPLICIT_MAP_V031.json',{cache:'no-store'});if(r.ok){const d=await r.json();state.explicit=new Map((d.mappings||[]).map(x=>[x.entry_id,x]))}}catch{}state.loaded=true}
function resolve(entryId){const local=window.SWBattleCatsImageResolverV032.resolve(entryId);if(local)return local;let m=/^cat:(\d+):(\d+)$/.exec(entryId);if(m){return {src:`${BASE}u/${Number(m[1])}/${Number(m[2])-1}.png`,kind:'remote-verified-pattern',verification_status:'PUBLIC_REPO_UNIT_PATH_PATTERN_VERIFIED'}}const e=state.explicit.get(entryId);if(e?.remote_path)return {src:BASE+e.remote_path,kind:'remote-explicit',verification_status:e.verification_status};return null}
window.SWBattleCatsImageResolverV036={load,resolve};
})();
