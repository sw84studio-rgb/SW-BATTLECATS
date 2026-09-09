#!/usr/bin/env python3
"""SW BATTLECATS V067 - verify enemy_base_id -> enemyCastleDataLegend row-index coverage.
No image filename inference or asset promotion is performed.
"""
from __future__ import annotations
import argparse,gzip,json,re
from pathlib import Path
from collections import Counter

def parse_rows(path:Path):
    out=[]
    for idx,line in enumerate(path.read_text('utf-8',errors='replace').splitlines()):
        body=line.split('//',1)[0].strip().rstrip(',')
        vals=[x.strip() for x in body.split(',') if x.strip()]
        try: nums=[int(x) for x in vals]
        except: continue
        out.append({'row_index':idx,'values':nums,'raw_line':line})
    return out

def load_registry(path:Path):
    if path.suffix.lower()=='.jgz':
        with gzip.open(path,'rt',encoding='utf-8') as f:return json.load(f)
    return json.loads(path.read_text('utf-8'))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('raw_root',help='KR 15.5.0 extracted root containing DataLocal/enemyCastleDataLegend.csv')
    ap.add_argument('enemy_base_registry',help='enemyBaseRegistry.jgz/json')
    ap.add_argument('--p1',default='0,136,1,7,13,5,85,4,6,12,20,11,3,2,21')
    ap.add_argument('--out',default='V067_ENEMY_BASE_ROW_INDEX_AUDIT.json')
    a=ap.parse_args(); root=Path(a.raw_root).resolve(); regp=Path(a.enemy_base_registry).resolve()
    lp=root/'DataLocal/enemyCastleDataLegend.csv'
    if not lp.is_file(): raise SystemExit('missing '+str(lp))
    reg=load_registry(regp); ids=sorted(int(e['enemy_base_id']) for e in reg.get('entries',[]))
    rows=parse_rows(lp); rm={r['row_index']:r for r in rows}; p1=[int(x) for x in a.p1.split(',') if x.strip()]
    report={
      'schema':'sw_battlecats_enemy_base_row_index_audit_v067','promotion_allowed':False,
      'summary':{'registry_ids':len(ids),'id_min':min(ids) if ids else None,'id_max':max(ids) if ids else None,'legend_rows':len(rows),'all_ids_covered':all(i in rm for i in ids),'p1_all_covered':all(i in rm for i in p1)},
      'missing_registry_ids':[i for i in ids if i not in rm],
      'p1_rows':[{'enemy_base_id':i,'legend_row':rm.get(i)} for i in p1],
      'column_counts':dict(Counter(len(r['values']) for r in rows)),
      'guardrail':'Row-index coverage is structural evidence only. enemyCastleDataLegend contains no image/model filenames, so filename inference and web promotion remain forbidden.'
    }
    Path(a.out).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report['summary'],ensure_ascii=False)); print('report:',Path(a.out).resolve())
if __name__=='__main__':main()
