league_config = {
    "Italian Serie A":{"id":"11", "name":"Serie-A"},
    "English Premier league":{"id":"9", "name":"Premier-League"}
}

for league, league_2 in league_config.items():
    print(f"league: {league_2['name']},{league_2['id']}\nleague_2: {league}")
    