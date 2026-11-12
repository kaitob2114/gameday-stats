
from bakery import assert_equal
from main import (
    State,
    Player,
    get_stat_labels,
    find_player,
    save_player,
    save_team_name,
    update_stats,
    delete_player
)


def test_stat_labels():
    """Test the statistic names for each sport."""
    assert_equal(
        get_stat_labels("Basketball"),
        ("Points", "Assists", "Rebounds")
    )
    assert_equal(
        get_stat_labels("Soccer"),
        ("Goals", "Assists", "Shots")
    )
    assert_equal(
        get_stat_labels("Softball"),
        ("Hits", "Runs", "RBIs")
    )


def test_find_player():
    """Test finding a player by ID."""
    player = Player(1, "Sarah", "Soccer", 2, 3, 5, 4)
    state = State(players=[player])

    assert_equal(find_player(state, 1), player)
    assert_equal(find_player(state, 5), None)


def test_save_player():
    """Test saving a soccer player."""
    state = State()

    save_player(state, "Sarah", "Soccer", 2, 3, 5, 4)

    assert_equal(len(state.players), 1)
    assert_equal(state.players[0].name, "Sarah")
    assert_equal(state.players[0].sport, "Soccer")
    assert_equal(state.players[0].stat_one, 2)
    assert_equal(state.players[0].games_played, 4)


def test_save_team_name():
    """Test changing the team name."""
    state = State()

    save_team_name(state, "Blue Eagles")

    assert_equal(state.team_name, "Blue Eagles")


def test_update_stats():
    """Test updating a player's statistics."""
    player = Player(1, "Sarah", "Basketball", 15, 5, 8, 3)
    state = State(players=[player])

    update_stats(state, 1, 20, 7, 10, 4)

    assert_equal(player.stat_one, 20)
    assert_equal(player.stat_two, 7)
    assert_equal(player.stat_three, 10)
    assert_equal(player.games_played, 4)


def test_delete_player():
    """Test deleting a player."""
    player = Player(1, "Sarah", "Softball", 3, 2, 4, 5)
    state = State(players=[player])

    delete_player(state, 1)

    assert_equal(len(state.players), 0)


test_stat_labels()
test_find_player()
test_save_player()
test_save_team_name()
test_update_stats()
test_delete_player()

print("GameDay Stats tests completed!")

