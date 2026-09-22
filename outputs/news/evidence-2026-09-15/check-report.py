import json,hashlib,sys
from pathlib import Path
from playwright.sync_api import sync_playwright
root=Path.cwd()
sys.path.insert(0,str(root/'scripts'))
import daily_news
ed=root/'outputs/news/evidence-2026-09-15'
r=json.loads((root/'outputs/news/2026-09-15.json').read_text(encoding='utf-8'))
assert len(r['items'])==19
assert sum(x['status']=='verified' for x in r['items'])==17
assert r['completedSlots']==['14:00'],r['completedSlots']
assert daily_news.due(today='2026-09-15',slot='14:00')['due'] is False
assert daily_news.due(today='2026-09-15',slot='09:00')['due'] is True
for name,digest in json.loads((ed/'before-archive-hashes.json').read_text()).items():
 assert hashlib.sha256((root/'outputs/news'/name).read_bytes()).hexdigest()==digest,name
for x in r['items']:
 assert x['status']==x['verification']['result']
 assert x['verification']['checkedAt']>=r['run']['startedAt']
 assert x['verification']['checkedAt']<=r['run']['completedAt']
 assert x['url'].startswith('https://')
 assert all((ed/n).is_file() for n in x['evidenceFiles'])
assert len({x['id'] for x in r['items']})==19
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless=True)
 page=b.new_page(viewport={'width':1294,'height':912})
 errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto((root/'outputs/daily-news-2026-09-15.html').as_uri())
 page.evaluate("Object.defineProperty(navigator,'clipboard',{value:{writeText:async t=>{window.copiedNews=t}}})")
 assert page.locator('#newsDate').input_value()=='2026-09-15'
 assert page.locator('#news .card').count()==17
 for status,num in [('all',19),('verified',17),('unconfirmed',2)]:
  page.locator('#status').select_option(status)
  assert page.locator('#news .card').count()==num,(status,num)
 page.locator('#news-016 .proof-trigger').hover()
 assert '订阅' in page.locator('#proofPopover').inner_text()
 page.mouse.move(1,1)
 page.locator('#status').select_option('verified')
 page.locator('#news-001 .proof-trigger').hover()
 assert '2026/9/15' in page.locator('#proofPopover').inner_text()
 page.mouse.move(1,1)
 page.locator('#news-001 [data-copy]').click()
 assert 'NEWS-20260915-001' in page.evaluate('window.copiedNews')
 page.screenshot(path=str(ed/'daily-desktop.png'))
 dates=page.locator('#newsDate option').evaluate_all('(nodes)=>nodes.map(n=>n.value)')
 for date in ['2026-09-12','2026-09-13','2026-09-14']:
  page.locator('#newsDate').select_option(date)
  old=json.loads((root/f'outputs/news/{date}.json').read_text(encoding='utf-8'))
  assert page.locator('#news .card').count()==sum(x['status']=='verified' for x in old['items'])
  page.locator('[data-copy]').first.click()
  assert 'NEWS-'+date.replace('-','')+'-' in page.evaluate('window.copiedNews')
 page.locator('#newsDate').select_option('2026-09-15')
 page.set_viewport_size({'width':390,'height':844})
 assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
 page.screenshot(path=str(ed/'daily-mobile.png'))
 assert not errors,errors
 b.close()
result={'passed':True,'total':19,'verified':17,'unconfirmed':2,'new':19,'updated':0,'completedSlots':r['completedSlots'],'archiveDates':dates,'oldArchivesUnchanged':True,'dateFiltersAndCopy':True,'proofPopovers':True,'mobileOverflow':False,'pageErrors':errors}
(ed/'qa-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result))
