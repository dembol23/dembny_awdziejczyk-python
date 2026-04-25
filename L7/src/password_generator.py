import random
import string

class PasswordGenerator:
    def __init__(self, length: int = 10, charset: str = string.ascii_letters + string.digits, count: int = 10):
        self.length = length
        self.charset = charset
        self.max = count
        self.count = 0

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.count >= self.max:
            raise StopIteration
        self.count += 1
        return "".join(random.choices(self.charset, k = self.length))
