from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

app = Flask(__name__)
BASE='https://www.baiscope.lk'

def search_baiscope(q, section='movies'):
    # Public catalogue pages; respects normal site access. Search is performed against
    # the site's public listing pages by fetching a small set of catalogue pages.
    url=f'{BASE}/{section}'
    try:
        r=requests.get(url,timeout=15,headers={'User-Agent':'Mozilla/5.0'})
        r.raise_for_status()
    except Exception as e:
        return [], str(e)
    soup=BeautifulSoup(r.text,'html.parser')
    ql=q.lower()
    out=[]
    seen=set()
    for a in soup.find_all('a', href=True):
        title=' '.join(a.stripped_strings)
        href=urljoin(BASE,a['href'])
        if not title or href in seen: continue
        if ql in title.lower() and ('Sinhala Subtitle' in title or 'සිංහල උපසිර' in title):
            seen.add(href)
            out.append({'title':title,'url':href,'source':'Baiscope','type':'TV Series' if section=='tv' else 'Movie'})
        if len(out)>=50: break
    return out,''

@app.route('/')
def home(): return render_template('index.html', results=[], query='')

@app.route('/search')
def search():
    q=request.args.get('q','').strip()
    if not q: return render_template('index.html',results=[],query=q,error='Enter a movie or series name.')
    results=[]; errors=[]
    for section in ('movies','tv'):
        r,e=search_baiscope(q,section)
        results += r
        if e: errors.append(e)
    # deduplicate
    unique=[]; seen=set()
    for x in results:
        if x['url'] not in seen: seen.add(x['url']); unique.append(x)
    return render_template('index.html',results=unique,query=q,error='; '.join(errors) if errors else '')

if __name__=='__main__': app.run(host='0.0.0.0',port=5000,debug=False)
