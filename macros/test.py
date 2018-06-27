# --------------------------------------------
# This is a test file and example of how functions file should be defined
# By default it should be called 'code.py'
# Or in a file of a properly defined python package called 'code'.
#
# Laurent Franceschetti (c) 2018
# --------------------------------------------

def declare_variables(variables, template_function):
    "This is the hook for the functions"

    variables['baz'] = 6

    @template_function
    def bar(x):
        return (2.3 * x) + 7
