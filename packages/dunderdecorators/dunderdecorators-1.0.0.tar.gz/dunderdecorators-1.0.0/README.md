By Andy Stokely

Python decorator library that adds customizeable dunder methods to
decorated classes. This both decreases the amount of code that is 
normally required to implement dunder methods, and also helps 
reduce repitition when coding classes that use custom dunder
methods with the same or similar code. Right now, the following
dunder methods have corresponding dunder decorators:

	__iter__ (dunder_iter)
	__setitem__ (dunder_setitem) 
	__getitem__ (dunder_getitem) 
	__missing__ (dunder_missing) 
	__repr__ (dunder_repr) 

If a dunder decorator is used without any parameters,
it defines the special method with respect to the class 
object's dictionary. However, the user is able to have the
special method defined with repsect to one of the class
object's attributes by setting the attr parameter equal
to the name of the attribute. Dunder decorators can also 
be used with classes that use __slots__, rather then a 
dictionary to store object attributes, by setting the 
slots parameter to True. For specific examples,
see the examples in the dunder_decorator.py doc-strings.


