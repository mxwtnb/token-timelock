from brownie import reverts


def test_timelock(chain, a, MockToken, SimpleTokenTimelock, SimpleTokenTimelockFactory):
    # params
    releaseTimes = [2000000000, 3000000000]
    amounts = [10 * 10 ** 18, 100 * 10 ** 18]

    # accounts
    deployer, beneficiary, keeper = a[:3]

    # deploy factory
    factory = deployer.deploy(SimpleTokenTimelockFactory)

    # run multiple times for different timelocks
    for amount, releaseTime in zip(amounts, releaseTimes):

        # deploy token
        token = deployer.deploy(MockToken)

        # check can't initialize token again
        token.initialize({"from": deployer})
        with reverts("Initializable: contract is already initialized"):
            token.initialize({"from": deployer})

        # create timelock
        tx = factory.createTimelock(token, beneficiary, releaseTime, {"from": deployer})
        timelock = SimpleTokenTimelock.at(tx.return_value)

        # check can't initialize timelock again
        with reverts("Initializable: contract is already initialized"):
            timelock.initialize(token, beneficiary, releaseTime, {"from": deployer})

        # send tokens to timelock
        token.transfer(timelock, amount, {"from": deployer})
        assert token.balanceOf(timelock) == amount

        # check variables set
        assert timelock.token() == token
        assert timelock.beneficiary() == beneficiary
        assert timelock.releaseTime() == releaseTime

        # fast forward to just before release time
        chain.sleep(releaseTime - chain.time() - 1)
        assert chain.time() == releaseTime - 1

        # check tokens cannot be released
        with reverts("TokenTimelock: current time is before release time"):
            timelock.release({"from": keeper})

        # fast forward to release time
        chain.sleep(releaseTime - chain.time())
        assert chain.time() == releaseTime

        # check tokens released
        assert token.balanceOf(beneficiary) == 0
        timelock.release({"from": keeper})
        assert token.balanceOf(beneficiary) == amount

        with reverts("TokenTimelock: no tokens to release"):
            timelock.release({"from": keeper})
