const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({
    headless: true,
    executablePath: '/usr/bin/chromium-browser'
  });
  const page = await browser.newPage();
  await page.goto('http://localhost:8090/');
  await page.waitForTimeout(3000);
  await page.screenshot({ path: '/home/j1coder/costforge-screenshot.png', fullPage: true });
  await browser.close();
  console.log('Screenshot saved!');
})();
