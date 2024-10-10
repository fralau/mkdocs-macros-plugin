def foo(x:int, y:str):
  "First macro"
  return f"{x} and {y}"

def bar(x:int, y:int):
  "Second macro"
  return x + y

def scramble(s:str, length:int=None):
    """
    Dummy filter to reverse the string and swap the case of each character. 

    Usage in Markdown page:

    {{ "Hello world" | scramble }}    -> Dlrow Olleh
    {{ "Hello world" | scramble(6) }} -> Dlrow
    """
    # Split the phrase into words
    words = s.split()
    # Reverse each word and then reverse the order of the words
    reversed_words = [word[::-1].capitalize() for word in words][::-1]
    # Join the reversed words to form the new phrase
    new_phrase = ' '.join(reversed_words)
    if length:
       new_phrase = new_phrase[length]
    return new_phrase


MY_FUNCTIONS = {"foo": foo, "bar": bar}
MY_VARIABLES = {"x1": 5, "x2": 'hello world'}
MY_FILTERS   = {"scramble": scramble}


def on_config(config, **kwargs):
    "Add the functions variables and filters to the mix"
    # get MkdocsMacros plugin, but only if present
    macros_plugin = config.plugins.get("macros")
    if macros_plugin:
      macros_plugin.register_macros(MY_FUNCTIONS)
      macros_plugin.register_variables(MY_VARIABLES)
      macros_plugin.register_filters(MY_FILTERS)
    else:
       raise SystemError("Cannot find macros plugin!")

