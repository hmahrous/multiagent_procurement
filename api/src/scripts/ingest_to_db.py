import asyncio
import json
import os
import sys

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
import logging

from api.src.schemas.requests import MetaData
from api.src.services.vector_service import vector_store_faiss as vector_store


async def main():
    try:
        json_file_path = (
            "../../knowledge_base/big_software_process_new_request_no_risk.json"
        )
        with open(json_file_path, "r") as file:
            data = json.load(file)
        logging.info("Data loaded from file")
    except Exception as e:
        logging.error(f"Error loading data from file: {e}")
        raise e

    for pair in data:
        meta_data = [MetaData(page=page) for page in pair.keys()]
        try:
            await vector_store.store_chunks(pair.values(), meta_data)
            logging.info(f"Stored chunk with identifier {meta_data}")
        except Exception as e:
            logging.error(f"Error storing chunk with identifier {meta_data}: {e}")


if __name__ == "__main__":
    asyncio.run(main())
