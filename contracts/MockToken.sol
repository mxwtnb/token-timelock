// SPDX-License-Identifier: MIT

pragma solidity =0.6.12;

import "@openzeppelin/contracts/token/ERC20/ERC20Upgradeable.sol";

contract MockToken is ERC20Upgradeable {
    function initialize() public initializer {
        __ERC20_init("Mock Token", "MOCK");
        _mint(msg.sender, 100e18);
    }
}
