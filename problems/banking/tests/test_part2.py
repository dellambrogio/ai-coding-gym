from solution import Bank


def make_bank():
    b = Bank()
    for a in ["alice", "bob", "carol"]:
        b.create_account(a)
        b.deposit(a, 1000)
    return b


def test_withdraw():
    b = make_bank()
    assert b.withdraw("alice", 300) == 700
    assert b.withdraw("alice", 701) is None
    assert b.withdraw("nobody", 1) is None


def test_top_spenders_counts_transfers_and_withdrawals():
    b = make_bank()
    b.transfer("alice", "bob", 100)
    b.withdraw("bob", 300)
    b.transfer("carol", "alice", 50)
    assert b.top_spenders(3) == [("bob", 300), ("alice", 100), ("carol", 50)]


def test_top_spenders_ties_and_zero():
    b = make_bank()
    b.withdraw("carol", 10)
    b.withdraw("bob", 10)
    assert b.top_spenders(3) == [("bob", 10), ("carol", 10), ("alice", 0)]


def test_failed_operations_do_not_count():
    b = make_bank()
    b.withdraw("alice", 5000)
    b.transfer("alice", "bob", 5000)
    assert b.top_spenders(1) == [("alice", 0)]


def test_top_spenders_n_larger_than_accounts():
    b = make_bank()
    assert len(b.top_spenders(10)) == 3
