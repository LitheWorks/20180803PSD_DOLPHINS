class TerminationRequested(Exception):
    """
    Players can raise this exception to terminate the game before a fleet has been annihilated.
    """
    pass
