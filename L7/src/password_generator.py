import random
import string

class PasswordGenerator:
    def __init__(self, length: int = 10, charset: str = string.ascii_letters + string.digits, limit: int = 10):
        self.length = length
        self.charset = charset
        self.limit = limit
        self.generated = 0

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.generated >= self.limit:
            raise StopIteration
        self.generated += 1
        return "".join(random.choices(self.charset, k = self.length))
