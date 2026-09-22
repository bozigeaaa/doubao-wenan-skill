import json
from pathlib import Path
from playwright.sync_api import sync_playwright
import sys
sys.path.insert(0,str(Path.cwd()/'scripts'))
import daily_news
root=Path.cwd()
before=json.loads((root/'outputs/news/evidence-2026-09-14/before-weekend-archive.json').read_text(encoding='utf-8'))
reports={day:json.loads((root/('outputs/news/'+day+'.json')).read_text(encoding='utf-8')) for day in ['2026-09-12','2026-09-13','2026-09-14']}
items=[item for report in reports.values() for item in report['items']]
assert len(items)==len(before['items'])==13
assert len({n['url'] for n in items})==13
for old in before['items']:
 new=next(n for n in items if n['url']==old['url'])
 assert new['verification']==old['verification'] and new['summary']==old['summary'] and new['status']==old['status']
for day in ['2026-09-12','2026-09-13']:
 report=reports[day]
 assert report['collectedAt'].startswith('2026-09-14')
 assert not report['completedSlots'] and 'slot' not in report['run']
 assert all(n['published']==day and '2026-09-14补录' in n['update'] for n in report['items'])
assert daily_news.due(today='2026-09-14',slot='09:00')['due'] is False
assert daily_news.due(today='2026-09-14',slot='14:00')['due'] is True
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless=True)
 page=b.new_page(viewport={'width':1294,'height':912})
 errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto((root/'outputs/daily-news-2026-09-14.html').as_uri())
 assert page.locator('#newsDate').input_value()=='2026-09-14'
 assert page.locator('#newsDate option').count()==15
 page.evaluate("Object.defineProperty(navigator,'clipboard',{value:{writeText:async t=>{window.copiedNews=t}}})")
 for day,counts in [('2026-09-12',(1,0,1)),('2026-09-13',(4,3,1)),('2026-09-14',(8,7,1))]:
  page.locator('#newsDate').select_option(day)
  for status,count in zip(['all','verified','unconfirmed'],counts):
   page.locator('#status').select_option(status)
   assert page.locator('#news .card').count()==count,(day,status)
  page.locator('#status').select_option('all')
  page.locator('[data-copy]').first.click()
  assert ('NEWS-'+day.replace('-','')+'-') in page.evaluate('window.copiedNews')
 page.locator('#newsDate').select_option('2026-09-13')
 page.locator('#status').select_option('all')
 page.locator('#news-001 .proof-trigger').hover()
 assert '2026/9/14' in page.locator('#proofPopover').inner_text()
 page.mouse.move(1,1)
 page.screenshot(path=str(root/'outputs/news/evidence-2026-09-14/weekend-archive-desktop.png'))
 page.set_viewport_size({'width':390,'height':844})
 assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
 assert not errors,errors
 b.close()
print(json.dumps({'passed':True,'dailyTotals':[1,4,8],'totalUnchanged':13,'verificationUnchanged':True,'dateSwitch':True,'copyDate':True,'actualCheckDatePreserved':True,'mondaySchedulePreserved':True,'pageErrors':errors}))
