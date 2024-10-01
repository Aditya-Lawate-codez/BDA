import math
from collections import deque

class DGIM:
    def __init__(self, window_size):
        self.window_size = window_size
        self.buckets = deque()  # Stores tuples (timestamp, bucket_size)
        self.current_time = 0  # Time increases as more bits are added
   
    def _expire_old_buckets(self):
        # Remove buckets that are outside the window
        while self.buckets and self.buckets[0][0] <= self.current_time - self.window_size:
            self.buckets.popleft()
   
    def add_bit(self, bit):
        self.current_time += 1
       
        # Add a new bucket if bit is 1
        if bit == 1:
            self.buckets.append((self.current_time, 1))
       
        # Merge buckets if there are more than two of the same size
        self._merge_buckets()
       
        # Remove expired buckets
        self._expire_old_buckets()
   
    def _merge_buckets(self):
        # We merge from the end of the deque (newest to oldest buckets)
        i = len(self.buckets) - 1
        while i > 0:
            if self.buckets[i][1] == self.buckets[i - 1][1]:
                # Merge the two oldest buckets of the same size
                merged_bucket = (self.buckets[i][0], self.buckets[i][1] * 2)
                self.buckets.pop()
                self.buckets.pop()
                self.buckets.append(merged_bucket)
            i -= 1
   
    def count_ones(self):
        # Sum the sizes of all buckets
        total_ones = 0
        if not self.buckets:
            return 0
       
        # We count all the buckets except the oldest one as they are fully in the window
        for i in range(len(self.buckets) - 1):
            total_ones += self.buckets[i][1]
       
        # The last bucket might be partially inside the window, so we approximate
        last_bucket_timestamp, last_bucket_size = self.buckets[-1]
        if last_bucket_timestamp > self.current_time - self.window_size:
            total_ones += last_bucket_size // 2  # Approximation
       
        return total_ones

# Example usage of DGIM algorithm:
window_size = 10  # Set the window size
dgim = DGIM(window_size)

# Simulate adding a stream of bits
stream = [1, 0, 1, 1, 0, 0, 1, 1, 0, 1]
for bit in stream:
    dgim.add_bit(bit)
    print(f"Stream: {stream[:dgim.current_time]}, Number of 1's in window: {dgim.count_ones()}")