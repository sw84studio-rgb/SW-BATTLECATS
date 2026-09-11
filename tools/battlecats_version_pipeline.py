#!/usr/bin/env python3
from __future__ import annotations
import argparse, copy, gzip, json, re, sys, urllib.request
from datetime import datetime, timezone
from pathlib import Path

UA='SW-BattleCats-Version-Pipeline/1.0'
def now(): return datetime.now(timezone.utc).isoformat()
def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def save(p,d):
    p=Path(p); p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def get_json(url):
    req=urllib.request.Request(url,headers={'User-Agent':UA,'Accept':'application/json'})
    with urllib.request.urlopen(req,timeout=30) as r: return json.load(r)
def baseline_id(appv,datav,stamp=None):
    stamp=stamp or datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')
    return f'KR{appv}_DATA{datav}_{stamp}'
def current_versions(base):
    return {'kr_ios_stable':str(base['kr_ios']['stable']),'project_data_version':str(base['project_data']['stable'])}
def detect(base):
    cur=current_versions(base); detected=dict(cur); warnings=[]
    try:
        payload=get_json(base['kr_ios']['watch_url'])
        rows=payload.get('results') or []
        if rows:
            v=str(rows[0].get('version','')).strip()
            if v: detected['kr_ios_stable']=v
    except Exception as e: warnings.append('KR iOS stable detection failed: '+repr(e))
    changes=[{'kind':k,'from':cur.get(k,''),'to':v} for k,v in detected.items() if str(cur.get(k,''))!=str(v)]
    return {'checked_at':now(),'baseline':cur,'detected':detected,'changes':changes,'changed':bool(changes),'warnings':warnings}
def runtime_summary(repo):
    out={'runtime_manifest':None,'counts':{},'protected_checks':{}}
    manifests=sorted((repo/'data').glob('runtime-v*/manifest.json'))
    if not manifests: return out
    def vernum(p):
        m=re.search(r'runtime-v(\d+)',str(p)); return int(m.group(1)) if m else -1
    mp=max(manifests,key=vernum); out['runtime_manifest']=str(mp.relative_to(repo))
    m=load(mp); base=mp.parent
    for key,meta in (m.get('files') or {}).items():
        f=base/meta.get('file','')
        try:
            raw=gzip.open(f,'rt',encoding='utf-8').read() if meta.get('compression')=='gzip' or f.suffix=='.jgz' else f.read_text(encoding='utf-8')
            d=json.loads(raw)
            if isinstance(d,list): out['counts'][key]=len(d)
            elif isinstance(d,dict):
                for candidate in ('items','entries','records','cats','enemies','stages'):
                    if isinstance(d.get(candidate),list): out['counts'][key]=len(d[candidate]); break
                else: out['counts'][key]=len(d)
            if key=='cats': out['protected_checks']['unit673_chita']=('치타' in raw)
        except Exception as e: out['counts'][key]={'error':repr(e)}
    return out
def candidate(base,selected,dr,summary,mode):
    cur=current_versions(base)
    changes=[{'kind':k,'from':cur.get(k,''),'to':v} for k,v in selected.items() if str(cur.get(k,''))!=str(v)]
    return {
      'schema_version':1,'state':'review_required','mode':mode,'created_at':now(),
      'base_baseline_id':base.get('baseline_id'),'current':cur,'selected':selected,'version_changes':changes,
      'detection':dr,'repository_summary':summary,
      'automatic_classification':{
        'auto_safe':['baseline metadata','candidate/report generation','runtime inventory audit'],
        'review_required':['Korean names','acquisition/stage links','trait mappings/icons','gacha classifications','descriptions','runtime replacement']
      },
      'approval_gate':{'required':True,'message':'검수 후 approve/apply-selected에서만 기준 버전을 확정합니다. runtime 데이터는 자동 덮어쓰지 않습니다.'}
    }
