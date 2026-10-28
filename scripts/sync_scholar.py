"""Refresh public Scholar data atomically; blocked or incomplete responses never replace cache."""
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
ROOT = Path(__file__).resolve().parents[1]
def parse_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    if not soup.select_one('#gsc_prf_in'):
        raise ValueError('Scholar profile missing; response may be blocked')
    papers = []
    for row in soup.select('.gsc_a_tr'):
        title = row.select_one('.gsc_a_at')
        if not title:
            raise ValueError('Incomplete publication row')
        grey = row.select('.gs_gray')
        year = row.select_one('.gsc_a_y')
        cited = row.select_one('.gsc_a_ac')
        papers.append({'title': title.get_text(' ', strip=True), 'authors': grey[0].get_text(' ', strip=True) if grey else '', 'venue': grey[1].get_text(' ', strip=True) if len(grey)>1 else '', 'year': int(year.text.strip()) if year and year.text.strip().isdigit() else None, 'citations': int(re.sub(r'\D','',cited.text) or 0) if cited else 0, 'url': urljoin('https://scholar.google.com', title['href'])})
    more = soup.select_one('#gsc_bpf_more')
    return papers, bool(more is not None and not more.has_attr('disabled'))
def sync():
    config = json.loads((ROOT/'data/scholar.json').read_text(encoding='utf-8-sig'))
    author = config['scholar_id']
    if not re.fullmatch(r'[A-Za-z0-9_-]+', author):
        raise ValueError('Configure a valid scholar_id')
    path = ROOT/'data/publications.json'
    previous = json.loads(path.read_text(encoding='utf-8-sig'))
    normalize = lambda title: re.sub(r'\W+', '', title).casefold()
    old = {normalize(p['title']):p for p in previous['papers']}
    papers = []; seen = set()
    with requests.Session() as session:
        for start in range(0, 2000, 100):
            response = session.get('https://scholar.google.com/citations', params={'user':author, 'hl':'en', 'pagesize':100, 'cstart':start,'sortby':'pubdate'}, timeout=30)
            response.raise_for_status()
            page, more = parse_page(response.text)
            if not page:
                raise ValueError('Empty Scholar response; retaining existing data')
            for p in page:
                key=normalize(p['title'])
                if key in seen: continue
                seen.add(key)
                prior=old.get(key,{})
                p['type']=prior.get('type','conference' if re.search(r'conference|proceedings|ICMA|ICRA|IROS',p['venue'],re.I) else 'other')
                # The profile listing may abbreviate authors. Keep the curated full list.
                if prior.get('authors'): p['authors']=prior['authors']
                papers.append(p)
            if not more: break
        else:
            raise ValueError('Pagination limit reached; refusing partial update')
    if len(papers) < len(previous['papers']):
        raise ValueError('Paper count decreased; review manually before replacing cache')
    result={'scholar_id':author,'updated_at':datetime.now(timezone.utc).isoformat(),'papers':sorted(papers,key=lambda p:p['year'] or 0,reverse=True)}
    temp=path.with_suffix('.tmp');temp.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');temp.replace(path)
    print(f'Synchronized {len(papers)} papers')
if __name__=='__main__':
    sync()
