from playwright.sync_api import sync_playwright
import json
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless=True)
 page=b.new_page(viewport={'width':1440,'height':1000})
 errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto('http://127.0.0.1:62436/',wait_until='networkidle')
 assert page.locator('article.card').count()==25
 assert page.locator('#newsDate option').count()==15
 assert page.locator('article.card .sourcebrief a').count()==25
 assert page.locator('#eventCount').inner_text()=='25'
 assert page.locator('#pendingCount').inner_text()=='19'
 for name,count in [('打包箱',2),('移动卫浴',1),('五金',2),('薄壁轻钢',1)]:
  page.get_by_role('button',name=name,exact=True).click()
  assert page.locator('article.card').count()==count,(name,page.locator('article.card').count())
 page.locator('#reset').click()
 page.locator('#status').select_option('partial')
 assert page.locator('article.card').count()==3
 page.locator('#reset').click()
 page.locator('#search').fill('NEWS-20260910-017')
 assert page.locator('article.card').count()==1
 page.locator('#reset').click()
 page.locator('#newsDate').select_option('2026-09-09')
 assert page.locator('article.card').count()==0
 assert '暂无收录' in page.locator('#empty').inner_text()
 page.locator('#newsDate').select_option('2026-09-10')
 assert page.locator('article.card').count()==25
 page.screenshot(path='outputs/daily-news-real-desktop.png',full_page=False)
 page.set_viewport_size({'width':390,'height':844})
 assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'),page.evaluate('document.documentElement.scrollWidth')
 page.screenshot(path='outputs/daily-news-real-mobile.png',full_page=False)
 assert not errors,errors
 print(json.dumps({'cards':25,'dateOptions':15,'productFilters':'passed','statusFilter':'passed','idSearch':'passed','emptyDate':'passed','mobileOverflow':False,'pageErrors':errors}))
 b.close()
