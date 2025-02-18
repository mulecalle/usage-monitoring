"""
Simple server to serve pools data
"""
from fastapi import FastAPI
import json5
import os
import uvicorn

app = FastAPI(title="Mock Pools Service")

@app.get('/pools')
async def get_pools():
    """Return pools data from json5 file"""
    file_path = os.path.join(os.path.dirname(__file__), 'pools.json5')
    with open(file_path, 'r') as f:
        data = json5.load(f)
    return data

def main():
    """Main entry point for mock server"""
    uvicorn.run(app, host="0.0.0.0", port=3000)

if __name__ == '__main__':
    main() 