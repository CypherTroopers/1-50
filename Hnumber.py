import plyvel
import csv
import struct

def decode_header_number_key(key, value):
    """
    Decode the block header number from the key and value.
    :param key: The key (bytes)
    :param value: The value (bytes)
    :return: (header_hash, block_number) (tuple)
    """
    try:
        header_hash = key[1:].hex()  # 'H' 
        block_number = struct.unpack(">Q", value)[0] 
        return header_hash, block_number
    except struct.error:
        return None, None  

db = plyvel.DB('./chaindata', create_if_missing=False)

header_number_prefix = b'H'
start_block = 0
end_block = 50000
output_file = "header_numbers.csv"

with open(output_file, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Header Hash", "Block Number"])

    for key, value in db:
        try:
            if key.startswith(header_number_prefix):
                header_hash, block_number = decode_header_number_key(key, value)

                if block_number is not None and start_block <= block_number <= end_block:
                    writer.writerow([header_hash, block_number])

        except ValueError:
            continue

db.close()
print(f"Header numbers saved to {output_file}")
