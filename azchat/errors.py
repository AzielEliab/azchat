"""AZChat errors. Author: Aziel Eliab only."""


class AzChatError(Exception):
    """Base refuse / engine error."""


class RefuseError(AzChatError):
    """Unknown or refused op."""
