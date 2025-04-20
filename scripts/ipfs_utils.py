import ipfshttpclient
import sys

def upload_to_ipfs(data):
    client = ipfshttpclient.connect()
    res = client.add_bytes(data.encode() if isinstance(data, str) else data)
    return res

def download_from_ipfs(hash_value):
    client = ipfshttpclient.connect()
    return client.cat(hash_value)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        data = sys.argv[1]
        hash_val = upload_to_ipfs(data)
        print("IPFS Hash:", hash_val)
    else:
        hash_val = upload_to_ipfs("Test media content")
        print("IPFS Hash:", hash_val)
        content = download_from_ipfs(hash_val)
        print("Downloaded:", content.decode())

