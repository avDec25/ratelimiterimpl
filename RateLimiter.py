import threading, sched, time
from Buckets import Buckets
from Constants import *

class RateLimiter:
  buckets = Buckets()
    
  schedule = {}
  current_event = {}
  fill_rate_interval = {}
  fill_rate_token = {}
  

  def bucket_filler(self, key, ep):
    self.buckets.add_tokens(key, ep, self.fill_rate_token[(key, ep)])
    self.current_event[(key, ep)] = self.schedule[(key,ep)].enter(self.fill_rate_interval[(key, ep)], 1, self.bucket_filler, argument=(key, ep,))

  def start_bucket_filler(self, key, ep, max_cap, interval, token_count):
    self.buckets.add_bucket(key, ep, max_cap)
    self.schedule[(key,ep)] = sched.scheduler(time.time, time.sleep)
    self.current_event[(key,ep)] = None
    self.fill_rate_interval[(key,ep)] = interval
    self.fill_rate_token[(key,ep)] = token_count
    
    s = self.schedule[(key,ep)]
    print(s)
    print(self.fill_rate_interval[(key, ep)])
    self.current_event[(key,ep)] = s.enter(self.fill_rate_interval[(key, ep)], 1, self.bucket_filler, argument=(key, ep,))
    t = threading.Thread(target=s.run)
    t.start()
    print(f"Enabled: Bucket Filler for bucket({key},{ep})")
      
  def stop_bucket_filler(self, key, ep):
    if self.current_event[(key,ep)]:
      self.schedule[(key,ep)].cancel(self.current_event[(key, ep)])
      self.current_event[(key,ep)] = None
      print(f"Disabled: Bucket Filler for bucket({key},{ep})")
  
  def remove_token(self, key, ep):
    if self.buckets.remove_token(key, ep):
      print("Request Accepted")
    else:
      print("Request Rejected")
