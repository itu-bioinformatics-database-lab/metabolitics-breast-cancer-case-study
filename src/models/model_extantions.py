import cobra as cb


def subsystems(self):
    ''' Gives subsystems of reactions '''
    return set([r.subsystem for r in self.reactions])


cb.Model.subsystems = subsystems
