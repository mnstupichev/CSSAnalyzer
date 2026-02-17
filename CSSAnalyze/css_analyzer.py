import re
from collections import defaultdict
from config import CSS_FEATURES


class CSSAnalyzer:
    def __init__(self):
        self.features_found = defaultdict(list)
    
    def analyze_css(self, css_content, source_url):
        results = {
            "source": source_url,
            "total_lines": len(css_content.split('\n')),
            "total_chars": len(css_content),
            "features": {}
        }
        
        for feature_key, feature_data in CSS_FEATURES.items():
            found_instances = []
            
            for pattern in feature_data.get('patterns', []):
                matches = re.finditer(pattern, css_content, re.IGNORECASE | re.MULTILINE)
                
                for match in matches:
                    start = max(0, match.start() - 100)
                    end = min(len(css_content), match.end() + 100)
                    context = css_content[start:end].strip()
                    
                    line_num = css_content[:match.start()].count('\n') + 1
                    
                    found_instances.append({
                        "match": match.group(0),
                        "line": line_num,
                        "context": context[:200]
                    })
            
            if found_instances:
                results['features'][feature_key] = {
                    "name": feature_data['name'],
                    "count": len(found_instances),
                    "instances": found_instances[:5],
                    "description": feature_data['description']
                }
        
        return results
    
    def extract_inline_styles(self, html):
        inline_css = []
        
        style_pattern = r'<style[^>]*>(.*?)</style>'
        matches = re.finditer(style_pattern, html, re.DOTALL | re.IGNORECASE)
        
        for match in matches:
            inline_css.append(match.group(1))
        
        return '\n'.join(inline_css)
    
    def extract_css_links(self, html, base_url):
        from urllib.parse import urljoin
        
        css_links = []
        
        link_pattern = r'<link[^>]*rel=["\']stylesheet["\'][^>]*>'
        matches = re.finditer(link_pattern, html, re.IGNORECASE)
        
        for match in matches:
            link_tag = match.group(0)
            
            href_match = re.search(r'href=["\']([^"\']+)["\']', link_tag)
            if href_match:
                href = href_match.group(1)
                absolute_url = urljoin(base_url, href)
                css_links.append(absolute_url)
        
        return css_links
