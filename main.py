from library import Library
from library_item import LibraryItem, BOOK, VIDEO, AUDIO
from datetime import date, timedelta
import re
import utils


library = Library()

# TODO: revise this to use your refactoring
patron_name = "Edward Snowden"
patron_id = "1234"
patron_email = "snowden@protonmail.com"


def borrow_item(item: LibraryItem, borrow_date: date = utils.today()):
    """Borrow something from the Library, using the patron data above."""
    try:
        checkout_date = borrow_date
        print(f'Check out {item} on {checkout_date}')
        # TODO Revise this after you refector Library.checkout
        borrowing = library.checkout(item, patron_id, patron_name, patron_email, checkout_date=checkout_date)
        if borrowing:
            print("> Checkout OK")
            print(f"> Date due {borrowing.due_date}")
        else:
            print("> Checkout Failed")
    except Exception as ex:
        print(f"Checkout raised exception: {ex}")


def return_item(item_id: str):
    """Return an item to the library. Librarian inputs the item_id into system."""
    borrowed_item = library.get_borrowed_item(item_id)
    if not borrowed_item:
        print(f"{item_id} is not checked out")
        return
    print("-" * 40)
    print(f'Return "{borrowed_item.item.title}" on {utils.today()}')
    print("Due Date:", borrowed_item.due_date)
    #TODO Revise this after you refactor is_overdue
    print("Status:  ", "OVERDUE" if library.is_overdue(borrowed_item) else "Normal")
    fine = library.return_item(borrowed_item.item.item_id) 
    print("Late Fee: ", fine)
    # verify it has been returned
    if library.get_borrowed_item(item_id) is None:
        print("Item Returned to Library")
    else:
        print("Oops! Library thinks this item is still checked out.")


def print_statement():
    # get the items borrowed by this patron
    borrowed = library.get_borrowed_items(patron_id)
 
    print("")
    print(f"Statement for patron {patron_name} on {utils.today()}")
    print("-" * 50)
    print(f"Item Id  {'Title':28} {'Checkout':10}  {'Due Date':10}  Status")
    for borrowing in borrowed:
        if library.is_overdue(borrowing):
            time_overdue = utils.today() - borrowing.due_date
            days_overdue = time_overdue.days
            status = f"OVERDUE {days_overdue} days"
        else:
            status = ""
        print(f"{borrowing.item.item_id:7} {borrowing.item.title:28}  "
              f"{borrowing.checkout_date}  {borrowing.due_date}  {status}")

if __name__ == '__main__':
    today = utils.today()
    
    input("Press ENTER to checkout some Library Items...")
    print("-" * 46)
    myborrowed = []
    # some items we want to borrow
    item1 = LibraryItem("111", "Secure by Design", BOOK)
    item2 = LibraryItem("253", "CitizenFour (video)", VIDEO)
    item3 = LibraryItem("388", "The Snowball (audiobook)", AUDIO)
    item4 = LibraryItem("117", "Inside the Machine", BOOK)
    item5 = LibraryItem("189", "Programming Python", BOOK)

    # Checkout from the library!
    # If you want to checkout in the past, add a second parameter:
    # borrow_item(item1, utils.today() + timedelta(days=-4))
    borrow_item(item1)
    borrow_item(item2)
    borrow_item(item3)
    borrow_item(item4, today)
        # next item cannot be borrowed (too many checkouts)
    borrow_item(item5, today)

    # Print a list of borrowings
    input("Press ENTER to print statement of borrowed items...")
    print_statement()

    # Go to the future a few days and repeat
    ndays = 4
    while True:
        utils.set_today(utils.today()+timedelta(days=ndays))  # move forward in time
        print(f"\n{ndays} days later. Today is now {utils.today()}.")
        input("Press ENTER to print statement of borrowed items...")
        print_statement()
        myborrowed = library.get_borrowed_items(patron_id)
        if not myborrowed:
            break
        reply = input("\nEnter item id to return or ENTER to keep all items: ")
        reply = reply.strip()
        if reply == "q" or reply == "quit":
            break
        if reply:
            return_item(reply)
    # final statement       
    print_statement()
