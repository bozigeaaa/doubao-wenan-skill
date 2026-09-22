from playwright.sync_api import sync_playwright
import json
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=r'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless=True)
 page=b.new_page(viewport={'width':1280,'height':900})
 errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto('http://127.0.0.1:62436/',wait_until='networkidle')
 trigger=page.locator('#accessTrigger')
 panel=page.locator('.access-popover')
 assert not panel.is_visible()
 assert page.locator('article.card').count()==25
 a=trigger.bounding_box();d=page.locator('.edition').bounding_box()
 assert a['x']+a['width']<d['x']
 page.screenshot(path='outputs/news-access-closed.png')
 trigger.hover()
 assert panel.is_visible()
 assert page.locator('#channels tbody tr').count()==8
 assert trigger.get_attribute('aria-expanded')=='true'
 panel.hover()
 assert panel.is_visible()
 page.screenshot(path='outputs/news-access-open.png')
 page.mouse.move(30,350)
 assert not panel.is_visible()
 page.locator('#newsDate').select_option('2026-09-09')
 trigger.hover()
 assert '该日期暂无收集与访问记录' in page.locator('#channelSummary').inner_text()
 assert not page.locator('#channels .tablewrap').is_visible()
 page.mouse.move(30,350)
 page.locator('#newsDate').select_option('2026-09-10')
 page.set_viewport_size({'width':390,'height':844})
 trigger.hover()
 assert panel.is_visible()
 assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
 page.screenshot(path='outputs/news-access-mobile.png')
 assert not errors,errors
 print(json.dumps({'position':'left of date','default':'hidden','hover':'visible','panelHover':'stays visible','mouseleave':'hidden','rows':8,'news':25,'dateState':'passed','mobileOverflow':False,'errors':errors}))
 b.close()
