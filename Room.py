

class Room:

    def __init__(self, name, longDescription, shortDescription, actions, **DunderActions):

        self.name = name
        self.longDescription = longDescription
        self.shortDescription = shortDescription
        self.actions = actions
        self.players = []
        self._entered = False

        self.initAction = DunderActions.get('initAction', None)
        self.enteringAction = None
        self.groupAction = None

        if 'initAction' in MagicActions:
            self.initAction = MagicActions['initAction']
        if 'enteringAction' in MagicActions:
            self.enteringAction = MagicActions['enteringAction']
        if 'partyAction' in MagicActions:
            self.groupAction = MagicActions['partyAction']


    def Enter(self, player):

        self.players.append(player)
        # syntax might be wrong, character class not written yet
        player.room = self

        if not self._entered:
            self._entered = True
            self.initAction.Execute(player)

    def Leave(self, player):

        self.players.remove(player)
        player.room = None
