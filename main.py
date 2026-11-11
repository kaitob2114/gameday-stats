
from dataclasses import dataclass, field
from drafter import *


# Website information
set_website_title("GameDay Stats")

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
    points: int
    assists: int
    rebounds: int
    games_played: int


@dataclass
class State:
    """Store information shared across all website pages."""
    players: list[Player] = field(default_factory=list)
    selected_sport: str = "Basketball"
    team_name: str = "My Team"
    message: str = "Welcome to GameDay Stats!"
    next_player_id: int = 1


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
def add_player(state: State) -> Page:
    """Display the add player form."""
    return Page(state, [
        Header("Add a Player"),
        Text(state.message),
        Text("Enter the player's information."),
        Text("Player Name:"),
        TextBox("name"),
        Text("Sport:"),
        SelectBox("sport", [
            "Basketball", "Soccer", "Softball"
        ], state.selected_sport),
        Text("Points:"),
        TextBox("points", 0, "number"),
        Text("Assists:"),
        TextBox("assists", 0, "number"),
        Text("Rebounds:"),
        TextBox("rebounds", 0, "number"),
        Text("Games Played:"),
        TextBox("games_played", 0, "number"),
        Button("Save Player", "save_player"),
        Button("Back Home", "index")
    ])


@route
def save_player(state: State, name: str, sport: str,
                points: int, assists: int, rebounds: int,
                games_played: int) -> Page:
    """Validate and save a new player."""
    if name.strip() == "":
        state.message = "Please enter a player name."
        return add_player(state)

    for player in state.players:
        if player.name.lower() == name.strip().lower():
            state.message = "This player already exists."
            return add_player(state)

    if (points < 0 or assists < 0 or rebounds < 0
            or games_played < 0):
        state.message = "Statistics cannot be negative."
        return add_player(state)

    new_player = Player(
        player_id=state.next_player_id,
        name=name.strip(),
        sport=sport,
        points=points,
        assists=assists,
        rebounds=rebounds,
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
                [Argument("player_id", player.player_id)]
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

    return Page(state, [
        Header(player.name + "'s Statistics"),
        Text("Sport: " + player.sport),
        Text("Points: " + str(player.points)),
        Text("Assists: " + str(player.assists)),
        Text("Rebounds: " + str(player.rebounds)),
        Text("Games Played: " + str(player.games_played)),

        Button(
            "Edit Statistics",
            "edit_stats",
            [Argument("player_id", player.player_id)]
        ),

        Button(
            "Delete Player",
            "delete_player",
            [Argument("player_id", player.player_id)]
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

    return Page(state, [
        Header("Edit " + player.name + "'s Statistics"),
        Text("Enter the updated statistics."),
        Text("Points:"),
        TextBox("points", player.points, "number"),
        Text("Assists:"),
        TextBox("assists", player.assists, "number"),
        Text("Rebounds:"),
        TextBox("rebounds", player.rebounds, "number"),
        Text("Games Played:"),
        TextBox("games_played", player.games_played, "number"),

        Button(
            "Save Changes",
            "update_stats",
            [Argument("player_id", player.player_id)]
        ),

        Button(
            "Cancel",
            "player_details",
            [Argument("player_id", player.player_id)]
        )
    ])


@route
def update_stats(state: State, player_id: int,
                 points: int, assists: int,
                 rebounds: int, games_played: int) -> Page:
    """Save updated statistics for a player."""
    player = find_player(state, player_id)

    if player is None:
        state.message = "Player not found."
        return view_players(state)

    if (points < 0 or assists < 0 or rebounds < 0
            or games_played < 0):
        state.message = "Statistics cannot be negative."
        return edit_stats(state, player_id)

    player.points = points
    player.assists = assists
    player.rebounds = rebounds
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
    """Calculate and display team statistics."""
    content = [
        Header("Team Statistics"),
        Text(state.message)
    ]

    if len(state.players) == 0:
        content.append(Text("Add players to see statistics."))
    else:
        total_points = 0
        total_assists = 0
        total_rebounds = 0

        for player in state.players:
            total_points += player.points
            total_assists += player.assists
            total_rebounds += player.rebounds

            content.append(Header(player.name))
            content.append(Text(
                "Points: " + str(player.points)
                + " | Assists: " + str(player.assists)
                + " | Rebounds: " + str(player.rebounds)
            ))

            if player.games_played > 0:
                average = player.points / player.games_played
                content.append(Text(
                    "Average Points Per Game: "
                    + str(round(average, 2))
                ))

        content.extend([
            Header("Team Totals"),
            Text("Total Points: " + str(total_points)),
            Text("Total Assists: " + str(total_assists)),
            Text("Total Rebounds: " + str(total_rebounds))
        ])

    content.extend([
        Button("Leaderboard", "leaderboard"),
        Button("Back Home", "index")
    ])

    return Page(state, content)


@route
def leaderboard(state: State,
                stat_category: str = "points") -> Page:
    """Find the player with the highest selected statistic."""
    content = [
        Header("Player Leaderboard"),
        Text("Choose a statistic to compare:"),
        SelectBox("stat_category", [
            "points", "assists", "rebounds"
        ], stat_category),
        Button("Compare Players", "leaderboard")
    ]

    if len(state.players) == 0:
        content.append(Text("No players to compare yet."))
    else:
        highest_player = state.players[0]

        for player in state.players:
            if stat_category == "points":
                if player.points > highest_player.points:
                    highest_player = player
            elif stat_category == "assists":
                if player.assists > highest_player.assists:
                    highest_player = player
            elif stat_category == "rebounds":
                if player.rebounds > highest_player.rebounds:
                    highest_player = player

        if stat_category == "points":
            highest_value = highest_player.points
        elif stat_category == "assists":
            highest_value = highest_player.assists
        else:
            highest_value = highest_player.rebounds

        content.extend([
            Header("Top Performer"),
            Text(highest_player.name),
            Text(
                "Highest " + stat_category + ": "
                + str(highest_value)
            )
        ])

    content.append(Button("Back Home", "index"))

    return Page(state, content)


start_server(State())
