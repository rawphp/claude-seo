#!/usr/bin/env python3
"""
Detailed image audit script for analyzing image optimization.
"""

import json
import sys
from playwright.sync_api import sync_playwright

def audit_images(url):
    """Audit all images on a page for optimization"""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 1920, 'height': 1080})
        page.goto(url, wait_until='networkidle', timeout=30000)

        # Extract detailed image information
        images = page.evaluate('''() => {
            const imgs = Array.from(document.querySelectorAll('img'));
            return imgs.map(img => {
                const rect = img.getBoundingClientRect();
                const styles = window.getComputedStyle(img);

                return {
                    src: img.src,
                    alt: img.alt || null,
                    title: img.title || null,
                    naturalWidth: img.naturalWidth,
                    naturalHeight: img.naturalHeight,
                    displayWidth: rect.width,
                    displayHeight: rect.height,
                    loading: img.loading || 'auto',
                    srcset: img.srcset || null,
                    sizes: img.sizes || null,
                    hasAltText: !!img.alt,
                    altTextLength: img.alt ? img.alt.length : 0,
                    inViewport: rect.top < window.innerHeight,
                    className: img.className,
                    id: img.id,
                    parent: img.parentElement ? img.parentElement.tagName : null,
                    parentClass: img.parentElement ? img.parentElement.className : null,
                    objectFit: styles.objectFit,
                    isLazyLoaded: img.loading === 'lazy',
                    isAboveFold: rect.top < window.innerHeight,
                    oversized: img.naturalWidth > rect.width * 2 || img.naturalHeight > rect.height * 2
                };
            });
        }''')

        # Get performance metrics
        performance = page.evaluate('''() => {
            const perf = performance.getEntriesByType('resource')
                .filter(r => r.initiatorType === 'img');
            return perf.map(p => ({
                name: p.name,
                size: p.transferSize,
                duration: p.duration
            }));
        }''')

        # Check for before/after images (common in lawn care sites)
        before_after = page.evaluate('''() => {
            const selectors = [
                '[class*="before"]',
                '[class*="after"]',
                '[alt*="before"]',
                '[alt*="after"]',
                '[alt*="Before"]',
                '[alt*="After"]'
            ];

            const found = [];
            selectors.forEach(sel => {
                const elements = document.querySelectorAll(sel);
                elements.forEach(el => {
                    if (el.tagName === 'IMG') {
                        found.push({
                            src: el.src,
                            alt: el.alt,
                            className: el.className,
                            type: sel.includes('before') ? 'before' : 'after'
                        });
                    } else {
                        const img = el.querySelector('img');
                        if (img) {
                            found.push({
                                src: img.src,
                                alt: img.alt,
                                className: img.className,
                                containerClass: el.className,
                                type: sel.includes('before') ? 'before' : 'after'
                            });
                        }
                    }
                });
            });
            return found;
        }''')

        # Check for trust signals
        trust_signals = page.evaluate('''() => {
            const selectors = [
                '[alt*="review"]',
                '[alt*="rating"]',
                '[alt*="star"]',
                '[alt*="testimonial"]',
                '[alt*="certification"]',
                '[alt*="award"]',
                '[alt*="guarantee"]',
                '[class*="review"]',
                '[class*="rating"]',
                '[class*="testimonial"]'
            ];

            const found = [];
            selectors.forEach(sel => {
                const elements = document.querySelectorAll(sel);
                elements.forEach(el => {
                    if (el.tagName === 'IMG') {
                        found.push({
                            type: 'trust_signal',
                            src: el.src,
                            alt: el.alt,
                            className: el.className
                        });
                    }
                });
            });
            return found;
        }''')

        browser.close()

        return {
            'url': url,
            'total_images': len(images),
            'images': images,
            'performance': performance,
            'before_after_images': before_after,
            'trust_signals': trust_signals,
            'statistics': {
                'with_alt_text': sum(1 for img in images if img['hasAltText']),
                'without_alt_text': sum(1 for img in images if not img['hasAltText']),
                'lazy_loaded': sum(1 for img in images if img['isLazyLoaded']),
                'above_fold': sum(1 for img in images if img['isAboveFold']),
                'oversized': sum(1 for img in images if img['oversized']),
                'with_srcset': sum(1 for img in images if img['srcset'])
            }
        }

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python image_audit.py <url>")
        sys.exit(1)

    url = sys.argv[1]
    data = audit_images(url)

    # Save to JSON
    with open('screenshots/image_audit.json', 'w') as f:
        json.dump(data, f, indent=2)

    print(f"Image Audit Complete!")
    print(f"Total Images: {data['total_images']}")
    print(f"\nStatistics:")
    for key, value in data['statistics'].items():
        print(f"  {key.replace('_', ' ').title()}: {value}")
    print(f"\nBefore/After Images Found: {len(data['before_after_images'])}")
    print(f"Trust Signals Found: {len(data['trust_signals'])}")
    print(f"\nDetailed results saved to screenshots/image_audit.json")
