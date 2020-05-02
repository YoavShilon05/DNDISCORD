

class Room:

    def __init__(self, name, longDescription, shortDescription, actions, adventure, **DunderActions):

        self.name = name
        self.longDescription = longDescription
        self.shortDescription = shortDescription
        self.actions = actions
        self.adventure = adventure
        self.players = []
        self._entered = False

        self.initAction = DunderActions.get('initAction', None)
        self.enteringAction = None
        self.groupAction = None


    def Enter(self, player):

        self.players.append(player)
        # syntax might be wrong, players class not written yet
        player.room = self

        if not self._entered:
            self._entered = True
            self.initAction.Execute(player)

    def Leave(self, player):

        self.players.remove(player)
        player.room = None
