from scripts.helpful_scripts import get_account, OPENSEA_URL
from brownie import BasicCartel

sample_token_uri = "https://ipfs.io/ipfs/QmcJHSgE819BwQBFAQSM134oSxgFWtoc14LP6khvPP1AYj?filename=KINGPIN_1.png"


def deploy_and_create():
    account = get_account()
    simple_collectible = BasicCartel.deploy({"from": account})
    tx = simple_collectible.createCollectible(sample_token_uri, {"from": account})
    tx.wait(1)
    print(
        f"Awesome, you can view your NFT at {OPENSEA_URL.format(simple_collectible.address, simple_collectible.tokenCounter() - 1)}"
    )
    print("Please wait up to 20 minutes, and hit the refresh metadata button. ")
    return simple_collectible


def main():
    deploy_and_create()
