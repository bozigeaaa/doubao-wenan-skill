import json
from pathlib import Path
from playwright.sync_api import sync_playwright
root=Path.cwd()
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless=True)
 page=browser.new_page(viewport={'width':1294,'height':912})
 errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto((root/'outputs/daily-news-2026-09-11.html').as_uri())
 expected={'verified':11,'all':18,'product':1,'unconfirmed':7}
 for value,count in expected.items():
  page.locator('#search').fill('no-matching-query')
  page.locator('[data-stat-filter="'+value+'"]').click()
  assert page.locator('#news .card').count()==count,(value,page.locator('#news .card').count())
  assert page.locator('#status').input_value()==value
  assert page.locator('.stat[aria-pressed="true"]').count()==1
  assert page.locator('#search').input_value()==''
  if value=='product': assert page.locator('#news-006').count()==1
 page.locator('#status').select_option('all')
 assert page.locator('[data-stat-filter="all"]').get_attribute('aria-pressed')=='true'
 page.locator('#reset').click()
 assert page.locator('#news .card').count()==11
 page.locator('[data-stat-filter="all"]').focus()
 page.keyboard.press('Enter')
 assert page.locator('#news .card').count()==18
 page.locator('#newsDate').select_option('2026-09-10')
 assert page.locator('#news .card').count()==25
 page.locator('[data-stat-filter="product"]').click()
 assert page.locator('#news .card').count()==int(page.locator('#productCount').inner_text())
 page.locator('#newsDate').select_option('2026-09-11')
 page.locator('[data-stat-filter="verified"]').click()
 page.screenshot(path=str(root/'outputs/news/stats-filter-desktop.png'))
 page.set_viewport_size({'width':390,'height':844})
 for value,count in expected.items():
  page.locator('[data-stat-filter="'+value+'"]').click()
  assert page.locator('#news .card').count()==count
 assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
 page.screenshot(path=str(root/'outputs/news/stats-filter-mobile.png'))
 assert not errors,errors
 print(json.dumps({'passed':True,'filterCounts':expected,'keyboard':True,'dateSwitch':True,'mobile':True,'pageErrors':errors}))
 browser.close()
