from brownie import network, Cartel
from scripts.helpful_scripts import OPENSEA_URL, get_rank, get_account

narco_metadata_dic = {
    "KINGPIN": "https://ipfs.io/ipfs/QmcJHSgE819BwQBFAQSM134oSxgFWtoc14LP6khvPP1AYj?filename=KINGPIN_1.png",
    "CAPTAIN": "https://ipfs.io/ipfs/QmSgSouvytjK8bVEGhCUnUrWecGWNc5Q2YyUVDpLrvVBkF?filename=CAPTAIN_2.png",
    "OG": "https://ipfs.io/ipfs/QmahuhWk85pZCdTFtmbuMmYvHxbuL4RRtXk68VA2zp4NkC?filename=OG_3.png",
    "ENFORCER": "https://ipfs.io/ipfs/QmUJ571EpgWXAe31PRwK9fLmG4U3qkKCCPKuv4XEArSEWU?filename=ENFORCER_4.png",
    "PROSPECT": "https://ipfs.io/ipfs/QmUJ571EpgWXAe31PRwK9fLmG4U3qkKCCPKuv4XEArSEWU?filename=ENFORCER_4.png",
}


def main():
    print(f"Working on {network.show_active()}")
    advanced_collectible = Cartel[-1]
    number_of_collectibles = advanced_collectible.tokenCounter()
    print(f"You have {number_of_collectibles} tokenIds")
    for token_id in range(number_of_collectibles):
        rank = get_rank(advanced_collectible.tokenIdToRank(token_id))
        if not advanced_collectible.tokenURI(token_id).startswith("https://"):
            print(f"Setting tokenURI of {token_id}")
            set_tokenURI(token_id, advanced_collectible, narco_metadata_dic[rank])


def set_tokenURI(token_id, nft_contract, tokenURI):
    account = get_account()
    tx = nft_contract.setTokenURI(token_id, tokenURI, {"from": account})
    tx.wait(1)
    print(
        f"Awesome! You can view your NFT at {OPENSEA_URL.format(nft_contract.address, token_id)}"
    )
    print("Please wait up to 20 minutes, and hit the refresh metadata button")
