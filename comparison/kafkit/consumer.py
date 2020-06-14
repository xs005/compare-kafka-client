import asyncio

from aiokafka import AIOKafkaConsumer

from comparison.kafkit.schema_registry import deserialize_data


async def consume():
    topic = 'kafkit_data0'
    consumer = AIOKafkaConsumer(topic, bootstrap_servers='192.168.1.137:9092', group_id="kafkit-group1",
                                auto_offset_reset="earliest")
    await consumer.start()
    response = []

    try:
        async for msg in consumer:
            key = await deserialize_data(msg.key)
            value = await deserialize_data(msg.value)
            response.append((key, value))
            print(key, value)
    finally:
        await consumer.stop()
    return response


if __name__ == '__main__':
    output = asyncio.run(consume())
