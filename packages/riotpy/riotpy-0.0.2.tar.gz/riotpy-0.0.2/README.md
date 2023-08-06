# riotpy

riotpy is a Python library for Riot API. Currently this is for only `SUMMONER-V4`, `SPECTATOR-V4`, and `MATCH-V5`.

## How to use

- First of all, you need to get Riot API key from https://developer.riotgames.com/.

1. Set `riot` variable with `riot = riotpy.Riot('my_api_key')`
2. Use functions with it like `riot.summoner(summonerName='hide on bush')`.
3. Plus, use query strings by kwargs like `riot.match(puuid=puuid, start=0, count=1)
