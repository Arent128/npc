from collections import UserDict
from copy import copy
from npc.util import print_err

from .sub_tag import SubTag

class GroupTag(UserDict):
    """
    Defines a mult-value tag object
    """
    def __init__(self,
        name: str,
        *args,
        required: bool=False,
        hidden: bool=False,
        limit: int=-1,
        subtag: str='rank',
        **kwargs):
        """
        Create a new Tag object

        Initial values must be formatted as appropriate for creating a new dict.

        Args:
            name (str): This tag's name
            args (list(str)): Initial values to populate for this tag. Each will
                be given a correct subtag.
            kwargs: Initial values to populate for this tag. This directly
                populates the underlying dict.
            required (bool): Whether this tag must be filled for the character
                to be valid.
            hidden (bool): Whether this tag should be displayed in character
                listings. When filled, a coresponding @hide tag will be
                generated by to_header.
            limit (int): Maximum number of values allowed in the tag. Passing a
                negative number allows an infinite number of values to be
                stored.
            subtag (str): Name of the tag used to hold sub-values for each
                value.
        """
        self.name = name
        self.required = required
        self.hidden = hidden
        self.hidden_values = []
        self.limit = limit
        self.problems = []
        self.subtag_name = subtag

        super().__init__(**kwargs)

        self.update(args)

    def __repr__(self):
        return "{cls}('{name}', {data}, required={req}, hidden={hidden}, hidden_values={hidden_vals}, limit={limit}, subtag='{subtag}')".format(
            cls=type(self).__name__,
            name=self.name,
            data=self.data,
            req=self.required,
            hidden=self.hidden,
            hidden_vals=self.hidden_values,
            limit=self.limit,
            subtag=self.subtag_name
        )

    def update(self, values):
        """
        Add the data in values to our own data

        Values can be either a group tag or a list of strings. A list of strings
        will have each of its members added with an appropriate subtag. Group
        tags will have their own subtags added verbatim.

        Args:
            values (list[str]|GroupTag): Values to add to this tag
        """
        if type(values) == GroupTag:
            for key, subtag in values.items():
                self.data[key] = subtag
        else:
            for val in values:
                self.data[val] = SubTag(self.subtag_name)

    @property
    def filled(self):
        """
        bool: Whether this tag is meaningfully filled in the character

        True whenever the tag has data
        """
        return len(self.data) > 0

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

    def append(self, val: str):
        """
        Add a new value to the tag

        Adds val as a new tag value with no subtags.

        Does nothing if val is already filled.

        Args:
            val (str): The new value to add
        """
        if val in self.data:
            return

        self.data[val] = SubTag(self.subtag_name)

    def subtag(self, val: str):
        """
        Get the subtag object for a given group name value

        Args:
            val (str): Group name

        Returns
            SubTag object for the named subtag
        """
        return self.data[val]

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
            * Subtags must have the correct name
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

        for value, subtag in self.data.items():
            if subtag.name != self.subtag_name:
                self.problems.append("Tag '{}' uses subtag '{}', but found '{}' for '{}'".format(self.name, self.subtag_name, subtag.name, value))

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
        for val, subtag in self.data.items():
            header_lines.append("@{} {}".format(self.name, val))
            if val in self.hidden_values:
                header_lines.append("@hide {} >> {}".format(self.name, val))
            header_lines.append(subtag.to_header(self.name, val))

        if self.hidden:
            header_lines.append("@hide {}".format(self.name))

        return "\n".join([line for line in header_lines if line])

    def tagslice(self, start, stop):
        """
        Create a new tag with a slice of our data

        This applies a basic slice operation to the stored values and creates a
        copy of this tag object whose data is the new slice. This is primarily
        used for generating limited headers.

        Since dicts do not normally allow slicing, this method emulates slice
        behavior by slicing the keys and creating a new dict containing only
        those keys. The end result is intuitive and preserves the values
        expected.

        Args:
            start (int|None): First index included in the slice
            stop (int|None): Index to end the slice, not included in the slice itself

        Returns:
            Tag object containing the sliced values
        """
        new_tag = copy(self)
        new_keys = list(self.data)[start:stop]
        new_tag.data = {k: v for k, v in self.data.items() if k in new_keys}
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
        Get the first stored key as a bare string

        This method has a confusing name to match the name on Tag

        Returns:
            String or None
        """
        if self.filled:
            return next(iter(self))
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
            if self[real_value].contains(value):
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
        Also asks subtags to hide themselves if needed
        """
        if self.hidden:
            self.clear()

        for value in self.hidden_values:
            try:
                del self.data[value]
            except KeyError:
                continue

        for subtag in self.values():
            subtag.sanitize()
