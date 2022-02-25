from brownie import Cartel


def main():
    flatten()


def flatten():
    file = open("./Cartel_flattened.sol", "w")
    verification_information = Cartel.get_verification_info()
    flattened_code = (
        verification_information["flattened_source"]
        .replace("\\n", "\n")
        .replace('\\"', '"')
    )
    file.write(flattened_code)
    file.close()
