class DGIM:
    def __init__(self, window_size):
        self.window_size = window_size
        self.buckets = []
        self.current_time = 0

    def add_bit(self, bit):
        if bit not in (0, 1):
            raise ValueError("Only bits 0 and 1 are allowed.")
        
        self.current_time += 1
        if bit == 1:
            self._add_one()
        
        # Remove old buckets
        self._remove_old_buckets()

    def _add_one(self):
        new_bucket = (self.current_time, 1)  # (timestamp, count of 1s)
        
        while self.buckets and self.buckets[-1][1] < new_bucket[1]:
            new_bucket = (self.buckets.pop()[0], new_bucket[1] + 1)
        
        self.buckets.append(new_bucket)

    def _remove_old_buckets(self):
        while self.buckets and self.buckets[0][0] <= self.current_time - self.window_size:
            self.buckets.pop(0)

    def count_ones(self):
        total_ones = 0
        for i in range(len(self.buckets)):
            total_ones += self.buckets[i][1]
        
        return total_ones

def main():
    window_size = int(input("Enter the size of the sliding window: "))
    dgim = DGIM(window_size)

    while True:
        bit = input("Enter a bit (0 or 1) or 'exit' to quit: ")
        if bit.lower() == 'exit':
            break
        try:
            bit = int(bit)
            dgim.add_bit(bit)
            print(f"Count of 1s in the last {window_size} bits: {dgim.count_ones()}")
        except ValueError as e:
            print(e)

if __name__ == "__main__":
    main()
