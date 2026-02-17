import asyncio
import json
from visualizer import CSSVisualizationGenerator
from website_crawler import WebsiteCSSCrawler
from report_generator import generate_summary_report
from config import OUTPUT_JSON, OUTPUT_TXT


def creat_report_and_vizualizations():
    crawler = WebsiteCSSCrawler()
    results = asyncio.run(crawler.analyze_all_websites())

    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    report = generate_summary_report(results)

    with open(OUTPUT_TXT, 'w', encoding='utf-8') as f:
         f.write(report)

    viz_gen = CSSVisualizationGenerator(OUTPUT_JSON)
    viz_gen.generate_all()

if __name__ == '__main__':
    creat_report_and_vizualizations()
