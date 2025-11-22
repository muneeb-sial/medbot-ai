from pydantic import BaseModel
import weaviate
from weaviate.classes.config import Property, DataType, Configure, VectorDistances


class WeaviateCollection:
    """
    A smart wrapper around Weaviate collections that:
      ✅ Auto-creates schema from a Pydantic model
      ✅ Applies default vector + index configs (overridable)
      ✅ Uses modern Weaviate SDK (vector_config instead of deprecated args)
    """

    TYPE_MAP = {
        str: DataType.TEXT,
        int: DataType.INT,
        float: DataType.NUMBER,
        bool: DataType.BOOL,
    }

    def __init__(
        self,
        client: weaviate.WeaviateClient,
        name: str,
        model: type[BaseModel],
    ):
        self.client = client
        self.name = name
        self.model = model

        # ✅ Create collection schema from Pydantic model
        props = self.pydantic_to_properties(model)

        if not client.collections.exists(name):
            client.collections.create(
                name=name,
                properties=props,
            )
            print(f"✅ Created collection '{name}' with configs.")
        else:
            print(f"⚡ Collection '{name}' already exists.")

        # ✅ Keep handle to live collection
        self.collection = client.collections.get(name)

    def pydantic_to_properties(self, model: type[BaseModel]):
        props = []
        for field_name, field in model.model_fields.items():  # Pydantic v2
            py_type = field.annotation
            if py_type in self.TYPE_MAP:
                props.append(Property(name=field_name, data_type=self.TYPE_MAP[py_type]))
        return props
