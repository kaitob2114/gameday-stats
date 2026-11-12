
from dataclasses import dataclass, field
from drafter import *


# Website information
set_site_information(
    author="Kaitlyn O'Brien",
    description=(
        "GameDay Stats is a website for tracking player statistics, "
        "managing team rosters, and comparing player performance."
    ),
    sources="Python class materials and Drafter documentation.",
    planning="See the GameDay Stats planning and brainstorming document.",
    links=["https://github.com/kaitob2114/gameday-stats"]
)


@dataclass
class Player:
    """Store one player's information and statistics."""
    player_id: int
    name: str
    sport: str
    stat_one: int
    stat_two: int
    stat_three: int
    games_played: int


@dataclass
class State:
    """Store information shared across all website pages."""
    players: list[Player] = field(default_factory=list)
    selected_sport: str = "Basketball"
    team_name: str = "My Team"
    message: str = "Welcome to GameDay Stats!"
    next_player_id: int = 1


def get_stat_labels(sport: str) -> tuple[str, str, str]:
    """Return the correct statistic names for each sport."""
    if sport == "Soccer":
        return ("Goals", "Assists", "Shots")
    elif sport == "Softball":
        return ("Hits", "Runs", "RBIs")
    else:
        return ("Points", "Assists", "Rebounds")


def find_player(state: State, player_id: int) -> Player | None:
    """Find a player using their ID."""
    for player in state.players:
        if player.player_id == player_id:
            return player
    return None


@route
def index(state: State) -> Page:
    """Display the home page."""
    return Page(state, [
        Header("GameDay Stats"),
        Text("Sports Statistics Tracker"),
        Text(state.message),
        Header("Team: " + state.team_name),
        Button("Change Team Name", "update_team"),
        Button("Add Player", "add_player"),
        Button("View Team Roster", "view_players"),
        Button("View Statistics", "view_stats"),
        Button("Leaderboard", "leaderboard")
    ])


@route
def update_team(state: State) -> Page:
    """Display the team name form."""
    return Page(state, [
        Header("Change Team Name"),
        TextBox("team_name", state.team_name),
        Button("Save Team Name", "save_team_name"),
        Button("Back Home", "index")
    ])


@route
def save_team_name(state: State, team_name: str) -> Page:
    """Save the new team name."""
    if team_name.strip() == "":
        state.message = "Please enter a team name."
        return update_team(state)

    state.team_name = team_name.strip()
    state.message = "Team name updated!"
    return index(state)


@route
def add_player(state: State, sport: str = "Basketball") -> Page:
    """Display the add player form for the selected sport."""
    stat_one, stat_two, stat_three = get_stat_labels(sport)
    state.selected_sport = sport

    return Page(state, [
        Header("Add a Player"),
        Text(state.message),
        Text("Enter the player's information."),
        Text("Player Name:"),
        TextBox("name"),
        Text("Choose a Sport:"),
        SelectBox("sport", [
            "Basketball", "Soccer", "Softball"
        ], sport),
        Button("Choose Sport", "add_player"),
        Header("Player Statistics"),
        Text(stat_one + ":"),
        TextBox("stat_one", 0, "number"),
        Text(stat_two + ":"),
        TextBox("stat_two", 0, "number"),
        Text(stat_three + ":"),
        TextBox("stat_three", 0, "number"),
        Text("Games Played:"),
        TextBox("games_played", 0, "number"),
        Button("Save Player", "save_player"),
        Button("Back Home", "index")
    ])


@route
def save_player(state: State, name: str, sport: str,
                stat_one: int, stat_two: int,
                stat_three: int, games_played: int) -> Page:
    """Validate and save a new player."""
    if name.strip() == "":
        state.message = "Please enter a player name."
        return add_player(state, sport)

    for player in state.players:
        if (player.name.lower() == name.strip().lower()
                and player.sport == sport):
            state.message = "This player already exists in this sport."
            return add_player(state, sport)

    if (stat_one < 0 or stat_two < 0 or stat_three < 0
            or games_played < 0):
        state.message = "Statistics cannot be negative."
        return add_player(state, sport)

    new_player = Player(
        player_id=state.next_player_id,
        name=name.strip(),
        sport=sport,
        stat_one=stat_one,
        stat_two=stat_two,
        stat_three=stat_three,
        games_played=games_played
    )

    state.players.append(new_player)
    state.next_player_id += 1
    state.selected_sport = sport
    state.message = name + " was successfully added!"

    return view_players(state)


@route
def view_players(state: State) -> Page:
    """Display all players on the team roster."""
    content = [
        Header("Team Roster"),
        Text(state.message)
    ]

    if len(state.players) == 0:
        content.append(Text("No players have been added yet."))
    else:
        for player in state.players:
            content.append(Header(player.name))
            content.append(Text("Sport: " + player.sport))
            content.append(Button(
                "View Player Details",
                "player_details",
                {"player_id": player.player_id}
            ))

    content.extend([
        Button("Add Another Player", "add_player"),
        Button("View Statistics", "view_stats"),
        Button("Back Home", "index")
    ])

    return Page(state, content)


@route
def player_details(state: State, player_id: int) -> Page:
    """Display the selected player's statistics."""
    player = find_player(state, player_id)

    if player is None:
        state.message = "Player not found."
        return view_players(state)

    stat_one, stat_two, stat_three = get_stat_labels(
        player.sport
    )

    return Page(state, [
        Header(player.name + "'s Statistics"),
        Text("Sport: " + player.sport),
        Text(stat_one + ": " + str(player.stat_one)),
        Text(stat_two + ": " + str(player.stat_two)),
        Text(stat_three + ": " + str(player.stat_three)),
        Text("Games Played: " + str(player.games_played)),
        Button(
            "Edit Statistics",
            "edit_stats",
            {"player_id": player.player_id}
        ),
        Button(
            "Delete Player",
            "delete_player",
            {"player_id": player.player_id}
        ),
        Button("Back to Roster", "view_players"),
        Button("Back Home", "index")
    ])


