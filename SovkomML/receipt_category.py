from transformers import pipeline
from collections import defaultdict

classifier = pipeline(
    task="zero-shot-classification",
    model="MoritzLaurer/mDeBERTa-v3-base-mnli-xnli",
    device=-1
)

categories = [
    "Косметика и парфюмерия", "Одежда и аксессуары ",
    "Электроника", "Ювелирные изделия",
    "Продукты", "Аптеки",
    "Интернет-магазины", "Такси и доставка",
    "Обувь", "Детские товары",
    "Кафе и рестораны", "Авто",
    "Заправки", "Красота",
    "Мебель и товары для дома", "Здоровье",
    "Спорт", "Страхование", "Товары для ремонта",
    "Товары для животных", "Путешествия ",
    "Услуги", "Подарки и развлечения", "Образование", "Разное",
]



def get_common_category(product_list, categories):
    category_stats = defaultdict(float)

    for product in product_list:
        result = classifier(product, categories, multi_label=False)
        best_category = result['labels'][0]
        confidence = result['scores'][0]

        category_stats[best_category] += confidence

    common_category = max(category_stats.items(), key=lambda x: x[1])[0]

    return common_category, dict(category_stats)


# products = [
#     'ПРОСТОКВАШИНО Сметана 15% 300г пл/ст (Да',
#     'Хлеб Крестьянский 2 сорт формовой 450г фл/п',
#     'Яйцо столовое С2 фас 10шт бокс:20',
#     'Крупа Гречневая 1с 800г :6',
#     'Кефир 1% 0,5л ф/п(Молочный кит)',
#     'Колбаса Печен лив 0,25кг мини мяс/пр(Атяшевск'
# ]
#
# common_category, stats = get_common_category(products, categories)
#
# print("Общая категория:", common_category)
# print("Статистика:")
# for cat, score in stats.items():
#     print(f"{cat}: {score:.2f}")
