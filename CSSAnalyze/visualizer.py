import json
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from collections import Counter, defaultdict
import os

from config import FEATURE_COLORS, VISUALIZATIONS_DIR


plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")


class CSSVisualizationGenerator:

    def __init__(self, json_file_path):
        with open(json_file_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        
        self.output_dir = VISUALIZATIONS_DIR
        os.makedirs(self.output_dir, exist_ok=True)
        
        self.prepare_data()
    
    def prepare_data(self):
        self.feature_stats = Counter()
        self.category_stats = defaultdict(lambda: defaultdict(int))
        self.site_features = {}
        
        for cat_name, cat_data in self.data['categories'].items():
            for site_name, site_data in cat_data['sites'].items():
                
                if site_data.get('error'):
                    continue
                
                site_features = set()
                
                for feature_key, feature_info in site_data.get('features_summary', {}).items():
                    self.feature_stats[feature_key] += 1
                    self.category_stats[cat_name][feature_key] += 1
                    site_features.add(feature_key)
                
                self.site_features[f"{cat_name}:{site_name}"] = site_features
        
        self.total_sites = self.data['total_sites']
    
    def create_pie_chart(self):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
        
        if self.feature_stats:
            features = list(self.feature_stats.keys())
            counts = [self.feature_stats[f] for f in features]
            percentages = [(c / self.total_sites * 100) for c in counts]

            labels = [self._get_feature_name(f) for f in features]
            colors = [FEATURE_COLORS.get(f, '#95A5A6') for f in features]

            ax1.pie(
                percentages,
                labels=labels,
                colors=colors,
                autopct='%1.1f%%',
                startangle=90,
                textprops={'fontsize': 10, 'weight': 'bold'}
            )

            ax1.set_title('Процент сайтов, использующих современные CSS-технологии\n' + 
                         f'(из {self.total_sites} проанализированных)',
                         fontsize=13, weight='bold', pad=20)
        else:
            ax1.text(0.5, 0.5, 'Нет данных', ha='center', va='center', fontsize=14)
            ax1.set_title('Использование CSS-технологий', fontsize=13, weight='bold')
        
        sites_with_features = len([s for s in self.site_features.values() if s])
        sites_without = self.total_sites - sites_with_features
        
        if sites_with_features > 0 or sites_without > 0:
            ax2.pie(
                [sites_with_features, sites_without],
                labels=['С современными CSS', 'Без современных CSS'],
                colors=['#2ECC71', '#E74C3C'],
                autopct='%1.1f%%',
                startangle=90,
                textprops={'fontsize': 11, 'weight': 'bold'}
            )
            ax2.set_title(f'Внедрение современных CSS-возможностей\n' +
                         f'({sites_with_features} из {self.total_sites} сайтов)',
                         fontsize=13, weight='bold', pad=20)
        
        plt.tight_layout()
        output_path = f'{self.output_dir}/pie_charts.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return output_path
    
    def create_bar_chart(self):
        fig, ax = plt.subplots(figsize=(14, 8))
        
        categories = list(self.category_stats.keys())
        
        all_features = set()
        for cat_features in self.category_stats.values():
            all_features.update(cat_features.keys())
        
        all_features = sorted(all_features)
        
        x = np.arange(len(categories))
        width = 0.15
        
        for i, feature in enumerate(all_features):
            counts = [self.category_stats[cat].get(feature, 0) for cat in categories]
            offset = width * (i - len(all_features) / 2)
            
            bars = ax.bar(
                x + offset,
                counts,
                width,
                label=self._get_feature_name(feature),
                color=FEATURE_COLORS.get(feature, '#95A5A6')
            )
            
            for bar in bars:
                height = bar.get_height()
                if height > 0:
                    ax.text(
                        bar.get_x() + bar.get_width() / 2.,
                        height,
                        f'{int(height)}',
                        ha='center',
                        va='bottom',
                        fontsize=9,
                        weight='bold'
                    )
        
        ax.set_xlabel('Категории', fontsize=12, weight='bold')
        ax.set_ylabel('Количество сайтов', fontsize=12, weight='bold')
        ax.set_title('Использование CSS-технологий по категориям',
                    fontsize=14, weight='bold', pad=20)
        ax.set_xticks(x)
        ax.set_xticklabels([c.replace('_', ' ').title() for c in categories])
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=10, frameon=True)
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        output_path = f'{self.output_dir}/bar_chart.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return output_path
    
    def create_horizontal_bar(self):
        site_scores = {}
        
        for site_key, features in self.site_features.items():
            cat_name, site_name = site_key.split(':', 1)
            site_scores[site_name] = len(features)
        
        sorted_sites = sorted(site_scores.items(), key=lambda x: x[1], reverse=True)
        
        if not sorted_sites:
            return None
        
        top_sites = sorted_sites[:15]
        
        sites = [s[0] for s in top_sites]
        scores = [s[1] for s in top_sites]
        
        colors = plt.cm.RdYlGn(np.linspace(0.3, 0.9, len(sites)))
        
        fig, ax = plt.subplots(figsize=(12, max(8, len(sites) * 0.5)))
        
        bars = ax.barh(sites, scores, color=colors)
        
        for i, (bar, score) in enumerate(zip(bars, scores)):
            ax.text(
                score + 0.1,
                bar.get_y() + bar.get_height() / 2,
                f'{score}',
                va='center',
                fontsize=10,
                weight='bold'
            )
        
        ax.set_xlabel('Количество используемых современных CSS-технологий',
                     fontsize=11, weight='bold')
        ax.set_title('Топ сайтов по использованию современных CSS-возможностей',
                    fontsize=14, weight='bold', pad=20)
        ax.grid(axis='x', alpha=0.3)
        
        plt.tight_layout()
        output_path = f'{self.output_dir}/site_ranking.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return output_path
    
    def create_comparison_chart(self):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
        
        category_avg = {}
        
        for cat_name, cat_data in self.data['categories'].items():
            total_features = 0
            valid_sites = 0
            
            for site_name, site_data in cat_data['sites'].items():
                if not site_data.get('error'):
                    total_features += site_data.get('total_features_found', 0)
                    valid_sites += 1
            
            if valid_sites > 0:
                category_avg[cat_name] = total_features / valid_sites
        
        if category_avg:
            categories = [c.replace('_', ' ').title() for c in category_avg.keys()]
            averages = list(category_avg.values())
            colors_cat = ['#3498DB', '#E74C3C', '#2ECC71', '#F39C12'][:len(categories)]
            
            bars = ax1.bar(categories, averages, color=colors_cat)
            ax1.set_ylabel('Среднее количество технологий', fontsize=11, weight='bold')
            ax1.set_title('Средняя технологичность по категориям',
                         fontsize=12, weight='bold')
            ax1.grid(axis='y', alpha=0.3)
            
            for bar in bars:
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.1f}', ha='center', va='bottom', fontsize=10, weight='bold')
        
        category_adoption = {}
        
        for cat_name, cat_data in self.data['categories'].items():
            sites_with_css = 0
            total_sites = 0
            
            for site_name, site_data in cat_data['sites'].items():
                if not site_data.get('error'):
                    total_sites += 1
                    if site_data.get('total_features_found', 0) > 0:
                        sites_with_css += 1
            
            if total_sites > 0:
                category_adoption[cat_name] = (sites_with_css / total_sites) * 100
        
        if category_adoption:
            categories = [c.replace('_', ' ').title() for c in category_adoption.keys()]
            percentages = list(category_adoption.values())
            
            bars = ax2.bar(categories, percentages, color=colors_cat)
            ax2.set_ylabel('Процент внедрения (%)', fontsize=11, weight='bold')
            ax2.set_title('Процент сайтов с современными CSS',
                         fontsize=12, weight='bold')
            ax2.set_ylim(0, 100)
            ax2.grid(axis='y', alpha=0.3)
            
            for bar in bars:
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.1f}%', ha='center', va='bottom', fontsize=10, weight='bold')
        
        plt.tight_layout()
        output_path = f'{self.output_dir}/category_comparison.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return output_path
    
    def _get_feature_name(self, feature_key):
        names = {
            'container_queries': 'Container Queries',
            'grid_subgrid': 'Grid Subgrid',
            'css_nesting': 'CSS Nesting',
            'css_layers': 'Cascade Layers',
            'has_selector': ':has() Selector',
            'color_functions': 'Modern Colors'
        }
        return names.get(feature_key, feature_key.replace('_', ' ').title())
    
    def generate_all(self):
        generated_files = []
        
        try:
            file = self.create_pie_chart()
            if file: generated_files.append(file)
        except Exception:
            pass
        
        try:
            file = self.create_bar_chart()
            if file: generated_files.append(file)
        except Exception:
            pass
        
        try:
            file = self.create_horizontal_bar()
            if file: generated_files.append(file)
        except Exception:
            pass
        
        try:
            file = self.create_comparison_chart()
            if file: generated_files.append(file)
        except Exception:
            pass
        
        return generated_files
