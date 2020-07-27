'''
Real Python Video Tutorial Series
Understanding the Python Zip Function
@author Liam Pulsifer
April, 2020 
'''

''' 
How Zip Works
'''
# Basic Example
prices = [10000, 20000, 15000]
cars = ["small", "large", "medium"]
colors = ["red", "blue"]

# Zip returns an iterator (zip object)
prices_cars = zip(prices, cars)

for price, car_size in prices_cars:
    #print (price, car_size)
    pass

# Convert to a list for easy viewing
list_version = list(prices_cars)

# Length of output determined by length of shortest input
prices_cars_colors = zip(prices, cars, colors)

# Use itertools.zip_longest for the opposite behavior
from itertools import zip_longest
prices_cars_colors = zip_longest(prices, cars, colors)

# Use fillvalue parameter to decide what fills the rest of the 
# shorter inputs
prices_cars_colors = zip_longest(prices, cars, colors, fillvalue="?")

'''
Zip in different Python Versions
'''

# Zip in Python2 returns a list
# Use itertools.izip for Python3 behavior in Python2
# Use list(zip(...)) to get Python2 behavior in Python3

# Remember that converting to a list uses more memory! 

# Trick for dealing with different versions

try:
    from itertools import izip as zip
except ImportError:
    print ("Must be Python3")
    pass

''' 
Iterating through parallel iterables
''' 

tools = ["Hammer", "Nail", "Sandpaper", "Bucket"]
prices = [18.99, 2.99, 1.99, 5.99]
sales = [10, 50, 23, 3]

for tool, price, sale in zip(tools, prices, sales):
    print (f"Total sales for tool <{tool}> is ${price * sale}")

userids = {"James1": 1, "John123": 2}
usertypes = {1: "Admin", 2: "Normal"}

for (uname, uid1), (uid2, utype) in zip(userids.items(), usertypes.items()):
    print(f"User with name {uname} has type {utype}")

''' 
Other applications
'''

# Creating dictionaries
tool_dict = dict(zip(tools, prices))

# Sorting
sorted_by_price = sorted(zip(prices, tools, sales))

sorted_by_toolname = sorted(zip(tools, prices, sales))

# With list comprehensions
total_sales = [price * sale for price, sale in zip(prices, sales)]

# With dict comprehension
tool_to_sales = {tool: price * sale for price, sale, tool in zip(prices, sales, tools)}




