from config.queue.broker import broker
from jobs.insert_one import insert_one_with_filepath

@broker.task
async def process_document_job(name: str):
    print("🚧 Processing document job...")
    await insert_one_with_filepath(name)
    print(f"Hello {name}")
    print("✅ Processing document job completed...")