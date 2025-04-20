const { Gateway, Wallets } = require('fabric-network');
const path = require('path');
const fs = require('fs');
const { execSync } = require('child_process');

async function main() {
    try {
        const walletPath = path.join(process.cwd(), 'wallet');
        const wallet = await Wallets.newFileSystemWallet(walletPath);
        const identity = {
            credentials: {
                certificate: fs.readFileSync(path.join(__dirname, '../fabric-samples/test-network/organizations/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp/signcerts/Admin@org1.example.com-cert.pem')).toString(),
privateKey: fs.readFileSync(path.join(__dirname, '../fabric-samples/test-network/organizations/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp/keystore/priv_sk')).toString()

            },
            mspId: 'Org1MSP',
            type: 'X.509'
        };
        await wallet.put('admin', identity);

        const gateway = new Gateway();
        const ccp = JSON.parse(fs.readFileSync('connection-org1.json', 'utf8'));
        await gateway.connect(ccp, { wallet, identity: 'admin', discovery: { enabled: true, asLocalhost: true } });
        const network = await gateway.getNetwork('mychannel');
        const contract = network.getContract('fingerchain');

        await contract.submitTransaction('OwnerReg', 'owner1', 'pk_owner1');
        console.log('Owner registered');

        await contract.submitTransaction('UserReg', 'user1', 'pk_user1');
        console.log('User registered');

        const mediaContent = 'Sample media content';
        const ipfsHash = execSync('python3 ~/fingerchain-scripts/ipfs_utils.py "' + mediaContent + '"').toString().split('IPFS Hash: ')[1].split('\n')[0];
        await contract.submitTransaction('MediaUpload', 'media1', 'owner1', 'Sample Media', ipfsHash, '10.0');
        console.log('Media uploaded with hash:', ipfsHash);

        await contract.submitTransaction('MediaShare', 'media1', 'user1');
        console.log('Media shared');

        const result = await contract.evaluateTransaction('MediaQuery', 'media1');
        console.log('Media info:', JSON.parse(result.toString()));

        console.log('Run fingerprinting manually with: python3 ~/fingerchain-scripts/fingerprinting.py');

        await gateway.disconnect();
    } catch (error) {
        console.error('Error:', error);
        process.exit(1);
    }
}

main();

