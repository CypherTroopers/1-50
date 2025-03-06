import plyvel
import csv
import struct

def decode_header_key(key):
    """
    Decode the block header key to extract block number and header hash.
    :param key: The key (bytes)
    :return: (block_number, header_hash) (tuple)
    """
    try:
        key_data = key[1:]  # 'h' 
        block_number = struct.unpack(">Q", key_data[:8])[0] 
        header_hash = key_data[8:].hex() 
        return block_number, header_hash
    except struct.error:
        return None, None 

db = plyvel.DB('./chaindata', create_if_missing=False)

header_prefix = b'h'
start_block = 0
end_block = 50000
output_file = "block_headers.csv"

with open(output_file, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Block Number", "Header Hash"])

    for key, value in db:
        try:
            if key.startswith(header_prefix):
                block_number, header_hash = decode_header_key(key)

                if block_number is not None and start_block <= block_number <= end_block:
                    writer.writerow([block_number, header_hash])

        except ValueError:
            continue

db.close()
print(f"Block headers saved to {output_file}")
