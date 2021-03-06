from collections import UserList
from copy import copy
from npc.util import print_err

class Tag(UserList):
    """
    Defines a mult-value tag object
    """
    def __init__(self, name: str, *args, required: bool=False, hidden: bool=False, limit: int=-1):
        """
        Create a new Tag object

        Args:
            name (str): This tag's name
            args (str): Initial values to populate for this tag
            required (bool): Whether this tag must be filled for the character
                to be valid.
            hidden (bool): Whether this tag should be displayed in character
                listings. When filled, a coresponding @hide tag will be
                generated by to_header.
            limit (int): Maximum number of values allowed in the tag. Passing a
                negative number allows an infinite number of values to be
                stored.
        """
        self.name = name
        self.required = required
        self.hidden = hidden
        self.hidden_values = []
        self.limit = limit
        self.problems = []
        self.subtag_name = None

        super().__init__(args)

    def __repr__(self):
        return "{cls}('{name}', {data}, required={req}, hidden={hidden}, hidden_values={hidden_vals}, limit={limit})".format(
            cls=type(self).__name__,
            name=self.name,
            data=self.data,
            req=self.required,
            hidden=self.hidden,
            hidden_vals=self.hidden_values,
            limit=self.limit
        )

    def update(self, values):
        """
        Add the strings in values to our own list of values

        Args:
            values (list[str]): List of string values to add to this tag
        """
        if hasattr(values, 'hidden'):
            self.hidden = values.hidden
        if hasattr(values, 'hidden_values'):
            self.hidden_values.extend(values.hidden_values)

        if hasattr(values, 'data'):
            self.data = values.data
        else:
            self.data = values

    def append(self, value: str):
        """
        Append a value to the tag

        If the value is blank, skip it

        Args:
            value (str): The value to append
        """
        if not value.strip():
            return

        super().append(value)

    @property
    def filled(self):
        """
        bool: Whether this tag has meaningful data

        True whenever the tag has data
        """
        return len(self.filled_data) > 0

    @property
    def present(self):
        """
        bool: Whether this tag is considered "present" in the character

        True whenever the tag should be included in the character. Defaults to
        whether the tag has data.
        """
        return self.filled

    def __bool__(self):
        """
        Delegate truthyness to the `present` property
        """
        return True and self.present

    @property
    def filled_data(self):
        """
        list: All non-whitespace values
        """
        return [v for v in self.data if v.strip()]

    def touch(self, present: bool = True):
        """
        No-op for compatibility with Flag class

        Args:
            present (bool): Whether to mark the flag present or not present.
                Defaults to True.

        Returns:
            None
        """
        print_err("Calling touch() on non-flag class {} object '{}'".format(type(self).__name__, self.name))

    def subtag(self, val: str):
        """
        No-op for compatibility with GroupTag class

        Args:
            val (str): Group name

        Returns:
            None
        """
        print_err("Calling touch() on non-flag class {} object '{}'".format(type(self).__name__, self.name))

    @property
    def valid(self):
        """
        bool: Whether this tag is internally valid

        This property is only meaningful after calling validate()
        """
        return len(self.problems) == 0

    def validate(self, strict: bool=False):
        """
        Validate this tag's attributes

        Validations:
            * If required is set, at least one value must be filled
            * Required is incompatible with a limit of zero
            * Hidden values must exist
            * (strict) If limit is non-negative, the total values must be <= limit

        Args:
            strict (bool): Whether to report non-critical errors and omissions

        Returns:
            True if this tag has no validation problems, false if not
        """
        self.problems = []

        if self.required and not self.filled:
            self.problems.append("No values for tag '{}'".format(self.name))

        if self.required and self.limit == 0:
            self.problems.append("Tag '{}' is required but limited to zero values".format(self.name))

        for value in [v for v in self.hidden_values if not v in self.data]:
            self.problems.append("Value '{}' for tag '{}' cannot be hidden, because it does not exist".format(value, self.name))

        if strict:
            if self.limit > -1 and len(self.data) > self.limit:
                self.problems.append("Too many values for tag '{}'. Limit of {}".format(self.name, self.limit))

        return self.valid

    def to_header(self):
        """
        Generate a text header representation of this tag

        This creates the appropriate `@tag value` lines that, when parsed, will
        recreate the data of this tag. If the tag is marked as hidden, an
        additional `@hide tag` will be appended. If `.filled` is false, an
        empty string is returned.

        Returns:
            A string of the header lines needed to create this tag, or an empty
            string if the filled is false.
        """
        if not self.filled:
            return ''

        header_lines = []
        for val in self.data:
            header_lines.append("@{} {}".format(self.name, val))
            if val in self.hidden_values:
                header_lines.append("@hide {} >> {}".format(self.name, val))

        if self.hidden:
            header_lines.append("@hide {}".format(self.name))

        return "\n".join(header_lines)

    def tagslice(self, start, stop):
        """
        Create a new tag with a slice of our data

        This applies a basic slice operation to the stored values and creates a
        copy of this tag object whose data is the new slice. This is primarily
        useful for generating limited headers.

        Args:
            start (int|None): First index included in the slice
            stop (int|None): Index to end the slice, not included in the slice itself

        Returns:
            Tag object containing the sliced values
        """
        new_tag = copy(self)
        new_tag.data = self.data[start:stop]
        return new_tag

    def first(self):
        """
        Get a copy of this tag containing only the first value

        Convenience method that's identical to calling `tagslice(0, 1)`

        Returns:
            Tag object containing the first value
        """
        return self.tagslice(0, 1)

    def remaining(self):
        """
        Get a copy of this tag excluding the first value

        Convenience method that's identical to calling `tagslice(1, None)`

        Returns:
            Tag object excluding the first value
        """
        return self.tagslice(1, None)

    def first_value(self):
        """
        Get the first stored value as a bare string

        Returns:
            String or None
        """
        if self.filled:
            return self[0]
        else:
            return None

    def contains(self, value: str):
        """
        Determine whether this tag contains a particular value

        When value is the special '*' char, contains will be true if the tag is
        filled.

        Otherwise, contains is only true when the value is wholly or partially
        filled in at least one value. The comparison is done using casefold()
        to avoid case conflicts.

        Args:
            value (str): Value to search for

        Returns:
            True if this tag contains value, false if not.
        """
        if value == '*' and self.filled:
            return True

        value = value.casefold()
        for real_value in self:
            if value in real_value.casefold():
                return True

        return False

    def hide_value(self, value):
        """
        Hide a single value for this tag

        Hiding will only work if the value to be hidden exactly matches a value
        present in this tag's data.

        Args:
            value (str): The value to hide
        """
        self.hidden_values.append(value)

    def sanitize(self):
        """
        Remove this tag's values if the tag is marked hidden
        """
        if self.hidden:
            self.clear()

        for value in self.hidden_values:
            try:
                self.data.remove(value)
            except ValueError:
                continue
