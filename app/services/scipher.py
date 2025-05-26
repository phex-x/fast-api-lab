import heapq
from collections import defaultdict

from app.schemas.scipher import ToEncode, Result


def build_huffman_tree(freq):
    heap = [[weight, [char, ""]] for char, weight in freq.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])

    return heap[0][1:]


def get_huffman_codes(text):
    freq = defaultdict(int)
    for char in text:
        freq[char] += 1

    tree = build_huffman_tree(freq)
    return {char: code for char, code in tree}


def huffman_encode(text, codes):
    return ''.join([codes[char] for char in text])


def xor_encrypt(text: str, key: str) -> str:
    encrypted = []
    key_len = len(key)
    for i, char in enumerate(text):
        encrypted_char = ord(char) ^ ord(key[i % key_len])
        encrypted.append(chr(encrypted_char))
    return ''.join(encrypted)


def calculate_padding(bit_string: str) -> int:
    remainder = len(bit_string) % 8
    return (8 - remainder) % 8


def scipher(toencode : ToEncode) -> Result:
    huffman_codes = get_huffman_codes(toencode.text)
    encoded_data = xor_encrypt(huffman_encode(toencode.text, huffman_codes), toencode.key)
    padding = calculate_padding(huffman_encode(toencode.text, huffman_codes))

    return Result(
        encoded_data=encoded_data,
        key = toencode.key,
        huffman_codes=huffman_codes,
        padding=padding
    )
