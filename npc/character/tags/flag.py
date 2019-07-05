from .tag import Tag

class Flag(Tag):
    """
    Defines a special type of tag which can be present with no values
    """
    def __init__(self, *args, **kwargs):
        """
        Create a new Flag object

        Args:
            name (str): This tag's name
            args (str): Initial values to populate for this tag
            hidden (bool): Whether this tag should be displayed in character
                listings. When present, a coresponding @hide tag will be
                generated by to_header.
            limit (int): Maximum number of values allowed in the tag. Passing a
                negative number allows an infinite number of values to be
                stored.
        """
        super().__init__(*args, **kwargs)
        self._present = False

    def update(self, values):
        """
        Add the strings in values to our own list of values

        Always set our presence to true when updating

        Args:
            values (list[str]): List of string values to add to this tag
        """
        if type(values) is bool:
            self.touch(values)
        elif type(values) is Flag:
            self.touch(values.present)
            super().update(values)
        else:
            self.touch()
            super().update(values)

    def append(self, value: str):
        """
        Append a value to the tag

        Always set our presence to true when appending. If the value is blank,
        skip it.

        Args:
            value (str): The value to append
        """
        self.touch()
        super().append(value)

    def clear(self):
        """
        Clear out all stored values and reset presence to false
        """
        self._present = False
        super().clear()

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
        self._present = (True and present)

    def validate(self, strict: bool=False):
        """
        Validate this flag's attributes

        Validations:
            * If required is set, at least one value must be present
            * Hidden values must exist
            * (strict) If limit is non-negative, the total values must be <= limit

        Args:
            strict (bool): Whether to report non-critical errors and omissions

        Returns:
            True if this flag has no validation problems, false if not
        """
        self.problems = []

        if self.required and not self.present:
            self.problems.append("No values for flag '{}'".format(self.name))

        for value in [v for v in self.hidden_values if not v in self.data]:
            self.problems.append("Value '{}' for tag '{}' cannot be hidden, because it does not exist".format(value, self.name))

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
        if self.present and not self.filled:
            return "@{}".format(self.name)

        return super().to_header()
