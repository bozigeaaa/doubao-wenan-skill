import json
from pathlib import Path
from playwright.sync_api import sync_playwright
root=Path.cwd()
html=(root/'outputs/daily-news-demo.html').read_text(encoding='utf-8')
dates=['2026-09-19','2026-09-20','2026-09-21']
results=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless=True)
 page=b.new_page(viewport={'width':1280,'height':800})
 page.set_default_timeout(6000)
 errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.set_content(html,wait_until='load')
 assert page.locator('#newsDate').input_value()=='2026-09-21'
 assert page.locator('article.card:visible').count()==1
 page.evaluate("Object.defineProperty(navigator,'clipboard',{value:{writeText:async text=>{window.copied=text}}})")
 for day in dates:
  report=json.loads((root/'outputs/news'/f'{day}.json').read_text(encoding='utf-8'))
  items=report['items']; verified=sum(i['status']=='verified' for i in items)
  page.locator('#newsDate').select_option(day)
  page.locator('[data-stat-filter="verified"]').click()
  assert page.locator('article.card:visible').count()==verified,(day,'verified')
  assert int(page.locator('#reportCount').inner_text())==verified
  assert int(page.locator('#eventCount').inner_text())==len(items)
  page.locator('[data-stat-filter="all"]').click()
  assert page.locator('article.card:visible').count()==len(items),(day,'total')
  item=items[-1]; news='#news-'+item['id']
  page.mouse.move(0,0)
  trigger=page.locator(news+' .proof-trigger'); trigger.scroll_into_view_if_needed()
  box=trigger.bounding_box(); page.mouse.move(box['x']+box['width']/2,box['y']+box['height']/2)
  page.wait_for_function("document.getElementById('proofPopover').dataset.ready==='true'")
  proof=page.locator('#proofPopover').inner_text()
  expected=item['verification']['missing'] if item['status']=='unconfirmed' else item['review']
  assert expected in proof,(day,'proof')
  assert '2026/9/21' in proof,(day,'actual verification date')
  page.keyboard.press('Escape')
  page.locator(news+' .copy').click()
  assert 'NEWS-'+day.replace('-','')+'-'+item['id'] in page.evaluate('window.copied')
  if day!='2026-09-21':
   assert not report.get('completedSlots'),day
   assert 'slot' not in report['run'],day
   assert report['backfill']['sourceDate']=='2026-09-21'
  results.append({'date':day,'total':len(items),'verified':verified,'unconfirmed':len(items)-verified,'proof':True,'copy':True,'actualTimes':True})
 page.locator('#newsDate').select_option('2026-09-18')
 page.locator('[data-stat-filter="all"]').click()
 assert page.locator('article.card:visible').count()==20
 page.locator('#newsDate').select_option('2026-09-20')
 for width,height in [(1280,800),(390,844)]:
  page.set_viewport_size({'width':width,'height':height})
  assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
  page.evaluate('window.scrollTo(0,document.body.scrollHeight)')
  assert page.evaluate('window.scrollY')>100
  page.locator('#backToTop').click();page.wait_for_function('window.scrollY===0')
 page.screenshot(path=str(root/'outputs/news/evidence-2026-09-21/09-00/report-mobile.png'))
 page.set_viewport_size({'width':1280,'height':800})
 page.locator('#newsDate').select_option('2026-09-21');page.locator('[data-stat-filter="verified"]').click()
 page.screenshot(path=str(root/'outputs/news/evidence-2026-09-21/09-00/report-desktop.png'))
 assert not errors,errors
 b.close()
print(json.dumps({'reports':results,'historyPreserved':True,'desktopMobileOverflow':False,'backToTop':True,'pageErrors':errors}))
