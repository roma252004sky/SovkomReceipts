import os
import tempfile
from confluent_kafka import Consumer, Producer, KafkaException
from ReceiptDTO import ReceiptDTO
from qr_scan import read_qr_qreader
from receipt_check_data import get_receipt_info
from receipt_category import get_common_category, categories


class ReceiptProcessor:
    def __init__(self, kafka_config):
        self.consumer = Consumer(kafka_config)
        self.producer = Producer(kafka_config)

    def _delivery_report(self, err, msg):
        """Callback-функция для обработки отчетов о доставке"""
        if err is not None:
            print(f'Message delivery failed: {err}')
        else:
            print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

    def process_message(self, message):
        """Обработка одного сообщения из Kafka"""
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
                temp_file.write(message.value())
                temp_path = temp_file.name

            try:
                qr_data = read_qr_qreader(temp_path)
                if not qr_data:
                    print("QR code not found in image")
                    return None

                receipt_data = get_receipt_info(qr_data)
                if not receipt_data or 'items' not in receipt_data:
                    print("Failed to get receipt data from QR")
                    return None

                receipt_dto = ReceiptDTO(receipt_data)

                products = [item.name for item in receipt_dto.items]
                common_category, stats = get_common_category(products, categories)
                receipt_dto.category = common_category

                headers = dict(message.headers()) if message.headers() else {}
                user_id = headers.get('userId', b'').decode('utf-8')
                load_id = headers.get('loadId', b'').decode('utf-8')

                receipt_dto.user_id = user_id
                receipt_dto.load_id = load_id

                payload = receipt_dto.to_json().encode('utf-8')

                self.producer.produce(
                    topic='postOCR',
                    value=payload,
                    callback=self._delivery_report
                )
                self.producer.poll(0)

                return {
                    'user_id': user_id,
                    'load_id': load_id,
                    'status': 'processed'
                }

            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)

        except Exception as e:
            print(f"Error processing receipt: {str(e)}")
            return None

    def consume_loop(self, topics):
        """Основной цикл потребления сообщений"""
        self.consumer.subscribe(topics)

        try:
            while True:
                msg = self.consumer.poll(timeout=1.0)
                if msg is None:
                    self.producer.flush()
                    continue

                if msg.error():
                    if msg.error().code() == KafkaException._PARTITION_EOF:
                        continue
                    else:
                        print(f"Consumer error: {msg.error()}")
                        continue

                print(f"Received message from {msg.topic()} [{msg.partition()}]")
                result = self.process_message(msg)
                if result:
                    print(f"Processed receipt for user {result['user_id']}, load {result['load_id']}")

        except KeyboardInterrupt:
            print("Shutting down consumer...")
        finally:
            self.consumer.close()
            self.producer.flush(10) 

if __name__ == '__main__':
    kafka_config = {
        'bootstrap.servers': 'kafka-1:9092,kafka-2:9092,kafka-3:9092',
        'group.id': 'receipt-processor-group',
        'auto.offset.reset': 'earliest',
        'message.max.bytes': 104857600,
    }

    processor = ReceiptProcessor(kafka_config)
    processor.consume_loop(['preOCR'])
