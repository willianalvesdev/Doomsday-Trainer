"""Extract the supplied APK's web app and apply explicit local-web adaptations."""
from pathlib import Path
import hashlib
import io
import json
import sys
import zipfile

source = Path(sys.argv[1])
root = Path(__file__).parent / 'dist'
root.mkdir(exist_ok=True)
manifest = {}
with zipfile.ZipFile(source) as outer:
    with zipfile.ZipFile(io.BytesIO(outer.read('base.apk'))) as apk:
        for name in apk.namelist():
            if not name.startswith('assets/public/') or name.endswith('/'):
                continue
            relative = name.removeprefix('assets/public/')
            target = root / relative
            if not target.resolve().is_relative_to(root.resolve()):
                raise ValueError('Unsafe archive path')
            data = apk.read(name)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            manifest[relative] = hashlib.sha256(data).hexdigest()

bundle = root / 'assets/index-QHRtOYCg.js'
js = bundle.read_text(encoding='utf-8')
start = js.index('function va({children:e})')
end = js.index('function ya()', start)
js = js[:start] + '''function va({children:e}){return(0,H.jsx)(_a.Provider,{value:{playFabId:null,entityToken:null,entityId:null,sessionTicket:null,playerStats:null,displayName:"",isLoading:false,authError:"Online play is unavailable in this local edition",refreshStats:async()=>{}},children:e})}''' + js[end:]
analytics = 'if(!S.isNativePlatform())try{let e=on(Wo);Li().then(t=>{t&&(Go=Fi(e))})}catch{}'
assert js.count(analytics) == 1
js = js.replace(analytics, '')
js = js.replace('onClick:()=>a&&e(`MULTIPLAYER_LOBBY`),disabled:!a', 'onClick:()=>{},disabled:!0')
js = js.replace('onClick:()=>t(`GLOBAL_LEADERBOARD`)', 'disabled:!0,title:`Unavailable in the local web edition`')
js = js.replace('children:a?`Race a real opponent head-to-head`:`Requires an internet connection`', 'children:`Unavailable in the local web edition`')
js = js.replace('new Audio(`/Doomsday_Theme.mp3`)', 'new Audio(new URL(`../Doomsday_Theme.mp3`,import.meta.url))')
bundle.write_text(js, encoding='utf-8')
index = root / 'index.html'
html = index.read_text(encoding='utf-8').replace(', maximum-scale=1.0, user-scalable=no', '')
html = html.replace('<title>doomsday-trainer</title>', '<title>Doomsday Trainer — Web</title>')
html = html.replace('<meta charset="UTF-8" />', '<meta charset="UTF-8" /><meta http-equiv="Content-Security-Policy" content="connect-src \'self\'; object-src \'none\'">')
index.write_text(html, encoding='utf-8')
manifest_path = Path(__file__).parent / 'evidence/extraction.json'
manifest_path.parent.mkdir(exist_ok=True)
manifest_path.write_text(json.dumps({'package_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'original_assets':manifest},indent=2),encoding='utf-8')
assert 'Li().then(t=>{t&&(Go=Fi(e))})' not in js
assert 'onClick:()=>{},disabled:!0' in js
print(f'Prepared {len(manifest)} original assets with local-web adaptations.')
