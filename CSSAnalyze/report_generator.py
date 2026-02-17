from collections import Counter, defaultdict
from config import CSS_FEATURES


def generate_summary_report(results):
    lines = []
    lines.append("="*80)
    lines.append("ИТОГОВЫЙ ОТЧЕТ: ИСПОЛЬЗОВАНИЕ СОВРЕМЕННЫХ CSS")
    lines.append("="*80)
    lines.append(f"Всего сайтов проанализировано: {results['total_sites']}")
    lines.append("")
    
    feature_usage = Counter()
    sites_using_features = defaultdict(list)
    
    for cat_name, cat_data in results['categories'].items():
        for site_name, site_data in cat_data['sites'].items():
            for feature_key, feature_info in site_data.get('features_summary', {}).items():
                feature_usage[feature_key] += 1
                sites_using_features[feature_key].append(site_name)
    
    lines.append("ОБЩАЯ СТАТИСТИКА ПО CSS-ВОЗМОЖНОСТЯМ")
    lines.append("-" * 80)
    lines.append("")
    
    for feature_key, feature_data in CSS_FEATURES.items():
        usage_count = feature_usage.get(feature_key, 0)
        percentage = (usage_count / results['total_sites'] * 100) if results['total_sites'] > 0 else 0
        
        lines.append(f"{feature_data['name']}")
        lines.append(f"   Описание: {feature_data['description']}")
        lines.append(f"   Использование: {usage_count}/{results['total_sites']} сайтов ({percentage:.1f}%)")
        
        if usage_count > 0:
            lines.append(f"   Сайты: {', '.join(sites_using_features[feature_key][:5])}")
        
        lines.append("")
    
    lines.append("")
    lines.append("="*80)
    lines.append("ДЕТАЛЬНЫЙ ОТЧЕТ ПО КАТЕГОРИЯМ")
    lines.append("="*80)
    
    for cat_name, cat_data in results['categories'].items():
        lines.append(f"\n{'#'*80}")
        lines.append(f"# {cat_name.upper()}")
        lines.append(f"{'#'*80}\n")
        
        for site_name, site_data in cat_data['sites'].items():
            lines.append(f"{site_name}")
            lines.append(f"   URL: {site_data['url']}")
            
            if site_data.get('error'):
                lines.append(f"   Ошибка: {site_data['error']}")
            else:
                lines.append(f"   Найдено современных возможностей: {site_data['total_features_found']}")
                
                if site_data.get('features_summary'):
                    for feature_key, feature_info in site_data['features_summary'].items():
                        lines.append(f"      {feature_info['name']}: {feature_info['total_occurrences']} упоминаний")
                else:
                    lines.append(f"      Современные CSS-возможности не обнаружены")
            
            lines.append("")
    
    return "\n".join(lines)
