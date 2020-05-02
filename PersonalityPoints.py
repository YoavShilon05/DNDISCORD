import enum

class PersonalityPoints(enum.Enum):

    strength = 0
    intelligence = 1
    charisma = 2
    agility = 3
    defense = 4

def MakePersonalityPoints(**personalityPoints):

    result = {}
    for p in PersonalityPoints:
        result[p.name] = personalityPoints.get(p, 0)

    return result

#