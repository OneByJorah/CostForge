#!/usr/bin/env python3
"""Capture CostForge dashboard screenshots using Playwright.

Usage:
    python scripts/capture-screenshots.py

Prerequisites:
    pip install playwright
    python -m playwright install chromium

This script captures screenshots of the CostForge dashboard and saves them
to docs/screenshots/ for use in the README.
"""
from playwright.sync_api import sync_playwright
import time
import subprocess
import sys

SCREENSHOT_DIR = "/home/j1coder/github-repos/CostForge/docs/screenshots"
BASE_URL = "http://localhost:8090"

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
            page.goto(BASE_URL, wait_until="networkidle", timeout=30000)
            page.wait_for_load_state("networkidle")
            
            if screenshot["scroll"] > 0:
                page.evaluate(f"window.scrollTo(0, {screenshot['scroll']})")
                time.sleep(1)
            
            page.screenshot(path=screenshot["path"], full_page=False)
            print(f"Saved: {screenshot['path']}")
        
        browser.close()
    
    print("\nAll screenshots captured successfully!")

if __name__ == "__main__":
    capture_screenshots()
