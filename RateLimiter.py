import threading, sched, time
from Constants import *

class RateLimiter:
  bucket = 0
  s = sched.scheduler(time.time, time.sleep)
  current_event = None

  def bucket_filler(self):
    if self.bucket == BUCKET.CAPACITY:
      print(f"Bucket CAPACITY = {self.bucket} FULL")
    else:
      self.bucket += 1
      print(f"bucket current capacity = {self.bucket}")
    self.current_event = self.s.enter(BUCKET.FILL_INTERVAL, 1, self.bucket_filler)

  def start_filler(self):
    self.current_event = self.s.enter(BUCKET.FILL_INTERVAL, 1, self.bucket_filler)
    t = threading.Thread(target=self.s.run)
    t.start()
    print("Enabled: Bucket Filler")
    
  def stop_filler(self):
    if self.current_event:
      self.s.cancel(self.current_event)
      self.current_event = None
      print("Disabled: Bucket Filler")
      
  def remove_token(self):
    if self.bucket > 0:
      self.bucket -= 1
      print("Request Approved.")
    else:
      print("Request rate limited.")