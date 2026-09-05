(()=>{'use strict';
const DATA_BASE='../data/';
const FILES={cat_form:'encyclopedia-cats-v030.json',enemy:'encyclopedia-enemies-v030.json',stage:'encyclopedia-stages-v030.json'};
const state={index:[],category:'all',query:'',cache:new Map(),current:null,history:[],strategy:null,deckMode:'all'};
const $=s=>document.querySelector(s),list=$('#entryList'),catalog=$('#catalogView'),detail=$('#detailView');
const esc=s=>String(s??'').replace(/[&<>"]/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[m]));
const {fieldKind,spans}=window.SWBattleCatsLayoutV030,IR=window.SWBattleCatsImageResolverV032,Deck=window.SWBattleCatsDeckEngineV034,Roster=window.SWBattleCatsRosterV035;
async function loadIndex(){
  await IR.load();
  const [a,b]=await Promise.all([fetch(DATA_BASE+'encyclopedia-index-v030.json',{cache:'no-store'}),fetch(DATA_BASE+'strategy-runtime-v034.json',{cache:'no-store'})]);
  if(!a.ok||!b.ok)throw new Error('data load failed');
  state.index=(await a.json()).entries;state.strategy=await b.json();Deck.init(state.strategy);renderList();
}
async function loadCategory(cat){if(state.cache.has(cat))return state.cache.get(cat);const r=await fetch(DATA_BASE+FILES[cat],{cache:'no-store'});if(!r.ok)throw new Error(cat+' load failed');const d=await r.json(),m=new Map(d.entries.map(e=>[e.entry_id,e]));state.cache.set(cat,m);return m}
function imageBox(id,name,cls){const hit=IR.resolve(id);if(hit)return `<img class="${cls}" src="${esc(hit.src)}" alt="${esc(name)}" loading="lazy">`;return `<div class="${cls} image-pending">이미지<br>준비 중</div>`}
function categoryName(c){return c==='cat_form'?'캐릭터':c==='enemy'?'적':'스테이지'}
function renderList(){const q=state.query.trim().toLowerCase();let rows=state.index.filter(x=>(state.category==='all'||x.category===state.category)&&(!q||(x.name_ko+' '+x.keywords+' '+x.subtitle).toLowerCase().includes(q)));rows=rows.slice(0,500);$('#resultCount').textContent=rows.length+(rows.length===500?'+':'');list.innerHTML=rows.length?rows.map(x=>`<button class="entry-card" type="button" data-entry="${esc(x.entry_id)}" data-category="${esc(x.category)}">${imageBox(x.entry_id,x.name_ko,'entry-thumb')}<div><b>${esc(x.name_ko)}</b><small>${esc(x.subtitle||categoryName(x.category))}</small></div></button>`).join(''):'<div class="empty">검색 결과가 없습니다.</div>'}
async function openEntry(id,cat,push=true){const map=await loadCategory(cat),e=map.get(id);if(!e)return;if(push&&state.current)state.history.push(state.current);state.current={id,cat};catalog.hidden=true;detail.hidden=false;detail.innerHTML=detailHtml(e);bindDetail(e);window.scrollTo({top:0,behavior:'auto'})}
function standardSections(e){return e.sections.map(g=>{const sm=spans(g.fields);return `<section class="info-group"><h2 class="info-group-title">${esc(g.title)}</h2><div class="info-grid">${g.fields.map((f,i)=>{const sp=sm[i]||6,links=(f.links||[]).map(l=>`<button class="info-link" type="button" data-open="${esc(l.entry_id)}">${esc(l.label)}</button>`).join('');return `<div class="info-cell span-${sp}"><div class="info-label">${esc(f.label)}</div><div class="info-value">${esc(f.value)}${links?`<div class="info-links">${links}</div>`:''}</div></div>`}).join('')}</div></section>`}).join('')}
function rosterControl(e){if(e.category!=='cat_form')return'';const u=e.classification.unit_id,f=e.classification.form_no,owned=Roster.isOwned(u,f);return `<div class="hero-actions"><button class="roster-btn ${owned?'owned':''}" type="button" data-roster-unit="${u}" data-roster-form="${f}">${owned?'보유 등록됨 · 해제':'이 형태까지 보유 등록'}</button></div>`}
function deckPanel(e){
  if(e.category!=='stage')return'';
  const sid=e.classification.stage_native_id,owned=state.deckMode==='owned'?Roster.read():null,d=Deck.recommend(sid,{owned});
  const cards=d.slots.map(x=>`<button class="deck-card" type="button" data-open="${esc(x.entry_id)}">${imageBox(x.entry_id,x.name_ko,'deck-thumb')}<div class="deck-slot">#${x.slot} · ${esc(x.role_ko)}</div><b>${esc(x.name_ko)}</b><small>비용 ${esc(x.stats.cost)} · 사거리 ${esc(x.stats.range)}</small><p>${esc(x.reasons.slice(0,2).join(' / '))}</p></button>`).join('');
  const shortage=d.status==='INSUFFICIENT_ROSTER'?`<div class="deck-warning">보유 등록 캐릭터가 부족해 ${10-d.slots.length}칸이 비었습니다. 전체 기준으로 전환하면 10칸 추천을 볼 수 있습니다.</div>`:'';
  return `<section class="deck-panel"><div class="deck-head"><div><h2>추천 편성 10칸</h2><p>공식 공략 공식이 아닌 KR15.5 데이터 기반 추천입니다.</p></div><div class="deck-mode"><button type="button" data-deck-mode="all" class="${state.deckMode==='all'?'active':''}">전체 기준</button><button type="button" data-deck-mode="owned" class="${state.deckMode==='owned'?'active':''}">보유만 (${Roster.count()})</button></div></div>${shortage}<div class="deck-grid">${cards}</div></section>`;
}
function detailHtml(e){const hero=`<div class="detail-hero"><div class="hero-image">${imageBox(e.entry_id,e.names.ko,'hero-img')}</div><div class="hero-copy"><h1>${esc(e.names.ko)}</h1>${e.names.ja?`<div class="ja">${esc(e.names.ja)}</div>`:''}<div class="type">${esc(e.ui_category)}</div>${rosterControl(e)}</div></div>`;const rel=(e.relations||[]).length?`<div class="relation-row">${e.relations.map(r=>`<button type="button" data-open="${esc(r.entry_id)}">${esc(r.label)}</button>`).join('')}</div>`:'';return hero+`<div class="detail-sections">${standardSections(e)}</div>`+deckPanel(e)+rel}
function catFromId(id){if(id.startsWith('cat:'))return'cat_form';if(id.startsWith('enemy:'))return'enemy';return'stage'}
function bindDetail(e){
  detail.querySelectorAll('[data-open]').forEach(b=>b.addEventListener('click',()=>openEntry(b.dataset.open,catFromId(b.dataset.open))));
  const rb=detail.querySelector('[data-roster-unit]');if(rb)rb.addEventListener('click',()=>{const u=Number(rb.dataset.rosterUnit),f=Number(rb.dataset.rosterForm);if(Roster.isOwned(u,f))Roster.remove(u);else Roster.setOwned(u,f);detail.innerHTML=detailHtml(e);bindDetail(e)});
  detail.querySelectorAll('[data-deck-mode]').forEach(b=>b.addEventListener('click',()=>{state.deckMode=b.dataset.deckMode;detail.innerHTML=detailHtml(e);bindDetail(e)}));
}
function showCatalog(){state.current=null;detail.hidden=true;catalog.hidden=false;renderList();window.scrollTo({top:0,behavior:'auto'})}
list.addEventListener('click',e=>{const b=e.target.closest('[data-entry]');if(b)openEntry(b.dataset.entry,b.dataset.category)});
$('#searchInput').addEventListener('input',e=>{state.query=e.target.value;renderList()});
$('#categoryTabs').addEventListener('click',e=>{const b=e.target.closest('[data-category]');if(!b)return;state.category=b.dataset.category;document.querySelectorAll('#categoryTabs button').forEach(x=>x.classList.toggle('active',x===b));renderList()});
document.querySelectorAll('[data-action]').forEach(b=>b.addEventListener('click',()=>{const a=b.dataset.action;if(a==='encyclopedia'||a==='home'){state.history=[];showCatalog();window.dispatchEvent(new CustomEvent('swbattlecats:'+a,{detail:state.current}))}else if(a==='back'){if(state.history.length){const p=state.history.pop();openEntry(p.id,p.cat,false)}else showCatalog()}}));
window.addEventListener('swbattlecats:roster-changed',()=>{if(state.current?.cat==='stage')openEntry(state.current.id,'stage',false)});
loadIndex().catch(err=>{list.innerHTML='<div class="empty">데이터를 불러오지 못했습니다.<br>HTTP 서버에서 실행해 주세요.</div>';console.error(err)});
window.SWBattleCatsEncyclopediaV035={openEntry,showCatalog,fieldKind,spans};
})();