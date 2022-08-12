from typing import Union
from RateLimiter import RateLimiter

from fastapi import FastAPI

app = FastAPI()
rate_limiter = RateLimiter()

@app.get("/filler/start")
def read_root():
  rate_limiter.start_filler()
  return {"message": "Started"}

@app.get("/filler/stop")
def read_root():
  rate_limiter.stop_filler()
  return {"message": "Stopped"}

@app.get("/test/ratelimit")
def read_root():
  rate_limiter.remove_token()
  return {"message": "Token Removed"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}
