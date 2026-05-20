import urllib.request
import urllib.error
import json

BASE = 'http://127.0.0.1:5000'
ENDPOINTS = [
    '/',
    '/topics',
    '/practice',
    '/quiz',
    '/dashboard',
    '/runner',
    '/resources',
    '/domain/machine-learning-fundamentals',
    '/api/questions/ml?count=3',
    '/api/quiz?count=5'
]

results = []
for ep in ENDPOINTS:
    url = BASE + ep
    try:
        with urllib.request.urlopen(url, timeout=5) as r:
            status = r.getcode()
            data = r.read(2000)
            txt = data.decode('utf-8', errors='ignore')
            ok = status == 200
            contains_error = 'Traceback' in txt or 'Exception' in txt or 'Not Found' in txt
            results.append((ep, status, len(data), contains_error))
    except urllib.error.HTTPError as e:
        results.append((ep, e.code, 0, True))
    except Exception as e:
        results.append((ep, 'ERROR', 0, True))

print('\nHealth check results:')
for ep, status, length, bad in results:
    print(f"{ep:35} -> {status:6}  bytes={length:5}  error={bad}")

# Exit code 0 if all OK
if all(not bad and status==200 for (_,status,_,bad) in results):
    print('\nAll endpoints OK')
else:
    print('\nSome endpoints returned errors; check server logs.')
    exit(2)
