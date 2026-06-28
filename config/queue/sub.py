from config.queue.broker import broker

@broker.task
async def process_document_job(name: str):
    print("🚧 Processing document job...")
    print(f"Hello {name}")
    print("✅ Processing document job completed...")