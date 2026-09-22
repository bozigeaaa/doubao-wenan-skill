import json
from pathlib import Path
from playwright.sync_api import sync_playwright
root=Path.cwd()
html=(root/'outputs/daily-news-demo.html').read_text(encoding='utf-8')
report=json.loads((root/'outputs/news/2026-09-18.json').read_text(encoding='utf-8'))
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless=True)
 page=b.new_page(viewport={'width':1280,'height':800}); errors=[]
 page.set_default_timeout(5000)
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.set_content(html,wait_until='load')
 page.locator('#newsDate').select_option('2026-09-18')
 print('CARDCOUNT',page.locator('article.card').count(),page.locator('article.card:visible').count(),page.locator('#reportCount').inner_text(),page.locator('#eventCount').inner_text(),errors); page.locator('[data-stat-filter="all"]').click(); assert page.locator('article.card').count()==20
 assert page.locator('#reportCount').inner_text()=='15'
 assert page.locator('#eventCount').inner_text()=='20'
 page.locator('[data-stat-filter="verified"]').click()
 assert page.locator('article.card:visible').count()==15
 page.locator('[data-stat-filter="all"]').click()
 assert page.locator('article.card:visible').count()==20
 page.mouse.move(0,0)
 page.locator('#news-020 .proof-trigger').scroll_into_view_if_needed()
 box=page.locator('#news-020 .proof-trigger').bounding_box()
 page.mouse.move(box['x']+box['width']/2,box['y']+box['height']/2)
 print('PROOF020')
 page.wait_for_function("document.getElementById('proofPopover').dataset.ready==='true'")
 assert report['items'][19]['verification']['missing'] in page.locator('#proofPopover').inner_text()
 page.keyboard.press('Escape')
 page.evaluate("Object.defineProperty(navigator,'clipboard',{value:{writeText:async text=>{window.copied=text}}})")
 page.locator('#news-019 .copy').click()
 assert 'NEWS-20260918-019' in page.evaluate('window.copied')
 page.locator('#newsDate').select_option('2026-09-17')
 assert page.locator('article.card').count()==17
 page.locator('#newsDate').select_option('2026-09-18')
 for width,height in [(1280,800),(390,844)]:
  page.set_viewport_size({'width':width,'height':height})
  assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
  page.evaluate('window.scrollTo(0,document.body.scrollHeight)')
  assert page.evaluate('window.scrollY')>1000
  page.locator('#backToTop').click()
  page.wait_for_function('window.scrollY===0')
 page.screenshot(path=str(root/'outputs/news/evidence-2026-09-18/14-00/report-mobile.png'))
 assert not errors,errors
 b.close()
print(json.dumps({'date':'2026-09-18','cards':20,'verified':15,'unconfirmed':5,'historicalDateSwitch':True,'evidencePopover':True,'copyNewsId':True,'desktopMobileOverflow':False,'backToTop':True,'pageErrors':errors}))
