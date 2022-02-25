//SPDX-License-identifier: MIT

pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract Cartel is ERC721, VRFConsumerBase {
    uint256 public tokenCounter;
    bytes32 public keyhash;
    uint256 public fee;
    enum Rank {
        KINGPIN,
        CAPTAIN,
        OG,
        ENFORCER,
        PROSPECT
    }
    mapping(uint256 => Rank) tokenIdToRank;
    mapping(bytes32 => address) public requestIdToSender;
    event requestedCollectible(bytes32 indexed requestId, address requester);
    event rankAssigned(uint256 indexed tokenId, Rank rank);

    constructor(
        address _vrfCoordinator,
        address _linkToken,
        bytes32 _keyhash,
        uint256 _fee
    )
        public
        VRFConsumerBase(_vrfCoordinator, _linkToken)
        ERC721("Cartel", "Narco")
    {
        tokenCounter = 0;
        keyhash = _keyhash;
        fee = _fee;
    }

    function createCollectible() public returns (bytes32) {
        bytes32 requestId = requestRandomness(keyhash, fee);
        requestIdToSender[requestId] = msg.sender;
        emit requestedCollectible(requestId, msg.sender);
    }

    function fulfillRandomness(bytes32 requestId, uint256 randomNumber)
        internal
        override
    {
        Rank rank = Rank(randomNumber % 5);
        uint256 newTokenId = tokenCounter;
        tokenIdToRank[newTokenId] = rank;
        emit rankAssigned(newTokenId, rank);
        address owner = requestIdToSender[requestId];
        _safeMint(owner, newTokenId);
        // _setTokenURI(newTokenId, tokenURI);
        tokenCounter = tokenCounter + 1;
    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        // KINGPIN, CAPTAIN, OG, ENFORCER, PROSPECT
        require(
            _isApprovedOrOwner(_msgSender(), tokenId),
            "ERC721: caller is not owner approved"
        );
        _setTokenURI(tokenId, _tokenURI);
    }
}
