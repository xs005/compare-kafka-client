import asyncio
from datetime import datetime

from aiokafka import AIOKafkaProducer

from comparison.kafkit.schema_registry import serialize_data


async def produce(row_num):
    # I have tried send_many, but got data loose.
    topic = 'kafkit_data0'
    producer = AIOKafkaProducer(bootstrap_servers='localhost:9092')
    await producer.start()
    try:
        serialized_key, serialized_value = await serialize_data(row_num=row_num)
        for key, value in zip(serialized_key, serialized_value):
            await producer.send_and_wait(topic=topic, value=value, key=key)
    finally:
        await producer.stop()


if __name__ == '__main__':
    row_num = 10000
    start = datetime.now()
    a = asyncio.run(produce(row_num=row_num))
    end = datetime.now()
    run_time = end - start
    print(f'Row: {row_num}; Run time: {run_time.total_seconds()} sec.')
