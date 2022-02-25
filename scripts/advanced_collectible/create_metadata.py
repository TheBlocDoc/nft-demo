from brownie import Cartel, network
from scripts.helpful_scripts import get_rank
from metadata.sample_metadata import metadata_template
from pathlib import Path
import requests
import json
import os

rank_to_image_uri = {
    "KINGPIN": "https://ipfs.io/ipfs/QmcJHSgE819BwQBFAQSM134oSxgFWtoc14LP6khvPP1AYj?filename=KINGPIN_1.png",
    "CAPTAIN": "https://ipfs.io/ipfs/QmSgSouvytjK8bVEGhCUnUrWecGWNc5Q2YyUVDpLrvVBkF?filename=CAPTAIN_2.png",
    "OG": "https://ipfs.io/ipfs/QmahuhWk85pZCdTFtmbuMmYvHxbuL4RRtXk68VA2zp4NkC?filename=OG_3.png",
    "ENFORCER": "https://ipfs.io/ipfs/QmUJ571EpgWXAe31PRwK9fLmG4U3qkKCCPKuv4XEArSEWU?filename=ENFORCER_4.png",
    "PROSPECT": "https://ipfs.io/ipfs/QmUJ571EpgWXAe31PRwK9fLmG4U3qkKCCPKuv4XEArSEWU?filename=ENFORCER_4.png",
}


def main():
    advanced_collectible = Cartel[-1]
    number_of_advanced_collectibles = advanced_collectible.tokenCounter()
    print(f"You have created {number_of_advanced_collectibles} collectibles!")
    for token_id in range(number_of_advanced_collectibles):
        rank = get_rank(advanced_collectible.tokenIdToRank(token_id))
        metadata_file_name = (
            f"./metadata/{network.show_active()}/{token_id}-{rank}.json"
        )
        collectible_metadata = metadata_template
        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} already exists! Delete it to overwrite")
        else:
            print(f"Creating Metadata file: {metadata_file_name}")
            collectible_metadata["name"] = rank
            collectible_metadata["description"] = f"A real ass {rank} nigga!"
            image_path = "./img/" + rank.lower().replace("_", "-") + ".png"

            image_uri = None
            if os.getenv("UPLOAD_IPFS") == "true":
                image_uri = upload_to_ipfs(image_path)
            image_uri = image_uri if image_uri else rank_to_image_uri[rank]

            collectible_metadata["image"] = image_uri
            with open(metadata_file_name, "w") as file:
                json.dump(collectible_metadata, file)
            if os.getenv("UPLOAD_IPFS") == "true":
                upload_to_ipfs(metadata_file_name)


# curl -X POST -F file=@metadata/rinkeby/0-RANK.json http://localhost:5001/api/v0/add


def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "http://127.0.0.1:5001"
        endpoint = "/api/v0/add"
        response = requests.post(ipfs_url + endpoint, files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        # "./img/0-PUG.png" -> "0-PUG.png"
        filename = filepath.split("/")[-1:][0]
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(image_uri)
        return image_uri
