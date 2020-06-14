import itertools
import os
from pathlib import Path

import aiohttp
from kafkit.registry.aiohttp import RegistryApi
from kafkit.registry.manager import RecordNameSchemaManager
from kafkit.registry.serializer import Deserializer

from comparison.utils import get_avro, generate_data


async def serialize_data(row_num):
    async with aiohttp.ClientSession() as http_session:
        schema_root = Path(os.path.join(os.path.dirname(os.path.dirname(__file__)), "avro_schemas"))

        registry_api = RegistryApi(
            session=http_session, url='http://localhost:8081'
        )
        suffix = '_v1'
        schema_manager = RecordNameSchemaManager(
            root=schema_root, registry=registry_api, suffix=suffix
        )
        await schema_manager.register_schemas(compatibility="FORWARD")
        key_avro, value_avro = get_avro(topic='example', suffix=suffix)
        df = generate_data(row_num=row_num)
        datas = df.to_dict('records')
        serialized_value = []
        serialized_key = []
        for counter, data in enumerate(datas):
            key_data = dict(itertools.islice(data.items(), 1))
            value_data = data
            value = await schema_manager.serialize(data=value_data, name=value_avro)
            key = await schema_manager.serialize(data=key_data, name=key_avro)

            serialized_key.append(key)
            serialized_value.append(value)

        return serialized_key, serialized_value


async def deserialize_data(serialized_msg):
    async with aiohttp.ClientSession() as http_session:
        registry_api = RegistryApi(
            session=http_session, url='http://192.168.1.137:8081'
        )
        deserializer = Deserializer(registry=registry_api)
        response = await deserializer.deserialize(serialized_msg)
        return response["message"]