def snapshot(base): return {'saved_at':now(),'baseline':copy.deepcopy(base)}
def append_history(path,base):
    h=load(path) if Path(path).exists() else {'schema_version':1,'history':[]}; hist=h.setdefault('history',[])
    bid=base.get('baseline_id')
    if not hist or hist[-1].get('baseline',{}).get('baseline_id')!=bid: hist.append(snapshot(base))
    h['history']=hist[-30:]; save(path,h)
def approve(base_path,history_path,candidate_path,confirm):
    base=load(base_path); cand=load(candidate_path)
    if cand.get('state')!='review_required': raise SystemExit('candidate is missing or not review_required')
    if not confirm: raise SystemExit('--confirm-reviewed is required')
    append_history(history_path,base); sel=cand['selected']; old=base.get('baseline_id')
    base['kr_ios']['stable']=sel['kr_ios_stable']; base['project_data']['stable']=sel['project_data_version']
    base['baseline_id']=baseline_id(sel['kr_ios_stable'],sel['project_data_version']); base['approved_at']=now(); base['checked_at']=now(); base['previous_baseline_id']=old; base['approval_state']='approved'
    save(base_path,base); cand['state']='approved'; cand['approved_at']=now(); cand['approved_baseline_id']=base['baseline_id']; save(candidate_path,cand); return base
def restore(base_path,history_path,target_id=None):
    base=load(base_path); h=load(history_path); hist=h.get('history',[])
    if not hist: raise SystemExit('version history is empty')
    idx=None
    if target_id:
        for i,x in enumerate(hist):
            if x.get('baseline',{}).get('baseline_id')==target_id: idx=i
        if idx is None: raise SystemExit('target baseline id not found')
    else: idx=len(hist)-1
    target=copy.deepcopy(hist[idx]['baseline']); hist.pop(idx); hist.append(snapshot(base)); h['history']=hist[-30:]; save(history_path,h)
    target['restored_at']=now(); target['approval_state']='approved'; target['restored_from']=base.get('baseline_id'); save(base_path,target); return target

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('mode',choices=['detect','rerun-current','rerun-selected','approve','restore','status'])
    ap.add_argument('--repo',default='.'); ap.add_argument('--baseline',default='data/version-baseline.json'); ap.add_argument('--history',default='data/version-history.json'); ap.add_argument('--candidate',default='data/version-candidate.json'); ap.add_argument('--report-dir',default='reports/version-pipeline')
    ap.add_argument('--kr-ios'); ap.add_argument('--project-data-version'); ap.add_argument('--confirm-reviewed',action='store_true'); ap.add_argument('--target-baseline-id')
    a=ap.parse_args(); repo=Path(a.repo).resolve(); bp=repo/a.baseline; hp=repo/a.history; cp=repo/a.candidate; rp=repo/a.report_dir; rp.mkdir(parents=True,exist_ok=True); base=load(bp)
    if a.mode=='status': print(json.dumps({'baseline':base,'history':load(hp),'candidate':load(cp)},ensure_ascii=False,indent=2)); return 0
    if a.mode=='detect':
        out=detect(base); save(rp/'version-detect.json',out); print(json.dumps(out,ensure_ascii=False)); return 2 if out['changed'] else 0
    if a.mode in ('rerun-current','rerun-selected'):
        dr=detect(base); sel=current_versions(base)
        if a.mode=='rerun-selected':
            if a.kr_ios: sel['kr_ios_stable']=a.kr_ios
            elif dr['detected'].get('kr_ios_stable'): sel['kr_ios_stable']=dr['detected']['kr_ios_stable']
            if a.project_data_version: sel['project_data_version']=a.project_data_version
        out=candidate(base,sel,dr,runtime_summary(repo),a.mode); save(cp,out); save(rp/'version-rerun-result.json',out); print(json.dumps(out,ensure_ascii=False)); return 0
    if a.mode=='approve': print(json.dumps({'approved':True,'baseline':approve(bp,hp,cp,a.confirm_reviewed)},ensure_ascii=False)); return 0
    if a.mode=='restore': print(json.dumps({'restored':True,'baseline':restore(bp,hp,a.target_baseline_id)},ensure_ascii=False)); return 0
    return 1
if __name__=='__main__': raise SystemExit(main())
