from playwright.sync_api import sync_playwright
from pathlib import Path
import json
report=json.loads(Path('outputs/news/2026-09-10.json').read_text(encoding='utf-8'))
assert len(report['items'])==25
assert len([n for n in report['items'] if n['status']=='verified'])==20
assert len([n for n in report['items'] if n['status']=='unconfirmed'])==5
assert all(n.get('verification',{}).get('checkedAt') for n in report['items'])
assert all(n['verification']['missing'] for n in report['items'] if n['status']=='unconfirmed')
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless=True)
 page=b.new_page(viewport={'width':1440,'height':1000})
 errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto('http://127.0.0.1:62436/',wait_until='networkidle')
 assert page.locator('article.card').count()==20
 assert page.locator('#newsDate option').count()==15
 assert page.locator('#reportCount').inner_text()=='20'
 assert page.locator('#pendingCount').inner_text()=='05'
 assert page.locator('#productCount').inner_text()=='03'
 assert '待系统' not in page.locator('body').inner_text()
 page.locator('#news-001 .proof-trigger').hover()
 pop=page.locator('#proofPopover')
 assert pop.is_visible()
 assert '核验时间' in pop.inner_text()
 assert 'Invalid Date' not in pop.inner_text()
 pop.hover()
 page.wait_for_timeout(200)
 assert pop.is_visible()
 page.mouse.move(1,1)
 page.wait_for_timeout(200)
 assert not pop.is_visible()
 for name,count in [('打包箱',2),('移动卫浴',1),('五金',2),('薄壁轻钢',1)]:
  page.get_by_role('button',name=name,exact=True).click()
  assert page.locator('article.card').count()==count,(name,page.locator('article.card').count())
 page.locator('#reset').click()
 page.locator('#status').select_option('unconfirmed')
 assert page.locator('article.card').count()==5
 assert page.get_by_role('button',name='复制核验线索',exact=True).count()==5
 assert '待系统' not in page.locator('body').inner_text()
 page.locator('#news-008 .proof-trigger').hover()
 assert '仍缺少的证据' in pop.inner_text()
 assert '核验时间' in pop.inner_text()
 page.screenshot(path='outputs/news-verification-unconfirmed.png')
 page.mouse.move(1,1)
 page.wait_for_timeout(200)
 page.locator('#status').select_option('all')
 assert page.locator('article.card').count()==25
 page.locator('#search').fill('NEWS-20260910-017')
 assert page.locator('article.card').count()==1
 assert '采购公告' in page.locator('#news-017').inner_text()
 assert '报价截止' not in page.locator('#news-017').inner_text()
 page.locator('#reset').click()
 assert page.locator('article.card').count()==20
 page.locator('#newsDate').select_option('2026-09-09')
 assert page.locator('article.card').count()==0
 assert '暂无收录' in page.locator('#empty').inner_text()
 page.locator('#newsDate').select_option('2026-09-10')
 assert page.locator('article.card').count()==20
 page.screenshot(path='outputs/news-verification-desktop.png')
 page.set_viewport_size({'width':390,'height':844})
 assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
 page.screenshot(path='outputs/news-verification-mobile.png')
 assert not errors,errors
 print(json.dumps({'defaultVerifiedCards':20,'allRecords':25,'unconfirmed':5,'productFilters':'passed','hoverEvidence':'passed','timestamps':'passed','emptyDate':'passed','mobileOverflow':False,'pageErrors':errors}))
 b.close()
