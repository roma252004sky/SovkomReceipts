import json

class ReceiptDTO:
    def __init__(self, json_data):
        self.shop = json.get('retailPlace', json.get('user'))
        self.total = json_data['totalSum'] / 100
        self.date = json_data['dateTime']
        self.items = ItemDTO.json_to_items(json_data["items"])
        self.load_id = None
        self.user_id = None
        self.category = None

    def __str__(self):
        items_str = "\n".join(str(item) for item in self.items)
        return f"Receipt from {self.shop}\nDate: {self.date}\nTotal: {self.total:.2f}\nItems:\n{items_str}"

    def to_json(self):
        receipt_dict = {
            "category": self.category,
            "load_id": self.load_id,
            "user_id": self.user_id,
            "shop": self.shop,
            "total": self.total,
            "date": self.date,
            "items": [item.to_json() for item in self.items]
        }
        return json.dumps(receipt_dict)


class ItemDTO:
    def __init__(self, json_data):
        self.name = json_data["name"]
        self.price = json_data["price"] / 100
        self.count = json_data["quantity"]
        self.total = json_data["sum"] / 100

    @staticmethod
    def json_to_items(json_items):
        return [ItemDTO(item) for item in json_items]

    def __str__(self):
        return f"- {self.name}: {self.count} x {self.price:.2f} = {self.total:.2f}"

    def to_json(self):
        return {
            "name": self.name,
            "price": self.price,
            "count": self.count,
            "total": self.total
        }
