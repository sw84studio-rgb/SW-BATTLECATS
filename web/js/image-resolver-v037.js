(()=>{'use strict';
let enemyMap=new Map();
function init(enemyData){enemyMap=new Map((enemyData?.mappings||[]).map(x=>[x.canonical_id,x]));}
function catUrl(entryId){const m=/^cat:(\d+):(\d+)$/.exec(entryId||'');if(!m)return null;return `https://battlecatsinfo.github.io/img/u/${m[1]}/${Number(m[2])-1}.png`;}
function resolve(entryId){
 const cu=catUrl(entryId);if(cu)return {src:cu,kind:'remote',provider:'battlecatsinfo_public_img',verification:'PUBLIC_REPO_UNIT_PATH_PATTERN_VERIFIED'};
 const em=enemyMap.get(entryId);if(em?.remote_path)return {src:'https://battlecatsinfo.github.io/img/'+em.remote_path,kind:'remote',provider:em.provider_id||'battlecatsinfo_public_img',verification:em.verification_status};
 return null;
}
window.SWBattleCatsImageResolverV037={init,resolve};
})();
