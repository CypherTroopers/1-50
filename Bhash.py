import plyvel
import csv
import struct

def decode_block_body_key(key):
    """
    Decode the block body key to extract block number and hash.
    :param key: The key (bytes)
    :return: (block_number, block_hash) (tuple)
    """
    try:
        key_data = key[1:]

        block_number = struct.unpack(">Q", key_data[:8])[0]

        block_hash = key_data[8:].hex()

        return block_number, block_hash
    except struct.error:
        return None, None 

db = plyvel.DB('./chaindata', create_if_missing=False)

block_body_prefix = b'b'
start_block = 0
end_block = 50000

output_file = "block_bodies.csv"

with open(output_file, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Block Number", "Block Hash"])

    for key, value in db:
        try:
            if key.startswith(block_body_prefix):
                block_number, block_hash = decode_block_body_key(key)

                if block_number is not None and start_block <= block_number <= end_block:
                    writer.writerow([block_number, block_hash])

        except ValueError:
            continue  

db.close()

print(f"Block body hashes saved to {output_file}")
