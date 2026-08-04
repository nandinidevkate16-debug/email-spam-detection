import urllib.request
import os

url = "https://raw.githubusercontent.com/justmarkham/pycon-2016-tutorial/master/data/sms.tsv"
print("Downloading SMS dataset...")

req = urllib.request.Request(
    url, 
    headers={'User-Agent': 'Mozilla/5.0'}
)

try:
    with urllib.request.urlopen(req, timeout=15) as response, open('sms.tsv', 'wb') as out_file:
        out_file.write(response.read())
    print("Download completed successfully! Size:", os.path.getsize('sms.tsv'), "bytes")
except Exception as e:
    print("Download error:", e)
