import plyvel
import csv

def decode_transaction_hash(key):
    """
    Decode the transaction hash from the given key.
    :param key: The key (bytes)
    :return: The transaction hash (str)
    """
    return key[1:].hex()  # Remove prefix and convert to hex string

db = plyvel.DB('./chaindata', create_if_missing=False)

tx_lookup_prefix = b'l' 
start_block = 0
end_block = 50000

output_file = "transactions.csv"

with open(output_file, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Block Number", "Transaction Hash"])

    for key, value in db:
        try:
            if key.startswith(tx_lookup_prefix):
                transaction_hash = decode_transaction_hash(key)

                block_number = int.from_bytes(value, byteorder="big")

                if start_block <= block_number <= end_block:
                    writer.writerow([block_number, transaction_hash])

        except ValueError:
            continue  

db.close()

print(f"Transaction hashes saved to {output_file}")
