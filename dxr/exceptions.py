"""Exceptions, broken out into a leaf module to ward off circular imports"""


class BadTerm(Exception):
    """A user error made it impossible to filter on a term."""

    def __init__(self, reason):
        """Construct.

        :arg reason: User-readble error message telling the user what is
            wrong and how to fix it. Can be Unicode or Markup.

        """
        self.reason = reason