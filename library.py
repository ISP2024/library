"""The library maintains a collection of items
and managed checkout and return of items.
"""
import datetime  # for date
import logging
from library_item import LibraryItem, BOOK, AUDIO, VIDEO
from borrowing import Borrowing
import utils


class Library:
    """Library has a collection of items in the library
    and manages checkout and return of these items.
    
    It also computes late fee for overdue items (in `return_item`).
    """

    def __init__(self):
        # Mapping of all checked out items, indexed by item_id.
        self.checkouts: dict[str, Borrowing] = {}  # item_id -> Borrowing
    
    def checkout(self, item: LibraryItem, patron_id, patron_name, patron_email,
                       checkout_date: datetime.date|str = None) -> Borrowing:
        """Checkout a library item to a patron.

        Checkout may fail if a) item is already checked out,
        or b) patron currently has 4 or more checked out items (4 is the max).

        :param item: the item to checkout
        :param patron_id, patron_name, patron_email: the patron borrowing this item
        :param checkout_date: (optional) date or "yyyy-mm-dd" of checkout. Default is today.
        :returns: a Borrowing object if successful, None if cannot borrow this item.
        """
        if item.item_id in self.checkouts:
            logging.warning(f"Checkout item {item.item_id} failed: this item is currently checked out.")
            return None
        # how many items are checked out to this patron?
        number_borrowed = len(self.get_borrowed_items(patron_id))
        if number_borrowed >= 4:
            logging.warning(f"Patron has checked out {number_borrowed} items. Cannot checkout any more")
            return None
        # maintain a record of this borrowing
        borrowing = Borrowing(item, patron_id, patron_name, patron_email, checkout_date) 
        self.checkouts[item.item_id] = borrowing
        return borrowing

    # Don't change this method signature (the parameters).
    # When an item is returned the librarian scans the item's barcode 
    # (item_id) and inputs it here. The only available info is the item_id.
    def return_item(self, item_id):
        """Process an item return.

           :param item_id: the library item id of the thing being returned
           :returns: the late fee (in Baht) or 0 if no late fee
           :raises ValueError: if item_id is not the id of a checked-out item
        """
        if item_id in self.checkouts:
            borrowing = self.checkouts[item_id]
            # remove item from the collection of checkout-out items
            del(self.checkouts[item_id])
            # is there any overdue fine?
            if self.is_overdue(borrowing):
                # compute the late fine
                time_overdue = utils.today() - borrowing.due_date
                days_overdue = time_overdue.days
                if borrowing.item.item_type == BOOK:
                    # 3 day grace period, then 10 Baht/day
                    late_fee = max(0, 10*(days_overdue - 3))
                elif borrowing.item.item_type == AUDIO:
                    # 2 day grace period, then 15 Baht/day
                    late_fee = max(0, 15*(days_overdue - 2))
                elif borrowing.item.item_type == VIDEO:
                    # no grace period, 20 Baht/day
                    late_fee = 20*days_overdue
                return late_fee
            else:
                # item returned on time
                return 0
        else:
            logging.error(f"Return of item {item_id} that is not checked out.""")
            raise ValueError(f"Item {item_id} is currently not checked out.")
    
    # Don't change this method signature.
    # We want to be able to find borrowings using just the patron's id,
    # which is as printed or encoded on the patron's library card.
    def get_borrowed_items(self, patron_id) -> list[Borrowing]:
        """Get all the items borrowed by a given Patron."""
        return [item for item in self.checkouts.values() if item.patron_id == patron_id]    

    def get_borrowed_item(self, item_id) -> Borrowing:
        """Find a single borrowed item by its library item id.
        :return: a Borrowing record or None if item is not checked out.
        """
        return self.checkouts.get(item_id)

    def is_overdue(self, borrowing: Borrowing) -> bool:
        """Return True if an item is overdue, 0 otherwise."""
        return utils.today() > borrowing.due_date
