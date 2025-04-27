from flask import Flask, request, jsonify
import tempfile
import os

from ReceiptDTO import ReceiptDTO
from qr_scan import read_qr_qreader
from receipt_check_data import get_receipt_info
from receipt_category import get_common_category, categories

app = Flask(__name__)


@app.route('/process_receipt', methods=['POST'])
def process_receipt():
    # Проверяем наличие файла в запросе
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400

    # Сохраняем временный файл
    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
        file.save(temp_file.name)
        temp_path = temp_file.name

    try:
        # Чтение QR-кода
        qr_data = read_qr_qreader(temp_path)
        if not qr_data:
            return jsonify({'error': 'QR code not found'}), 400

        # Получение данных чека
        receipt_data = get_receipt_info(qr_data)
        if not receipt_data or 'items' not in receipt_data:
            return jsonify({'error': 'Failed to get receipt data'}), 500

        # Извлечение названий товаров
        products = [item["name"] for item in receipt_data["items"]]
        if not products:
            return jsonify({'error': 'No products found in receipt'}), 400

        # Определение категорий
        common_category, stats = get_common_category(products, categories)

        # Формирование результата
        result = {
            'qr_data': qr_data,
            'total_amount': receipt_data.get('totalSum', 0),
            'datetime': receipt_data.get('dateTime', ''),
            'products': products,
            'common_category': common_category,
            'category_stats': stats
        }

        return jsonify(result)

    except Exception as e:
        app.logger.error(f'Error processing receipt: {str(e)}')
        return jsonify({'error': str(e)}), 500

    finally:
        # Удаление временных файлов
        if os.path.exists(temp_path):
            os.remove(temp_path)


@app.route('/products', methods=['POST'])
def products():
    # Проверяем наличие файла в запросе
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400

    # Сохраняем временный файл
    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
        file.save(temp_file.name)
        temp_path = temp_file.name

    try:
        # Чтение QR-кода
        qr_data = read_qr_qreader(temp_path)
        if not qr_data:
            return jsonify({'error': 'QR code not found'}), 400

        # Получение данных чека
        receipt_data = get_receipt_info(qr_data)
        if not receipt_data or 'items' not in receipt_data:
            return jsonify({'error': 'Failed to get receipt data'}), 500

        ReceiptDTO(receipt_data)

        return ReceiptDTO(receipt_data).to_json()

    except Exception as e:
        app.logger.error(f'Error processing receipt: {str(e)}')
        return jsonify({'error': str(e)}), 500

    finally:
        # Удаление временных файлов
        if os.path.exists(temp_path):
            os.remove(temp_path)





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)