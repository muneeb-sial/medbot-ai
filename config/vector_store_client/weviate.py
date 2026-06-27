import weaviate

weviate_db_client = weaviate.connect_to_local()
if weviate_db_client.is_ready():
    print("✅ Weaviate instance is ready")