from config.queue.sub import process_document_job

async def publish_document_job(name: str):
   await process_document_job.kiq(name=name)