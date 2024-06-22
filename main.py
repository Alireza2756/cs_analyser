from demoparser2 import DemoParser

parser = DemoParser("demos/faze-vs-vitality-m2-dust2.dem")


# parse_event("player_hurt") is a method (presumably part of DemoParser)
# that extracts events where players are hurt or damaged from the demo file.
# player_hurt_events will contain a DataFrame with information about each event
# where a player is hurt, such as the tick (game time), the player who was hurt,
# and who attacked them (attacker_steamid).
player_hurt_events = parser.parse_event("player_hurt")



# parse_ticks(["pitch", "yaw"]) is another method that extracts data about player orientation (pitch and yaw angles) at each tick (game time)
# from the demo file.
# df is a DataFrame that contains information about each tick,
# including the pitch and yaw angles of each player.
df = parser.parse_ticks(["pitch", "yaw"])

# This loop iterates over each player hurt event (player_hurt_events).
# For each event, it calculates a time window (start_tick to end_tick)
# around the event where the attacker's aiming data (pitch and yaw) will be analyzed.
# It filters df (which contains pitch and yaw data for all ticks) to get subdf,
# which contains data only for the specific attacker (attacker_steamid) and within the time window.
# It then checks if the attacker's pitch is within a certain range (0 to 30 degrees in this example)
# that typically corresponds to head level aiming.
# If the condition is met, it prints a message indicating that the attacker aimed at head level at a specific tick.

for idx, event in player_hurt_events.iterrows():
    start_tick = event["tick"] - 300
    end_tick = event["tick"]
    attacker = event["attacker_steamid"]

    if attacker is not None:
        subdf = df[(df["tick"].between(start_tick, end_tick)) & (df["steamid"] == int(attacker))]

        # Check if the attacker was aiming at head level
        for _, row in subdf.iterrows():
            pitch = row["pitch"]
            yaw = row["yaw"]

            # Assuming head level pitch and yaw ranges
            # Adjust these ranges based on your game's specific mechanics
            if 0 <= pitch <= 30:  # Example range for head level pitch
                print(f"Attacker {attacker} aimed at head level at tick {row['tick']}")

