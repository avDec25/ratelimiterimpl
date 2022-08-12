class Buckets:
  current_capacity = {}
  max_capacity = {}
  
  def add_bucket(self, key, ep, max_cap):
    if self.current_capacity[(key,ep)]:
      self.max_capacity[(key,ep)] = max(max_cap, self.max_capacity[(key,ep)])
    else:
      self.current_capacity[(key,ep)] = 0
      self.max_capacity[(key,ep)] = max_cap

  def bucket_capacity(self, key, ep):
    if (key, ep) in self.max_capacity:
      return self.current_capacity[(key, ep)]
    else:
      return None
  
  def remove_token(self, key, ep) -> bool:
    if self.bucket_capacity(key, ep) <= 0:
      print(f"Request rate limited because of bucket({key}, {ep}).")
      return False
    else:
      self.current_capacity[(key, ep)] -= 1
      return True

  def add_tokens(self, key, ep, count):
    if self.bucket_capacity(key, ep) + count > self.max_capacity[(key, ep)]:
      print(f"Bucket({key},{ep}) is FULL")
    else:
      self.current_capacity[(key, ep)] += count
      print(f"Bucket({key},{ep}) capacity = {self.bucket_capacity(key, ep)}")