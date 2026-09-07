(()=>{'use strict';
let entryMap=new Map(),itemMap=new Map();
function init(data){entryMap=new Map((data?.entries||[]).map(x=>[x.entry_id,x]));itemMap=new Map((data?.items||[]).map(x=>[String(x.item_id),x]));}
function resolve(entryId){const x=entryMap.get(entryId);if(!x?.local_path)return null;return {src:x.local_path,kind:'local',provider:'sw_battlecats_v038_assets',verification:x.source_class||'LOCAL_LOCKED',sha256:x.sha256||'',alias_of:x.alias_of||null};}
function resolveItem(itemId){const x=itemMap.get(String(itemId));if(!x?.local_path)return null;return {src:x.local_path,kind:'local',provider:'sw_battlecats_v038_assets',verification:x.source_class||'LOCAL_LOCKED',sha256:x.sha256||''};}
window.SWBattleCatsImageResolverV038={init,resolve,resolveItem};
})();
