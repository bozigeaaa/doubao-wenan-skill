import json,sys
from pathlib import Path
from playwright.sync_api import sync_playwright
root=Path.cwd()
sys.path.insert(0,str(root/'scripts'))
import daily_news
ed=root/'outputs/news/evidence-2026-09-14/recheck-12-14'
reports={d:json.loads((root/f'outputs/news/{d}.json').read_text(encoding='utf-8')) for d in ['2026-09-12','2026-09-13','2026-09-14']}
old={d:json.loads((ed/f'before-{d}.json').read_text(encoding='utf-8')) for d in reports}
items=[x for r in reports.values() for x in r['items']]
assert len(items)==22 and len({x['url'] for x in items})==22
assert sum(x['status']=='verified' for x in items)==17
for d,r in old.items():
 for x in r['items']:
  if d=='2026-09-13' and x['id']=='004':continue
  new=next(n for n in items if n['url']==x['url'])
  assert new['verification']==x['verification'] and new['summary']==x['summary']
for d in ['2026-09-12','2026-09-13']:
 assert not reports[d]['completedSlots'] and 'slot' not in reports[d]['run']
 assert all(x['published']==d for x in reports[d]['items'])
assert daily_news.due(today='2026-09-14',slot='09:00')['due'] is False
assert daily_news.due(today='2026-09-14',slot='14:00')['due'] is True
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless=True)
 page=b.new_page(viewport={'width':1294,'height':912})
 errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto((root/'outputs/daily-news-2026-09-14.html').as_uri())
 page.evaluate("Object.defineProperty(navigator,'clipboard',{value:{writeText:async t=>{window.copiedNews=t}}})")
 for d,counts in [('2026-09-12',(4,3,1)),('2026-09-13',(9,6,3)),('2026-09-14',(9,8,1))]:
  page.locator('#newsDate').select_option(d)
  for status,count in zip(['all','verified','unconfirmed'],counts):
   page.locator('#status').select_option(status)
   assert page.locator('#news .card').count()==count,(d,status)
  page.locator('#status').select_option('all')
  page.locator('[data-copy]').first.click()
  assert 'NEWS-'+d.replace('-','')+'-' in page.evaluate('window.copiedNews')
 page.locator('#newsDate').select_option('2026-09-12')
 page.locator('#news-004 .proof-trigger').hover()
 assert '2026/9/14' in page.locator('#proofPopover').inner_text()
 page.mouse.move(1,1)
 page.locator('#newsDate').select_option('2026-09-13')
 page.screenshot(path=str(ed/'recheck-desktop.png'))
 page.locator('#news-008 .proof-trigger').hover()
 assert '原始公告' in page.locator('#proofPopover').inner_text()
 page.mouse.move(1,1)
 page.set_viewport_size({'width':390,'height':844})
 assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
 assert not errors,errors
 b.close()
result={'passed':True,'totals':[4,9,9],'verified':[3,6,8],'unconfirmed':[1,3,1],'new':9,'updated':1,'datesAndCopy':True,'oldCheckTimesPreserved':True,'afternoonDuePreserved':True,'mobileOverflow':False,'pageErrors':errors}
(ed/'qa-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result))
