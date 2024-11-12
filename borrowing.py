"""A record of the borrowing of a library item.

The borrowing records name and id of Patron who borrowed the item,
date borrowed, due date, and status (checked out, returned).
"""
from datetime import date, timedelta
from utils import parse_date
from library_item import LibraryItem, BOOK, AUDIO, VIDEO
import utils


class Borrowing:
    """Record the checkout (borrowing) of a library item. The due date is computed from 
    the `checkout_date` and the item type.

    :param item: the LibraryItem that patron borrows from Library
    :param patron_id, patron_name, patron_email: the patron who is borrowing the item.
    :param checkout_date: date the item was borrowed (datetime.date or "yyyy-mm-dd").
                          Default value is today.
    """

    def __init__(self, item: LibraryItem,
                       patron_id: str, patron_name: str, patron_email: str,  
                       checkout_date: date|str = None):
        self.patron_id = patron_id 
        self.patron_name = patron_name
        self.patron_email = patron_email
        self.item = item
        # compute checkout as a date object
        if checkout_date:
            self.checkout_date = parse_date(checkout_date)
        else:
            self.checkout_date = utils.today()
    
    @property
    def due_date(self) -> date:
        """Get the due date for this borowed item."""
        if self.item.item_type == BOOK:
            return self.checkout_date + timedelta(days=14)
        elif self.item.item_type == AUDIO:
            return self.checkout_date + timedelta(days=7)
        elif self.item.item_type == VIDEO:
            return self.checkout_date + timedelta(days=5)
        raise ValueError(f"Unknown item type {self.item.item_type}")

    def __str__(self):
        """String representation of a borrowing record."""
        overdue = " [OVERDUE]" if self.due_date < utils.today() else ""
        return f'Item {self.item.item_id} checked out {self.checkout_date} due {self.due_date}{overdue}'
