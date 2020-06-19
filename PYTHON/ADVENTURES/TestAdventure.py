import Adventure, Room, Action, Sequence

adv = Adventure.Adventure('Demo Adventure', 'This is a demo adventure. not much to say...')

ForestEntrance = adv.AddRoom(Room.Room(
    "Forest Enter",
    Sequence.Sequence(["You are standing in the front of the forest",
                       "You came here to look for the legendary diamond sword."],
                      deleteMessages=False),
    Sequence.Sequence([("You are standing at the forest entrance.", 3)], deleteMessages=False)
))

