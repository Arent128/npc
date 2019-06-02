from .flag import Flag

class UnknownTag(Flag):
    """
    Defines a mult-value unrecognized tag object

    These are special tag objects that represent an unexpected or unknown tag.
    They are added automatically when attempting to access a tag that was not
    initialized.

    These tags cannot be required and will always be invalid in strict mode.
    """
    def __init__(self, name: str, *args, hidden: bool=False, limit: int=-1):
        """
        Create a new Tag object

        Args:
            hidden (bool): Whether this tag should be displayed in character
                listings. When present, a coresponding @hide tag will be
                generated by to_header.
            limit (int): Maximum number of values allowed in the tag. Passing a
                negative number allows an infinite number of values to be
                stored.
            values (list): Initial values to save
        """
        super().__init__(name, *args, required=False, hidden=hidden, limit=limit)
        self._present = True

    def __repr__(self):
        return "{}({}, {}, hidden={}, limit={})".format(
            type(self).__name__,
            self.name,
            *self.data,
            self.hidden,
            self.limit
        )

    def validate(self, strict=False):
        """
        Validate this tag's attributes

        Validations:
            * Required is incompatible with a limit of zero
            * (strict) If limit is non-negative, the total values must be <= limit
            * (strict) This tag is always invalid in strict mode

        Args:
            strict (bool): Whether to report non-critical errors and omissions

        Returns:
            True if this tag has no validation problems, false if not
        """
        if strict:
            self.problems.append("Unrecognized tag '{}'".format(self.name))
            if self.limit > -1 and len(self.data) > self.limit:
                self.problems.append("Too many values for tag '{}'. Limit of {}".format(self.name, self.limit))

        return self.valid
