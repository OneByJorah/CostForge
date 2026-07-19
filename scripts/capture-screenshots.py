#!/usr/bin/env python3
"""Capture CostForge dashboard screenshots using Playwright.

Usage:
    python scripts/capture-screenshots.py

Prerequisites:
    pip install playwright
    python -m playwright install chromium

Environment Variables:
    COSTFORGE_URL: Base URL (default: http://localhost:8090)
    SCREENSHOT_DIR: Output directory (default: docs/screenshots)
"""
from playwright.sync_api import sync_playwright
import time
import os

# Configurable via environment variables
BASE_URL = os.environ.get("COSTFORGE_URL", "http://localhost:8090")
SCREENSHOT_DIR = os.environ.get("SCREENSHOT_DIR", "docs/screenshots")

# Ensure screenshot directory exists
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

def capture_screenshots():
    """Capture CostForge dashboard screenshots."""
    screenshots = [
        {"path": f"{SCREENSHOT_DIR}/dashboard.png", "scroll": 0, "name": "dashboard"},
        {"path": f"{SCREENSHOT_DIR}/comparison.png", "scroll": 500, "name": "comparison"},
        {"path": f"{SCREENSHOT_DIR}/providers.png", "scroll": 1000, "name": "providers"},
    ]
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        
        for screenshot in screenshots:
            print(f"Capturing {screenshot['name']}...")
            try:
                page.goto(BASE_URL, wait_until="networkidle", timeout=30000)
                
                if screenshot["scroll"] > 0:
                    page.evaluate(f"window.scrollTo(0, {screenshot['scroll']})")
                    time.sleep(1)
                
                page.screenshot(path=screenshot["path"], full_page=False)
                
                # Validate screenshot size (should be >10KB)
                file_size = os.path.getsize(screenshot["path"])
                if file_size < 10240:
                    print(f"Warning: {screenshot['name']} is only {file_size} bytes - may be blank")
                else:
                    print(f"Saved: {screenshot['path']} ({file_size:,} bytes)")
            except Exception as e:
                print(f"Error capturing {screenshot['name']}: {e}")
                raise
        
        browser.close()
    
    print("\nAll screenshots captured successfully!")

if __name__ == "__main__":
    capture_screenshots()
