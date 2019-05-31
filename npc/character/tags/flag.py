from .tag import Tag

class Flag(Tag):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._present = False

    @property
    def present(self):
        """
        Whether this flag is meaningfully present in the character

        True whenever the flag has data or has been marked present by calling
        touch().
        """
        return super().present or self._present

    def touch(self, present: bool = True):
        """
        Manually mark this flag as present in a character.

        Args:
            present (bool): Whether to mark the flag present or not present.
                Defaults to True.

        Returns:
            None
        """
        self._present = present

    def validate(self, strict=False):
        """
        Validate this flag's attributes

        Validations:
            * If required is set, at least one value must be present
            * (strict) If limit is non-negative, the total values must be <= limit

        Args:
            strict (bool): Whether to report non-critical errors and omissions

        Returns:
            True if this flag has no validation problems, false if not
        """
        self.problems = []

        if self.required and not self.present:
            self.problems.append("No values for flag '{}'".format(self.name))

        if strict:
            if self.limit > -1 and len(self.data) > self.limit:
                self.problems.append("Too many values for flag '{}'. Limit of {}".format(self.name, self.limit))

        return self.valid

    def to_header(self):
        """
        Generate a text header representation of this flag

        This creates the appropriate `@flag value` lines that, when parsed, will
        recreate the data of this flag. If the flag is marked as hidden, an
        additional `@hide flag` will be appended. If `.present` is false, an
        empty string is returned.

        If the flag has no values, but is marked present, a simple `@flag` line
        will be returned.

        Returns:
            A string of the header lines needed to create this flag, or an empty
            string if the present is false.
        """
        if self.present and not self.data:
            return "@{}".format(self.name)

        return super().to_header()
