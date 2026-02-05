from fastapi import Header, HTTPException, Security
from fastapi.security import APIKeyHeader
import os

API_KEY_NAME = "x-api-key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# Ideally, this should be in an environment variable. 
# For prototype, we can check against a hardcoded list or allow any non-empty key if specified, 
# but the prompt says "Your API must validate an API Key".
# We'll expect a specific key or list of keys. Let's start with a default for testing.
VALID_API_KEYS = {
    "sk_test_123456789", 
    "human_or_ai_secret_key"
}

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if not api_key_header:
         raise HTTPException(
            status_code=401,
            detail="Missing API Key"
        )
    
    if api_key_header not in VALID_API_KEYS:
        raise HTTPException(
            status_code=403,
            detail="Invalid API Key"
        )
    return api_key_header
