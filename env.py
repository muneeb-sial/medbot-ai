import os


def get_env(key: str) -> str:
    print("-"*50)
    env = os.environ.get(key)
    print(f"🔃 Loading environment variable {key}: {env}")
    print("-"*50)
    if not env:
        raise RuntimeError(f"{key} is not set in environment variables")
    return env