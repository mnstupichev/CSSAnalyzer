import asyncio
from crawl4ai import AsyncWebCrawler
from css_analyzer import CSSAnalyzer
from config import WEBSITES, CSS_FEATURES


class WebsiteCSSCrawler:
    def __init__(self):
        self.css_analyzer = CSSAnalyzer()
        self.results = {}
    
    async def fetch_css_file(self, crawler, url):
        try:
            result = await crawler.arun(
                url=url,
                bypass_cache=True,
                word_count_threshold=1
            )
            
            if result.success:
                return result.html
            
        except Exception:
            pass
        
        return ""
    
    async def analyze_website(self, crawler, name, url):
        site_results = {
            "name": name,
            "url": url,
            "inline_css": {},
            "external_css": [],
            "features_summary": {},
            "total_features_found": 0
        }
        
        try:
            result = await crawler.arun(
                url=url,
                bypass_cache=True,
                word_count_threshold=10,
                exclude_external_links=True
            )
            
            if not result.success:
                site_results['error'] = result.error_message
                return site_results
            
            inline_css = self.css_analyzer.extract_inline_styles(result.html)
            
            if inline_css:
                inline_analysis = self.css_analyzer.analyze_css(inline_css, f"{url} (inline)")
                site_results['inline_css'] = inline_analysis
            
            css_links = self.css_analyzer.extract_css_links(result.html, url)
            
            for css_url in css_links:
                css_content = await self.fetch_css_file(crawler, css_url)
                
                if css_content:
                    css_analysis = self.css_analyzer.analyze_css(css_content, css_url)
                    site_results['external_css'].append(css_analysis)
                
                await asyncio.sleep(0.5)
            
            all_features = set()
            
            if site_results['inline_css'].get('features'):
                all_features.update(site_results['inline_css']['features'].keys())
            
            for css_file in site_results['external_css']:
                if css_file.get('features'):
                    all_features.update(css_file['features'].keys())
            
            for feature_key in all_features:
                feature_name = CSS_FEATURES[feature_key]['name']
                total_count = 0
                
                if site_results['inline_css'].get('features', {}).get(feature_key):
                    total_count += site_results['inline_css']['features'][feature_key]['count']
                
                for css_file in site_results['external_css']:
                    if css_file.get('features', {}).get(feature_key):
                        total_count += css_file['features'][feature_key]['count']
                
                site_results['features_summary'][feature_key] = {
                    "name": feature_name,
                    "total_occurrences": total_count,
                    "description": CSS_FEATURES[feature_key]['description']
                }
            
            site_results['total_features_found'] = len(all_features)
        
        except Exception as e:
            site_results['error'] = str(e)
        
        return site_results
    
    async def analyze_all_websites(self):
        results = {
            "total_sites": 0,
            "categories": {}
        }
        
        async with AsyncWebCrawler(verbose=False) as crawler:
            
            for cat_name, websites in WEBSITES.items():
                
                category_results = {
                    "total_sites": len(websites),
                    "sites": {}
                }
                
                for site_name, site_url in websites.items():
                    site_result = await self.analyze_website(crawler, site_name, site_url)
                    category_results['sites'][site_name] = site_result
                    results['total_sites'] += 1
                    
                    await asyncio.sleep(1)
                
                results['categories'][cat_name] = category_results
        
        return results
