import string


class Base62:
    """A utility class for converting integers to Base-62 strings and vice versa."""

    ALPHABET = string.digits + string.ascii_letters  # Character set: 0-9a-zA-Z
    BASE = 62

    def __init__(self, fixed_length: int = 4):

        # Precomputed lookup dictionary for faster decoding
        self._char_to_index = {char: idx for idx,
                               char in enumerate(self.ALPHABET)}
        self.fixed_length = fixed_length

    def encode(self, num: int) -> str:
        """Convert an integer into a Base-62 encoded string."""

        if num <= 0:
            raise ValueError(
                "Only non-negative and non-zero integers are supported.")
        else:
            parts = []
            while num > 0:
                num, remainder = divmod(num, self.BASE)
                parts.append(self.ALPHABET[remainder])
            result = ''.join(reversed(parts))

        if len(result) > self.fixed_length:
            raise ValueError(
                f"Number {num} is too large for fixed length {self.fixed_length}")
        result = result.rjust(self.fixed_length, self.ALPHABET[0])

        return result

    def decode(self, encoded: str) -> int:
        """Convert a Base-62 encoded string back into an integer."""
        num = 0
        for char in encoded:
            num = num * self.BASE + self._char_to_index[char]
        return num


if __name__ == "__main__":
    # Example usage
    base62 = Base62()
    original_number = 123456
    encoded = base62.encode(original_number)
    decoded = base62.decode(encoded)

    print(f"Original number: {original_number}")
    print(f"Encoded string: {encoded}")
    print(f"Decoded number: {decoded}")
