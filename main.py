class HashMap:
    def __init__(self, m=8):
        """Initialize hash map with m buckets."""
        self.m = max(1, m)  # avoid 0 buckets
        self.buckets = [[] for _ in range(self.m)]
        self.count = 0

    def __len__(self):
        return self.count

    def _bucket_index(self, key):
        """Return the bucket index for a given key."""
        return hash(key) % self.m

    def _find_pair(self, bucket, key):
        """Return (index, pair) if found in the bucket, else (-1, None)."""
        for i, (k, v) in enumerate(bucket):
            if k == key:
                return i, (k, v)
        return -1, None

    def put(self, key, value):
        """Insert or update a key-value pair."""
        idx = self._bucket_index(key)
        bucket = self.buckets[idx]
        i, pair = self._find_pair(bucket, key)

        if pair is not None:
            bucket[i] = (key, value)
        else:
            bucket.append((key, value))
            self.count += 1

        # Resize when load factor exceeds 0.75
        if self.count / self.m > 0.75:
            self._resize(self.m * 2)

    def get(self, key):
        """Return value for key, or None if not found."""
        idx = self._bucket_index(key)
        bucket = self.buckets[idx]
        _, pair = self._find_pair(bucket, key)
        return pair[1] if pair else None

    def delete(self, key):
        """Remove key-value pair if present; return True if removed, else False."""
        idx = self._bucket_index(key)
        bucket = self.buckets[idx]
        i, pair = self._find_pair(bucket, key)

        if pair is None:
            return False

        del bucket[i]
        self.count -= 1
        return True

    def _resize(self, new_m):
        """Rehash all existing keys into a new bucket array."""
        old_items = []
        for bucket in self.buckets:
            old_items.extend(bucket)

        self.m = new_m
        self.buckets = [[] for _ in range(self.m)]
        self.count = 0

        for k, v in old_items:
            self.put(k, v)
