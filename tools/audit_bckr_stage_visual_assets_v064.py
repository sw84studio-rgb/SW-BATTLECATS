#!/usr/bin/env python3
from pathlib import Path
import argparse,json,gzip,hashlib,sys

IMAGE_SIGS={
 '.png':lambda b:b.startswith(b'\x89PNG\r\n\x1a\n'),
 '.jpg':lambda b:b.startswith(b'\xff\xd8\xff'),
 '.jpeg':lambda b:b.startswith(b'\xff\xd8\xff'),
 '.webp':lambda b:len(b)>=12 and b[:4]==b'RIFF' and b[8:12]==b'WEBP',
}
RELEVANT_EXT={'.png','.jpg','.jpeg','.webp','.imgcut','.mamodel','.maanim','.pack','.list','.bcuzip'}
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for c in iter(lambda:f.read(1024*1024),b''):h.update(c)
 return h.hexdigest()
def load_plan(path):
 if path.suffix=='.jgz': return json.loads(gzip.open(path,'rt',encoding='utf-8').read())
 return json.loads(path.read_text('utf-8'))
def meta(p,root):
 ext=p.suffix.lower(); head=p.read_bytes()[:16]
 sig=None
 if ext in IMAGE_SIGS: sig=bool(IMAGE_SIGS[ext](head))
 return {'path':p.relative_to(root).as_posix(),'basename':p.name,'bytes':p.stat().st_size,'sha256':sha(p),'extension':ext,'signature_ok':sig}
def main():
 ap=argparse.ArgumentParser(description='Inventory already obtained/extracted BCKR stage visual assets. No decryption and no auto-promotion.')
 ap.add_argument('root',help='Extracted/decrypted asset directory or directory containing pack/list files')
 ap.add_argument('--plan',default=str(Path(__file__).resolve().parents[1]/'data/runtime-v064/stageBinaryAcquisitionPlan.jgz'))
 ap.add_argument('--out',default='V064_LOCAL_STAGE_BINARY_SCAN.json')
 a=ap.parse_args(); root=Path(a.root).resolve(); plan=load_plan(Path(a.plan).resolve())
 if not root.is_dir(): raise SystemExit('root directory not found: '+str(root))
 files=[p for p in root.rglob('*') if p.is_file() and (p.suffix.lower() in RELEVANT_EXT or p.name.lower().endswith('.asset.bcuzip'))]
 byname={}
 for p in files: byname.setdefault(p.name.lower(),[]).append(p)
 bg=[]
 for x in plan['p1_backgrounds']:
  main_names=x.get('reference_main_image_candidates') or []
  effect_names=[c['file'] for c in x.get('kr_effect_definition',{}).get('components',[])]
  hits=[]
  for role,names in [('PUBLIC_MAIN_FILENAME_CANDIDATE',main_names),('KR_EFFECT_EXACT_FILENAME',effect_names)]:
   for n in names:
    for p in byname.get(n.lower(),[]): hits.append({'role':role,**meta(p,root)})
  bg.append({'background_id':x['background_id'],'expected_main_names':main_names,'expected_effect_names':effect_names,
             'hits':hits,'state':'FOUND_REQUIRES_PROVENANCE_REVIEW' if hits else ('NO_FILENAME_RULE_DO_NOT_GUESS' if not main_names and not effect_names else 'NOT_FOUND')})
 packs=[meta(p,root) for p in files if p.suffix.lower() in {'.pack','.list','.bcuzip'} or p.name.lower().endswith('.asset.bcuzip')]
 out={'schema':'sw_battlecats_local_stage_binary_scan_v064','root':str(root),'plan_version':plan['version'],
      'promotion_allowed':False,'reason':'This tool inventories filename/signature/hash only. BCKR 15.5.0 provenance and ID mapping still require review.',
      'inventory':{'relevant_files':len(files),'pack_or_list_files':len(packs),'pack_or_list':packs},
      'p1_backgrounds':bg,
      'p1_enemy_bases':[{'enemy_base_id':x['enemy_base_id'],'state':'MAPPING_NOT_ATTEMPTED_NO_VERIFIED_FILENAME_RULE'} for x in plan['p1_enemy_bases']],
      'summary':{'background_ids_with_hits':sum(bool(x['hits']) for x in bg),'enemy_base_ids_mapped':0}}
 Path(a.out).write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(out['summary'],ensure_ascii=False)); print('report:',Path(a.out).resolve())
if __name__=='__main__': main()
