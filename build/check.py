"""Run the engine's geometry audit on this room's own build (index.html, patched).

    python3 build/check.py

Same checks the skill's test.py runs, but against the page build/make.sh produced rather than a fresh
splice into the stock engine, so the extra builders and the walk mode are covered too. Exits 1 on any
finding. Needs Chrome and the network (three.js comes from a CDN).
"""
import html, json, os, re, shutil, subprocess, sys, tempfile, time

here = os.path.dirname(os.path.abspath(__file__))
proj = os.path.dirname(here)
page = os.path.join(proj, 'index.html')
chrome = os.environ.get('CHROME') or shutil.which('google-chrome') or shutil.which('google-chrome-stable') or shutil.which('chromium')
if not chrome:
    sys.exit('No Chrome found: set CHROME=<path to a Chrome or Chromium binary>')

tmp = tempfile.mkdtemp(prefix='room-check-')
prof = os.path.join(tmp, 'chrome')
out = os.path.join(tmp, 'dom.html')
with open(out, 'w') as f:
    pr = subprocess.Popen([chrome, '--headless=new', '--user-data-dir=' + prof, '--disable-gpu', '--use-angle=swiftshader',
                           '--enable-unsafe-swiftshader', '--disable-extensions', '--allow-file-access-from-files',
                           '--window-size=1200,800', '--virtual-time-budget=9000', '--dump-dom',
                           'file://' + page + '#debug&test'], stdout=f, stderr=subprocess.DEVNULL)
    for _ in range(240):
        if pr.poll() is not None or '</html>' in open(out).read():
            break
        time.sleep(0.5)
    pr.kill()
subprocess.run(['pkill', '-f', 'user-data-dir=' + prof], capture_output=True)
dom = open(out).read()

found = []
m = re.search(r'<pre id="audit">(\[.*?\])</pre>', dom, re.S)
if not m:
    sys.exit('FAIL - no audit in the page (a script error, or the CDN was unreachable)')
found += json.loads(html.unescape(m.group(1)))
mf = re.search(r'<pre id="finishes">(.*?)</pre>', dom, re.S)
if not mf or mf.group(1) != 'photo':
    found.append({'layout': 0, 'text': 'photo finishes: ' + (html.unescape(mf.group(1)) if mf else 'the loader never reported')})
mo = re.search(r'<pre id="load">(.*?)</pre>', dom, re.S)
lo = json.loads(html.unescape(mo.group(1))) if mo else None
if not lo:
    found.append({'layout': 0, 'text': 'page load: the load event never reported'})
elif lo['photos'] or lo['finishes'] == 'photo':
    found.append({'layout': 0, 'text': 'page load: the load event waited for %d photo(s) and %s'
                  % (lo['photos'], 'the scans' if lo['finishes'] == 'photo' else 'no scans')})
ml = re.search(r'<pre id="light">(.*?)</pre>', dom, re.S)
if not ml or ml.group(1) != 'steady':
    found.append({'layout': 0, 'text': 'photo light: ' + (ml.group(1) if ml else 'the check never ran')})

mc = re.search(r'<pre id="checks">(\[.*?\])</pre>', dom, re.S)
lines = json.loads(html.unescape(mc.group(1))) if mc else []
print('--- what the fit checks say ---')
for l in lines:
    print('    option %d  [%s] %s' % (l['layout'], l['level'], l['text']))
print('ok' if not found else 'FAIL')
for f in found:
    print('     %s: %s' % ('page' if f['text'].startswith(('photo finishes', 'photo light', 'page load')) else
                           'library' if f['layout'] == 0 else 'option %d' % f['layout'], f['text']))
shutil.rmtree(tmp, ignore_errors=True)
sys.exit(1 if found else 0)
