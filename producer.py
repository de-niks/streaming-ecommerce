import json
import time
from datetime import datetime
import random

from faker import Faker
from confluent_kafka import SerializingProducer

faker = Faker()


def generate_sales_transaction():
    user = faker.simple_profile()

    return {
        'transactionId': faker.uuid4(),
        'productId': random.choice(['product1', 'product2', 'product3', 'product4', 'product5', 'product6']),
        'productName': random.choice(['laptop', 'mobile', 'tablet', 'headphone', 'watch', 'speaker']),
        'productCategory': random.choice(['electronics', 'grocery', 'fashion', 'home']),
        'productPrice': round(random.uniform(10, 1000), 2),
        'productQuantity': random.randint(1, 10),
        'productBrand': random.choice(['apple', 'samsung', 'beat', 'mi']),
        'currency': random.choice(['USD', 'GBP']),
        'customerId': user['username'],
        'transactionDate': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
        'paymentMethod': random.choice(['credit_card', 'debit_card', 'online_transfer'])
    }


def main():
    topic = 'financial_transaction'
    producer = SerializingProducer({
        'bootstrap.servers': 'localhost:9092'
    })

    current_time = datetime.now()

    while (datetime.now() - current_time).seconds < 300:
        try:
            transaction = generate_sales_transaction()
            transaction['totalAmount'] = transaction['productQuantity'] * transaction['productPrice']
            producer.produce(
                topic,
                key=transaction['transactionId'],
                value=json.dumps(transaction),
                on_delivery=delivery_report
            )
            producer.poll(0)
            time.sleep(5)


        except BufferError:
            print('Buffer full ! .. waiting')
            time.sleep(10)
        except Exception as e:
            print(e)


def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed : {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')


if __name__ == "__main__":
    main()
