from pathlib import Path

BASE_PATH = Path(__file__).parent
OUTPUT_JSON = f"{BASE_PATH}css_usage_analysis.json"
OUTPUT_TXT = f"{BASE_PATH}css_usage_report.txt"
VISUALIZATIONS_DIR = f"{BASE_PATH}css_visualizations"

WEBSITES = {
    "universities": {
        "МГУ": "https://www.msu.ru",
        "СПбГУ": "https://spbu.ru",
        "МФТИ": "https://mipt.ru",
        "ВШЭ": "https://www.hse.ru",
        "ИТМО": "https://itmo.ru",
        "МИСиС": "https://misis.ru",
        "МИФИ": "https://mephi.ru",
        "Бауманка": "https://bmstu.ru",
    },
    "web_courses": {
        "Яндекс Практикум": "https://practicum.yandex.ru",
        "Skillbox": "https://skillbox.ru",
        "GeekBrains": "https://geekbrains.ru",
        "HTML Academy": "https://htmlacademy.ru",
        "Нетология": "https://netology.ru",
        "Hexlet": "https://hexlet.io",
        "Stepik": "https://stepik.org",
        "Coursera": "https://coursera.org",
    }
}

CSS_FEATURES = {
    "container_queries": {
        "name": "CSS Container Queries",
        "patterns": [
            r'@container\s+',
            r'container-type:\s*\w+',
            r'container-name:\s*[\w-]+',
            r'container:\s*[\w\s/]+',
        ],
        "description": "Адаптивность на уровне компонентов",
    },
    
    "grid_subgrid": {
        "name": "CSS Grid Subgrid",
        "patterns": [
            r'grid-template-columns:\s*subgrid',
            r'grid-template-rows:\s*subgrid',
            r'grid-template:\s*subgrid',
        ],
        "description": "Вложенные grid-сетки",
    },
    
    "css_nesting": {
        "name": "CSS Nesting (native)",
        "patterns": [
            r'&\s*\{',
            r'&\s*:\w+',
            r'&\s*>\s*\w+',
            r'&\s*\.\w+',
        ],
        "description": "Нативная вложенность селекторов",
    },
    
    "css_layers": {
        "name": "CSS Cascade Layers",
        "patterns": [
            r'@layer\s+[\w-]+',
            r'@layer\s*\{',
        ],
        "description": "Управление каскадом через слои",
    },
    
    "has_selector": {
        "name": ":has() Selector",
        "patterns": [
            r':has\(',
        ],
        "description": "Родительский селектор",
    },
    
    "color_functions": {
        "name": "Modern Color Functions",
        "patterns": [
            r'oklch\(',
            r'oklab\(',
            r'lch\(',
            r'lab\(',
            r'color\(',
        ],
        "description": "Современные цветовые функции",
    }
}

FEATURE_COLORS = {
    'container_queries': '#FF6B6B',
    'grid_subgrid': '#4ECDC4',
    'css_nesting': '#45B7D1',
    'css_layers': '#FFA07A',
    'has_selector': '#98D8C8',
    'color_functions': '#F7DC6F'
}
