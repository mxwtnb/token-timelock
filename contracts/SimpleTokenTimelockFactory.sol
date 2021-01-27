// SPDX-License-Identifier: MIT

pragma solidity =0.6.12;

import "@openzeppelin/contracts/token/ERC20/IERC20Upgradeable.sol";

import "./CloneFactory.sol";
import "./SimpleTokenTimelock.sol";

contract SimpleTokenTimelockFactory is CloneFactory {
    address public logic;

    constructor() public {
        logic = address(new SimpleTokenTimelock());
    }

    function createTimelock(
        IERC20Upgradeable token,
        address beneficiary,
        uint256 releaseTime
    ) external returns (address timelock) {
        timelock = createClone(logic);
        SimpleTokenTimelock(timelock).initialize(
            token,
            beneficiary,
            releaseTime
        );
    }
}
