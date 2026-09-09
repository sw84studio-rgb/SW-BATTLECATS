#!/usr/bin/env python3
"""SW BATTLECATS V066 - BCKR server download TSV / server file verifier.

This tool does NOT download, decrypt, or promote game assets.
It inventories download*.tsv files already present in an extracted KR package,
parses filename/size/MD5 rows, pairs .pack/.list files, and optionally verifies
already-obtained server files against those exact TSV fingerprints.
"""
from __future__ import annotations
import argparse, hashlib, json, re, sys
from collections import Counter, defaultdict
from pathlib import Path

SCHEMA="sw_battlecats_bckr_server_tsv_audit_v066"
MD5_RE=re.compile(r"^[0-9a-fA-F]{32}$")
TEXT_ENCODINGS=("utf-8-sig","utf-8","cp949","shift_jis","latin-1")

def md5_file(path:Path, chunk=1024*1024):
    h=hashlib.md5(); size=0
    with path.open('rb') as f:
        for b in iter(lambda:f.read(chunk),b''):
            size += len(b); h.update(b)
    return size,h.hexdigest()

def decode_text(path:Path):
    data=path.read_bytes()
    for enc in TEXT_ENCODINGS:
        try: return data.decode(enc),enc
        except UnicodeDecodeError: pass
    return data.decode('latin-1',errors='replace'),'latin-1-replace'

def is_valid_name(name:str):
    return bool(name) and not name.isdigit() and (not name or ord(name[0])!=65279)

def parse_tsv(path:Path,root:Path):
    text,enc=decode_text(path); rows=[]; malformed=[]
    for line_no,line in enumerate(text.splitlines(),1):
        if not line.strip(): continue
        cols=line.split('\t'); name=(cols[0] if cols else '').strip().lstrip('\ufeff')
        if not is_valid_name(name): continue
        size=None; md5=None
        if len(cols)>1:
            try: size=int(cols[1].strip())
            except (ValueError,TypeError): size=None
        if len(cols)>2:
            v=cols[2].strip().lower(); md5=v if MD5_RE.fullmatch(v or '') else None
        row={'tsv':path.relative_to(root).as_posix(),'line':line_no,'filename':name,'declared_size_bytes':size,'md5':md5,'column_count':len(cols)}
        if len(cols)<3 or size is None or md5 is None: malformed.append(row)
        rows.append(row)
    return {'path':path.relative_to(root).as_posix(),'encoding':enc,'rows':rows,'malformed':malformed}

def locate_local_file(server_root:Path,filename:str,by_basename:dict[str,list[Path]]):
    # Prefer exact relative path if TSV contains directories; basename fallback only when unique.
    exact=server_root.joinpath(*Path(filename.replace('\\','/')).parts)
    if exact.is_file(): return exact,'exact_relative_path'
    hits=by_basename.get(Path(filename).name.lower(),[])
    if len(hits)==1: return hits[0],'unique_basename_fallback'
    return None,'not_found' if not hits else 'ambiguous_basename'

def main():
    ap=argparse.ArgumentParser(description='Audit BCKR download*.tsv and optionally verify already-obtained server files. No network/decryption/promotion.')
    ap.add_argument('root',help='Extracted APK/XAPK/InstallPack directory containing download*.tsv files')
    ap.add_argument('--server-root',help='Optional already-obtained server files directory to verify against TSV fingerprints')
    ap.add_argument('--out',default='V066_BCKR_SERVER_TSV_AUDIT.json')
    a=ap.parse_args(); root=Path(a.root).resolve()
    if not root.is_dir(): raise SystemExit('root directory not found: '+str(root))
    tsv_paths=sorted([p for p in root.rglob('*') if p.is_file() and p.name.lower().startswith('download') and p.suffix.lower()=='.tsv'])
    parsed=[parse_tsv(p,root) for p in tsv_paths]
    rows=[r for t in parsed for r in t['rows']]
    by_filename=defaultdict(list)
    for r in rows: by_filename[r['filename']].append(r)
    dup={k:v for k,v in by_filename.items() if len(v)>1}
    pack_rows=[r for r in rows if Path(r['filename']).suffix.lower() in {'.pack','.list'}]
    pairs=defaultdict(lambda:{'pack':[],'list':[]})
    for r in pack_rows:
        p=Path(r['filename']); ext=p.suffix.lower()[1:]; stem=(p.parent/p.stem).as_posix().lower(); pairs[stem][ext].append(r)
    pair_rows=[]
    for stem,v in sorted(pairs.items()):
        pair_rows.append({'stem':stem,'pack_rows':v['pack'],'list_rows':v['list'],'has_exact_pair':bool(v['pack'] and v['list'])})
    verify=[]
    server_root=Path(a.server_root).resolve() if a.server_root else None
    if server_root:
        if not server_root.is_dir(): raise SystemExit('server-root directory not found: '+str(server_root))
        bybase=defaultdict(list)
        for p in server_root.rglob('*'):
            if p.is_file(): bybase[p.name.lower()].append(p)
        for r in rows:
            p,match=locate_local_file(server_root,r['filename'],bybase)
            vr={'filename':r['filename'],'tsv':r['tsv'],'line':r['line'],'match_method':match,'found':bool(p),'size_match':None,'md5_match':None}
            if p:
                size,md5=md5_file(p); vr.update({'local_path':p.relative_to(server_root).as_posix(),'actual_size_bytes':size,'actual_md5':md5})
                if r['declared_size_bytes'] is not None: vr['size_match']=size==r['declared_size_bytes']
                if r['md5'] is not None: vr['md5_match']=md5==r['md5']
            verify.append(vr)
    ext_counts=Counter(Path(r['filename']).suffix.lower() or '<none>' for r in rows)
    out={
      'schema':SCHEMA,'root':str(root),'promotion_allowed':False,
      'reason':'TSV provenance/fingerprint audit only. No network download, decryption, or asset promotion.',
      'tsv_files':[{'path':x['path'],'encoding':x['encoding'],'row_count':len(x['rows']),'malformed_count':len(x['malformed'])} for x in parsed],
      'summary':{
        'download_tsv_files':len(parsed),'rows':len(rows),'malformed_rows':sum(len(x['malformed']) for x in parsed),
        'duplicate_filenames':len(dup),'pack_or_list_rows':len(pack_rows),'pack_list_stems':len(pair_rows),
        'exact_pack_list_pairs':sum(x['has_exact_pair'] for x in pair_rows),
        'verified_server_files':sum(1 for x in verify if x['found'] and x['size_match'] is not False and x['md5_match'] is not False),
        'exact_md5_verified_server_files':sum(1 for x in verify if x['md5_match'] is True),
      },
      'extension_counts':dict(sorted(ext_counts.items())),
      'pack_list_pairs':pair_rows,
      'duplicate_filename_rows':dup,
      'malformed_rows':[r for x in parsed for r in x['malformed']],
      'server_file_verification':verify,
      'next_step':'After exact TSV size+MD5 verification, decrypt only verified pack/list pairs externally/manually, then run the V064 stage visual scanner on decrypted output.'
    }
    Path(a.out).write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(out['summary'],ensure_ascii=False)); print('report:',Path(a.out).resolve())
if __name__=='__main__': main()
