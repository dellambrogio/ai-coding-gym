from solution import Bank


def make_bank():
    b = Bank()
    for a in ["a", "b", "c"]:
        b.create_account(a)
        b.deposit(a, 100)
    return b


def test_merge_moves_balance_and_spending():
    b = make_bank()
    b.withdraw("b", 40)
    assert b.merge_accounts("a", "b") is True
    assert b.get_balance("a") == 160
    assert b.get_balance("b") is None
    assert b.top_spenders(1) == [("a", 40)]


def test_merged_id_can_be_recreated():
    b = make_bank()
    b.merge_accounts("a", "b")
    assert b.create_account("b") is True
    assert b.get_balance("b") == 0


def test_merge_invalid():
    b = make_bank()
    assert b.merge_accounts("a", "a") is False
    assert b.merge_accounts("a", "zzz") is False
    assert b.merge_accounts("zzz", "a") is False


def test_frozen_account_blocks_operations():
    b = make_bank()
    assert b.freeze("a") is True
    assert b.deposit("a", 10) is None
    assert b.withdraw("a", 10) is None
    assert b.transfer("a", "b", 10) is None
    assert b.transfer("b", "a", 10) is None
    assert b.get_balance("a") == 100 and b.get_balance("b") == 100


def test_unfreeze_restores():
    b = make_bank()
    b.freeze("a")
    assert b.unfreeze("a") is True
    assert b.deposit("a", 10) == 110


def test_freeze_missing_and_merge_frozen():
    b = make_bank()
    assert b.freeze("zzz") is False and b.unfreeze("zzz") is False
    b.freeze("c")
    assert b.merge_accounts("a", "c") is False
    assert b.get_balance("c") == 100
