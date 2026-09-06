# -*- coding: utf-8 -*-
"""Read small JSON/log entries from a large GitHub Actions artifact zip via HTTP Range requests.
usage: python remote_zip_probe.py <artifact_id> <name-substring> [<name-substring> ...]
"""
import sys, subprocess, urllib.request, urllib.error, struct, zlib, re, json
art = sys.argv[1]; wants = sys.argv[2:]
tok = subprocess.run(['gh', 'auth', 'token'], capture_output=True, text=True).stdout.strip()
api = 'https://api.github.com/repos/tochiazuma0510-alt/shadow-atelier/actions/artifacts/%s/zip' % art
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None
op = urllib.request.build_opener(NoRedirect)
req = urllib.request.Request(api, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json', 'User-Agent': 'probe'})
try:
    op.open(req)
    print('no redirect?'); sys.exit(1)
except urllib.error.HTTPError as e:
    if e.code not in (302, 301, 307):
        print('unexpected', e.code); sys.exit(1)
    url = e.headers['Location']
def rng(a, b):
    r = urllib.request.Request(url, headers={'Range': 'bytes=%d-%d' % (a, b), 'User-Agent': 'probe'})
    with urllib.request.urlopen(r, timeout=120) as f:
        return f.read()
# total size
r = urllib.request.Request(url, method='HEAD', headers={'User-Agent': 'probe'})
with urllib.request.urlopen(r, timeout=60) as f:
    total = int(f.headers['Content-Length'])
print('total', total)
tail = rng(max(0, total - 2 * 1024 * 1024), total - 1)
# find EOCD / zip64
eocd = tail.rfind(b'PK\x05\x06')
if eocd < 0: print('no eocd'); sys.exit(1)
cd_size, cd_off = struct.unpack('<II', tail[eocd + 12:eocd + 20])
if cd_off == 0xFFFFFFFF or cd_size == 0xFFFFFFFF:
    loc = tail.rfind(b'PK\x06\x07')
    z64off = struct.unpack('<Q', tail[loc + 8:loc + 16])[0]
    z64 = rng(z64off, z64off + 55)
    cd_size, cd_off = struct.unpack('<QQ', z64[40:56])
cd = rng(cd_off, cd_off + cd_size - 1)
pos = 0; entries = []
while pos + 46 <= len(cd) and cd[pos:pos + 4] == b'PK\x01\x02':
    (flag, comp, csize, usize, nlen, elen, clen, loff) = struct.unpack('<HH', cd[pos + 8:pos + 12]) + struct.unpack('<II', cd[pos + 20:pos + 28]) + struct.unpack('<HHH', cd[pos + 28:pos + 34]) + struct.unpack('<I', cd[pos + 42:pos + 46])
    name = cd[pos + 46:pos + 46 + nlen].decode('utf-8', 'replace')
    extra = cd[pos + 46 + nlen:pos + 46 + nlen + elen]
    if csize == 0xFFFFFFFF or usize == 0xFFFFFFFF or loff == 0xFFFFFFFF:
        ep = 0
        while ep + 4 <= len(extra):
            hid, hsz = struct.unpack('<HH', extra[ep:ep + 4]); body = extra[ep + 4:ep + 4 + hsz]
            if hid == 1:
                q = 0
                if usize == 0xFFFFFFFF: usize = struct.unpack('<Q', body[q:q + 8])[0]; q += 8
                if csize == 0xFFFFFFFF: csize = struct.unpack('<Q', body[q:q + 8])[0]; q += 8
                if loff == 0xFFFFFFFF: loff = struct.unpack('<Q', body[q:q + 8])[0]; q += 8
            ep += 4 + hsz
    entries.append((name, comp, csize, usize, loff))
    pos += 46 + nlen + elen + clen
print('entries', len(entries))
def fetch(e):
    name, comp, csize, usize, loff = e
    lh = rng(loff, loff + 29)
    nlen, elen = struct.unpack('<HH', lh[26:30])
    start = loff + 30 + nlen + elen
    data = rng(start, start + csize - 1)
    if comp == 8: data = zlib.decompress(data, -15)
    return data
hits = [e for e in entries if any(w in e[0] for w in wants) and e[3] < 400000]
for e in hits[:12]:
    try:
        d = fetch(e).decode('utf-8', 'replace')
        print('==', e[0], e[3]); print(d[-1200:])
    except Exception as ex:
        print('== fetch fail', e[0], ex)
