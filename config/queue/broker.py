from taskiq import InMemoryBroker

broker = InMemoryBroker()


@broker.task
async def process_document_job(name: str):
    print(f"Hello {name}")