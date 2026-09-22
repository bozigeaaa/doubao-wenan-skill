import json
from pathlib import Path
from playwright.sync_api import sync_playwright
root=Path.cwd()
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless=True)
 page=b.new_page(viewport={'width':1294,'height':912})
 errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto((root/'outputs/daily-news-2026-09-14.html').as_uri())
 assert page.locator('#newsDate').input_value()=='2026-09-14'
 assert page.locator('#newsDate option').count()==15
 for status,count in {'verified':10,'all':13,'product':1,'unconfirmed':3}.items():
  page.locator('[data-stat-filter="'+status+'"]').click()
  assert page.locator('#news .card').count()==count
 page.locator('#news-011 .proof-trigger').hover()
 assert '仍缺少的证据' in page.locator('#proofPopover').inner_text()
 page.mouse.move(1,1)
 page.locator('[data-stat-filter="product"]').click()
 page.locator('#news-001 .proof-trigger').hover()
 assert '核验时间' in page.locator('#proofPopover').inner_text()
 page.mouse.move(1,1)
 page.evaluate("Object.defineProperty(navigator,'clipboard',{value:{writeText:async t=>{window.copiedNews=t}}})")
 page.locator('[data-copy="001"]').click()
 copied=page.evaluate('window.copiedNews')
 assert 'NEWS-20260914-001' in copied and '打包箱' in copied and '2026-09-14T' in copied
 page.locator('[data-usage="001"]').click()
 assert page.locator('#usagePanel input').count()==4
 page.locator('[data-usage-option="移动卫浴"]').check()
 assert '已用 1/4' in page.locator('[data-usage="001"]').inner_text()
 page.locator('[data-usage-option="移动卫浴"]').uncheck()
 page.keyboard.press('Escape')
 page.locator('#newsDate').select_option('2026-09-11')
 page.locator('[data-stat-filter="verified"]').click()
 assert page.locator('#news .card').count()==11
 page.locator('#newsDate').select_option('2026-09-13')
 assert page.locator('#news .card').count()==0
 page.locator('#newsDate').select_option('2026-09-14')
 assert page.locator('#news .card').count()==10
 page.screenshot(path=str(root/'outputs/news/evidence-2026-09-14/report-desktop.png'))
 page.set_viewport_size({'width':390,'height':844})
 assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
 page.screenshot(path=str(root/'outputs/news/evidence-2026-09-14/report-mobile.png'))
 assert not errors,errors
 result={'passed':True,'total':13,'verified':10,'unconfirmed':3,'product':1,'proofPopup':True,'copy':True,'usage':True,'dateSwitch':True,'noFabricatedWeekendReport':True,'mobile':True,'pageErrors':errors}
 (root/'outputs/news/evidence-2026-09-14/qa-result.json').write_text(json.dumps(result),encoding='utf-8')
 print(json.dumps(result))
 b.close()
