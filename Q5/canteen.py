"""Q5 - Canteen order system: default-parameter bug, correct design, return values, scope."""

GST_RATE = 5                              # percent (global constant, read only)

# ------------- the bug (Complete the Code) -------------
def add_item_buggy(item, order=[]):
    order.append(item)
    return order

def add_item(item, order=None):
    # TODO 1 (done): new empty list when order is None, append the item, return the list
    if order is None:
        order = []
    order.append(item)
    return order

# ------------- order functions with positional / keyword / default parameters -------------
MENU = {"Tea": 10, "Vada": 15, "Dosa": 40, "Coffee": 12}

def add_to_order(item, quantity=1, order=None):
    """item: positional; quantity: default 1; order: None means 'start a new order'. Returns the order dict."""
    if order is None:
        order = {}
    order[item] = order.get(item, 0) + quantity
    return order

def bill(order, gst_rate=GST_RATE):
    """Returns TWO (three) values: subtotal, gst, total (a tuple). All in rupees (int paise avoided by whole-rupee prices)."""
    subtotal = sum(MENU[item] * qty for item, qty in order.items())
    gst = round(subtotal * gst_rate / 100, 2)
    return subtotal, gst, subtotal + gst

# ------------- scope demonstrations -------------
counter_global = 0

def local_demo():
    x = "local"                      # exists only inside the function
    return x

def read_global():
    return counter_global            # reading a global needs no keyword

def change_global_wrong():
    counter_global = 99              # creates a NEW local name; the global is untouched

def change_global_right():
    global counter_global            # explicit: rebind the module-level name
    counter_global += 1

def make_order_taker():
    """Closure: the order lives inside the outer function; the inner function remembers it (nonlocal)."""
    order = []
    def add(item):
        order.append(item)           # mutating a list needs no nonlocal
        return list(order)
    return add

def make_counter():
    count = 0
    def next_token():
        nonlocal count               # rebinding an enclosing name needs nonlocal
        count += 1
        return count
    return next_token
