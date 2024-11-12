"""An item in the library, such as a book, music CD, or video.
   The same rules apply to both physical and digital items.
"""

# The types of items
BOOK = 1
AUDIO = 2
VIDEO = 3

class LibraryItem:
    """A library item has an id, title, and type (book, audio, etc).
    Additional details would be in an ItemDescriptor object, but that
    is omitted for this quiz code.

    :param item_id: the unique id of this library item.
    :param item_title: title of item, such as book or CD title
    :param item_type: the kind of item
    """

    def __init__(self, item_id: str, item_title: str, item_type: int):
        self.item_id = item_id
        self.title = item_title
        self.item_type = item_type

    def __str__(self):
        return f'[{self.item_id}] "{self.title}"'
