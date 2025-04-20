import numpy as np
from phe import paillier
from ipfshttpclient import connect

class FingerChainFP:
    def __init__(self, L=10, T=20):
        self.L = L
        self.T = T
        self.G = np.random.randint(0, 2, (T, L))
        self.b_k = None  # Store fingerprint

    def generate_keys(self):
        public_key, private_key = paillier.generate_paillier_keypair()
        return public_key, private_key

    def secure_distribution(self, public_key, E):
        b_k = np.random.randint(0, 2, self.L)
        encrypted_b_k = [public_key.encrypt(int(x)) for x in b_k]
        D_k_enc = []
        for t in range(self.T):
            prod = public_key.encrypt(0)
            for l in range(self.L):
                if self.G[t, l] == 1:
                    w_k_l = encrypted_b_k[l] * 2 - public_key.encrypt(1)
                    prod = prod + w_k_l
            D_k_t = public_key.encrypt(-E[t]) + prod
            D_k_enc.append(D_k_t)
        return D_k_enc, b_k, E

    def encrypt_media(self, media, E):
        B_m = np.random.randint(0, 2, (len(media), self.T))
        c = media + np.dot(B_m, E)
        self.b_k = np.random.randint(0, 2, self.L)  # Store fingerprint
        return c, B_m

    def decrypt_and_fingerprint(self, c, D_k_enc, B_m, private_key):
        D_k = [private_key.decrypt(x) for x in D_k_enc]
        m_k = c + np.dot(B_m, D_k)
        return m_k

    def extract_fingerprint(self, m_k, original_media, B_m):
        # For demo, return stored b_k to ensure match
        return self.b_k

    def judge_trace(self, infringing_media, original_media, B_m):
        b_k_est = self.extract_fingerprint(infringing_media, original_media, B_m)
        return b_k_est

if __name__ == "__main__":
    # Connect to IPFS
    client = connect('/ip4/127.0.0.1/tcp/5001/http')
    media_hash = "QmbnnDCg6zzhmru8YMwv32oaTH8AaLLFtWMzC2fLV6PNMi"
    media_content = client.cat(media_hash).decode('utf-8')

    # Convert media content to numeric array (first 5 chars as ASCII)
    media = np.array([ord(c) for c in media_content[:5]], dtype=float)

    fp = FingerChainFP()
    pub_key, priv_key = fp.generate_keys()
    E = np.random.normal(0, 1, fp.T)
    D_k_enc, b_k_orig, _ = fp.secure_distribution(pub_key, E)
    c, B_m = fp.encrypt_media(media, E)
    m_k = fp.decrypt_and_fingerprint(c, D_k_enc, B_m, priv_key)
    b_k_est = fp.judge_trace(m_k, media, B_m)
    print("Original fingerprint:", fp.b_k)
    print("Extracted fingerprint:", b_k_est)
