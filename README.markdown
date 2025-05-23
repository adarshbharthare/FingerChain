# FingerChain Implementation

An implementation of the FingerChain media-sharing system from Xiao et al., "FingerChain: Copyrighted Multi-Owner Media Sharing by Introducing Asymmetric Fingerprinting Into Blockchain" (IEEE TNSM, 2023). This implements secure media sharing for one owner and one user using Hyperledger Fabric, IPFS, and user-side fingerprinting.

## Overview

FingerChain enables secure media sharing (e.g., music, videos) with copyright protection. It uses:
- **Hyperledger Fabric**: Blockchain for tracking ownership and access.
- **IPFS**: Decentralized storage for media.
- **Asymmetric Fingerprinting**: Adds a unique user ID (`b_k`) to media for piracy tracing.

This implementation demonstrates the workflow: an owner registers, uploads media to IPFS, shares it with a user, who adds a fingerprint, which can be traced if shared illegally. Visuals (workflow flowchart, fingerprint plot) are generated by included scripts.

## Workflow

1. Deploy Fabric network and chaincode.
2. Register owner (`owner1`).
3. Upload media to IPFS, store hash on Fabric.
4. Register user (`user1`).
5. Share media with user.
6. Add fingerprint (`b_k`, e.g., `[1 1 1 1 0 1 1 1 0 1]`) to user’s copy.
7. Trace fingerprint to identify user.

## Technologies

- **Hyperledger Fabric**: Blockchain ledger.
- **IPFS**: Decentralized storage.
- **Node.js**: Client logic (`client/app.js`).
- **Python**: Fingerprinting (`scripts/fingerprinting.py`), graphs (`scripts/workflow_graph.py`, `scripts/fingerprint_graph.py`).
- **Go**: Chaincode (`chaincode/chaincode.go`).
- **Paillier Encryption**: Secure fingerprinting.

## Files

- `fabric-commands.sh`: Starts Fabric, deploys chaincode.
- `client/app.js`: Registers owner/user, uploads/shares media.
- `client/package.json`: Node.js dependencies.
- `scripts/ipfs_utils.py`: Manages IPFS storage.
- `scripts/fingerprinting.py`: Generates/traces fingerprint.
- `scripts/workflow_graph.py`: Creates workflow flowchart.
- `scripts/fingerprint_graph.py`: Plots fingerprint.
- `chaincode/chaincode.go`: Smart contract.
- `.gitignore`: Excludes dependencies.
- `LICENSE`: MIT license.

## Setup

### Prerequisites

- **macOS** (Linux compatible).
- **Tools**:
  ```bash
  brew install node python3 graphviz go
  ```
- **IPFS**:
  ```bash
  brew install ipfs
  ipfs init  # First time only
  ```
- **Hyperledger Fabric**:
  ```bash
  curl -sSL https://bit.ly/2ysbOFE | bash -s -- 2.5.0
  mv fabric-samples ~/fabric-samples
  cd ~/fabric-samples
  git checkout v2.5.0
  ```

### Dependencies

```bash
# Node.js (in FingerChain/client/)
cd client
npm install

# Python (in FingerChain/scripts/)
pip3 install ipfshttpclient numpy phe matplotlib graphviz
```

### Folder Setup

1. Clone this repo:
   ```bash
   git clone https://github.com/your-username/FingerChain.git
   cd FingerChain
   ```
2. Ensure `~/fabric-samples/test-network` exists (from Fabric install).
3. Create wallet:
   ```bash
   mkdir client/wallet
   cd ~/fabric-samples/test-network
   ./network.sh up
   node enrollAdmin.js
   cp -r wallet/* ~/FingerChain/client/wallet/
   ./network.sh down
   ```

## Run

1. **Start Fabric and IPFS**:
   ```bash
   bash fabric-commands.sh
   ```
   - In another terminal:
     ```bash
     ipfs daemon
     ```

2. **Run Client**:
   ```bash
   cd client
   node app.js
   ```

3. **Run Scripts**:
   ```bash
   cd scripts
   python3 ipfs_utils.py
   python3 fingerprinting.py
   ```

4. **Generate Visuals**:
   ```bash
   cd scripts
   python3 workflow_graph.py
   python3 fingerprint_graph.py
   mv *.png ../
   ```

## Outputs

- `app.js`:
  ```
  Owner registered
  Media uploaded with hash: QmbnnDCg6zz...
  Media shared
  ```
- `ipfs_utils.py`:
  ```
  IPFS Hash: QmX2Dr...
  ```
- `fingerprinting.py`:
  ```
  Original fingerprint: [1 1 1 1 0 1 1 1 0 1]
  ```
- Visuals: `workflow.png` (flowchart).


## License

MIT License. See `LICENSE`.