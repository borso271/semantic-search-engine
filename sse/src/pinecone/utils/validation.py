import json

def validate_metadata(metadata: dict):
    """
    Validates metadata to ensure it conforms to Pinecone's requirements.
    """
    for key, value in metadata.items():
        if not isinstance(value, (str, int, float, bool, list)) or (
            isinstance(value, list) and not all(isinstance(item, str) for item in value)
        ):
            raise ValueError(f"Invalid metadata field '{key}': {value}")

def prepare_metadata(metadata: dict):
    """
    Prepares metadata by converting complex fields like dictionaries to JSON strings.
    """
    if "article" in metadata and isinstance(metadata["article"], dict):
        metadata["article"] = json.dumps(metadata["article"])
    return metadata