@route
def edit_stats(state: State, player_id: int) -> Page:
    """Display the form for editing player statistics."""
    player = find_player(state, player_id)

    if player is None:
        state.message = "Player not found."
        return view_players(state)

    stat_one, stat_two, stat_three = get_stat_labels(
        player.sport
    )

    return Page(state, [
        Header("Edit " + player.name + "'s Statistics"),
        Text("Enter the updated statistics."),
        Text(stat_one + ":"),
        TextBox("stat_one", player.stat_one, "number"),
        Text(stat_two + ":"),
        TextBox("stat_two", player.stat_two, "number"),
        Text(stat_three + ":"),
        TextBox("stat_three", player.stat_three, "number"),
        Text("Games Played:"),
        TextBox("games_played", player.games_played, "number"),
        Button(
            "Save Changes",
            "update_stats",
            {"player_id": player.player_id}
        ),
        Button(
            "Cancel",
            "player_details",
            {"player_id": player.player_id}
        )
    ])


@route
def update_stats(state: State, player_id: int,
                 stat_one: int, stat_two: int,
                 stat_three: int, games_played: int) -> Page:
    """Save updated statistics for a player."""
    player = find_player(state, player_id)

    if player is None:
        state.message = "Player not found."
        return view_players(state)

    if (stat_one < 0 or stat_two < 0 or stat_three < 0
            or games_played < 0):
        state.message = "Statistics cannot be negative."
        return edit_stats(state, player_id)

    player.stat_one = stat_one
    player.stat_two = stat_two
    player.stat_three = stat_three
    player.games_played = games_played

    state.message = player.name + "'s statistics were updated!"

    return player_details(state, player_id)


@route
def delete_player(state: State, player_id: int) -> Page:
    """Delete a player from the team roster."""
    player = find_player(state, player_id)

    if player is None:
        state.message = "Player not found."
    else:
        state.players.remove(player)
        state.message = player.name + " was deleted."

    return view_players(state)


@route
def view_stats(state: State) -> Page:
    """Calculate and display statistics for each sport."""
    content = [
        Header("Team Statistics"),
        Text(state.message)
    ]

    if len(state.players) == 0:
        content.append(Text("Add players to see statistics."))
    else:
        for sport in ["Basketball", "Soccer", "Softball"]:
            sport_players = []

            for player in state.players:
                if player.sport == sport:
                    sport_players.append(player)

            if len(sport_players) > 0:
                stat_one, stat_two, stat_three = (
                    get_stat_labels(sport)
                )

                total_one = 0
                total_two = 0
                total_three = 0

                content.append(Header(sport))

                for player in sport_players:
                    total_one += player.stat_one
                    total_two += player.stat_two
                    total_three += player.stat_three

                    content.append(Text(
                        player.name + ": "
                        + stat_one + " " + str(player.stat_one)
                        + " | " + stat_two + " "
                        + str(player.stat_two)
                        + " | " + stat_three + " "
                        + str(player.stat_three)
                    ))

                    if player.games_played > 0:
                        average = (
                            player.stat_one / player.games_played
                        )
                        content.append(Text(
                            "Average " + stat_one + " per game: "
                            + str(round(average, 2))
                        ))

                content.extend([
                    Header(sport + " Totals"),
                    Text(stat_one + ": " + str(total_one)),
                    Text(stat_two + ": " + str(total_two)),
                    Text(stat_three + ": " + str(total_three))
                ])

    content.extend([
        Button("Leaderboard", "leaderboard"),
        Button("Back Home", "index")
    ])

    return Page(state, content)


@route
def leaderboard(state: State,
                sport: str = "Basketball",
                stat_category: str = "stat_one") -> Page:
    """Find the player with the highest selected statistic."""
    stat_one, stat_two, stat_three = get_stat_labels(sport)

    content = [
        Header("Player Leaderboard"),
        Text("Choose a sport:"),
        SelectBox("sport", [
            "Basketball", "Soccer", "Softball"
        ], sport),
        Text("Choose a statistic:"),
        SelectBox("stat_category", [
            "stat_one", "stat_two", "stat_three"
        ], stat_category),
        Button("Compare Players", "leaderboard")
    ]

    sport_players = []

    for player in state.players:
        if player.sport == sport:
            sport_players.append(player)

    if len(sport_players) == 0:
        content.append(Text("No players to compare in this sport."))
    else:
        highest_player = sport_players[0]

        for player in sport_players:
            if stat_category == "stat_one":
                if player.stat_one > highest_player.stat_one:
                    highest_player = player
            elif stat_category == "stat_two":
                if player.stat_two > highest_player.stat_two:
                    highest_player = player
            elif stat_category == "stat_three":
                if player.stat_three > highest_player.stat_three:
                    highest_player = player

        if stat_category == "stat_one":
            highest_value = highest_player.stat_one
            label = stat_one
        elif stat_category == "stat_two":
            highest_value = highest_player.stat_two
            label = stat_two
        else:
            highest_value = highest_player.stat_three
            label = stat_three

        content.extend([
            Header("Top Performer"),
            Text(highest_player.name),
            Text("Highest " + label + ": " + str(highest_value))
        ])

    content.append(Button("Back Home", "index"))

    return Page(state, content)


if __name__ == "__main__":
    start_server(State())

