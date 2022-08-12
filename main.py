from typing import Union
from RateLimiter import RateLimiter

from fastapi import FastAPI

app = FastAPI()
rate_limiter = RateLimiter()

@app.get("/filler/start")
def start_rule(key: str, ep: str, max_cap: int, interval: int, token_count: int):
  rate_limiter.start_bucket_filler(key, ep, max_cap, interval, token_count)
  return {"message": "Started"}

@app.get("/filler/stop")
def end_rule(key: str, ep: str):
  rate_limiter.stop_bucket_filler(key, ep)
  return {"message": "Stopped"}


@app.get("/test/ratelimit")
def hit_api(key: str, ep: str):
  print(f"API key({key}), endPoint({ep})")
  rate_limiter.remove_token(key, ep)
  return {"message": "Token Removed"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}
