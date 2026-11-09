from __future__ import annotations
import hashlib, zipfile
from pathlib import Path
from .geode import parse

KNOWN={
 'SPINTEXT.GEO':'848f5afb43a2184b01d2a4ad3231957b6ab9936006b23b4b2a260d1224d44370',
 'NOTEPAD.GEO':'edc48848ff4b9d2880e715bbb29532f14b3b54293c45159c467e33e2af841d1b',
 'VIEWER.GEO':'3d433a39c455a9cea242763dad0e3f681b4196fb7b1a75a08ca47e1aa8aa4a30',
 'TERM.GEO':'2d66ac2ff9fd24c4591303b2cba7cec6f40f0d52b4f3d75d9e0cdaa5fc1be542',
}
PATHS={
 'SPINTEXT.GEO':'/WORLD/EXTRAS/SPINTEXT.GEO',
 'NOTEPAD.GEO':'/WORLD/NOTEPAD.GEO',
 'VIEWER.GEO':'/WORLD/VIEWER.GEO',
 'TERM.GEO':'/WORLD/TERM.GEO',
}

PROFILES={
 'geoworks-pro-1.2':{
  'hashes':KNOWN,
  'format_version':1,
  'kernel_protocol':[622,3],
  'ui_protocol':[693,0],
 },
 'geoworks-1.2.8-de':{
  'hashes':{
   'SPINTEXT.GEO':'18f2075c9d61fe7231b1dacae8c171e68c2028ef2fca6d40a6694158fdfcb9fd',
   'NOTEPAD.GEO':'a1ebd0cb84712a126b1f67f5fd1ca6b57f8bda2e9038e9224ba16ebc008f9ea9',
   'VIEWER.GEO':'c884b76cdc4f9119d4794f7830d5438e0abcc1d92d3cc248aa912bde85ed43e7',
   'TERM.GEO':'a62ebc0fb3c01acb4b59c8172d20d520653822a6d42f0bec4831dfdb93e1cf3a',
  },
  'format_version':1,
  'kernel_protocol':[622,3],
  'ui_protocol':[693,0],
 },
}

def sha(b):return hashlib.sha256(b).hexdigest()

def member(z,end):
    names=[n for n in z.namelist() if n.replace('\\','/').upper().endswith(end)]
    if len(names)!=1:raise ValueError(f'Expected exactly one archive member ending {end}, got {len(names)}')
    return z.read(names[0])

def load_templates(gwp,profile='geoworks-pro-1.2'):
    if profile not in PROFILES:
        raise ValueError(f'Unknown target profile: {profile}')
    spec=PROFILES[profile]
    out={}
    with zipfile.ZipFile(gwp) as z:
        for name,end in PATHS.items():
            data=member(z,end); digest=sha(data)
            expected=spec['hashes'][name]
            if digest!=expected:
                raise ValueError(f'Unsupported {name} for profile {profile}: SHA-256 {digest}; expected {expected}')
            info=parse(data,name)
            if info['format_version']!=spec['format_version']:
                raise ValueError(f'{name} is GEOS format {info["format_version"]}; profile {profile} requires {spec["format_version"]}')
            if info['kernel_protocol']!=spec['kernel_protocol']:
                raise ValueError(f'{name} kernel protocol {info["kernel_protocol"]}; profile {profile} requires {spec["kernel_protocol"]}')
            ui_imports=[item for item in info['imports'] if item['name'].lower()=='ui']
            if len(ui_imports)!=1 or ui_imports[0]['protocol']!=spec['ui_protocol']:
                actual=[item['protocol'] for item in ui_imports]
                raise ValueError(f'{name} UI import protocol(s) {actual}; profile {profile} requires exactly one {spec["ui_protocol"]}')
            out[name]=(data,info,digest)
    return out

def scan(gwp):
    rows=[]
    with zipfile.ZipFile(gwp) as z:
        for zi in z.infolist():
            if zi.is_dir() or not zi.filename.lower().endswith('.geo'):continue
            data=z.read(zi)
            try:q=parse(data,zi.filename)
            except Exception:continue
            rows.append({'path':zi.filename,'sha256':sha(data),'format':q['format_version'],'name':q['permanent_name'],
                         'ext':q['permanent_extension'],'release':q['release'],'protocol':q['protocol'],
                         'kernel_protocol':q['kernel_protocol'],'imports':q['imports'],'resources':len(q['resources']),
                         'exports':len(q['exports'])})
    return rows
