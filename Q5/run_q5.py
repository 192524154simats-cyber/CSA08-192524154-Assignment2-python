from canteen import *
import canteen

print("== Complete the Code ==")
print(add_item_buggy("Tea"), add_item_buggy("Vada"))
print(add_item("Tea"), add_item("Vada"))
print("add_item_buggy.__defaults__ =", add_item_buggy.__defaults__)
print("add_item.__defaults__       =", add_item.__defaults__)
print("(expected output: ['Tea', 'Vada'] ['Tea', 'Vada']  then  ['Tea'] ['Vada'])")

print("\n== Explanation in numbers ==")
print("The default [] was created ONCE when 'def' ran: id =", id(add_item_buggy.__defaults__[0]))
a = add_item_buggy("Dosa"); b = add_item_buggy("Coffee")
print("a is b (both calls return the same list object):", a is b, "->", b)

print("\n== Three customers in sequence (corrected design) ==")
orders = []
for customer, items in (("Customer 1", [("Tea", 2), ("Vada", 1)]),
                        ("Customer 2", [("Dosa", 1)]),
                        ("Customer 3", [("Coffee", 3), ("Tea", 1), ("Dosa", 2)])):
    order = None                                     # new customer: no order yet
    for name, qty in items:
        order = add_to_order(name, qty, order)       # positional + positional + passes the order along
    orders.append(order)
    sub, gst, total = bill(order)                    # returns more than one value (tuple unpacking)
    print(f"{customer}: {order}  subtotal {sub}  GST {gst}  total {total}")
print("Each order independent:", orders[0] is not orders[1] and orders[1] is not orders[2],
      "| customer 1 has no Dosa:", "Dosa" not in orders[0])
print("keyword call: add_to_order('Vada', order=None, quantity=4) ->", add_to_order("Vada", order=None, quantity=4))
print("default GST vs keyword:", bill({"Tea": 10})[1], bill({"Tea": 10}, gst_rate=18)[1])
print("bill returns a", type(bill({"Tea": 1})).__name__, ":", bill({"Tea": 1}))

print("\n== Scope: local / global / nonlocal ==")
print("local_demo() =", local_demo())
try:
    print(x)
except NameError as e:
    print("x outside the function -> NameError:", e)
print("read_global() =", read_global())
change_global_wrong(); print("after change_global_wrong() global =", canteen.counter_global, "(unchanged: the function made a local variable)")
change_global_right(); print("after change_global_right() global =", canteen.counter_global, "(changed because of the global keyword)")
token = make_counter()
print("closure counter (nonlocal):", token(), token(), token())
t1, t2 = make_order_taker(), make_order_taker()
t1("Tea"); t1("Vada"); t2("Dosa")
print("two closures, two separate orders:", t1("Coffee"), t2("Tea"))
