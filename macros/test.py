# --------------------------------------------
# This is a test file and example of how functions file should be defined
# By default it should be called 'main.py'
# Or in a file of a properly defined python package called 'main'.
# It is actually used by module_reader.py
# --------------------------------------------

def declare_variables(variables, macro):
    """
    This is the hook for the functions

    - variables: the dictionary that contains the variables
    - macro: a decorator function, to declare a macro.
    """

    variables['baz'] = "John Doe"

    @macro
    def bar(x):
        return (2.3 * x) + 7



    # If you wish, you can  declare a macro with a different name:
    def f(x):
        return x * x

    f = macro(f, 'barbaz')
