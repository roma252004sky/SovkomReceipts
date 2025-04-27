import cv2
from qreader import QReader

_QREADER_INSTANCE = QReader(model_size="s")


def read_qr_qreader(image_path: str) -> str:
    """Чтение QR-кода через QReader (требует TensorFlow)"""
    qreader = QReader()
    img = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)
    return _QREADER_INSTANCE.detect_and_decode(image=img)[0]

# Установка:
# pip install qreader

# Пример использования
# result = read_qr_qreader("products.jpg")
# print(f"Результат: {result}" if result else "QR-код не найден")