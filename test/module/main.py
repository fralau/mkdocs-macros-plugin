import os




def define_env(env):
    """
    This is the hook for the functions (new form)
    """
    # activate trace
    chatter = env.start_chatting("Simple module")

    env.macros.cwd = os.getcwd()

    # use dot notation for adding
    env.macros.baz = env.macros.fix_url('foo')

    @env.macro
    def include_file(filename, start_line=0, end_line=None):
        """
        Include a file, optionally indicating start_line and end_line
        (start counting from 0)
        The path is relative to the top directory of the documentation
        project.
        """
        chatter("Including:", filename)
        full_filename = os.path.join(env.project_dir, filename)
        with open(full_filename, 'r') as f:
            lines = f.readlines()
        line_range = lines[start_line:end_line]
        return '\n'.join(line_range)
    

    @env.macro
    def doc_env():
        "Document the environment"
        return {name:getattr(env, name) for name in dir(env) if not name.startswith('_')}


    # Optional: a special function for making relative urls point to root
    fix_url = env.macros.fix_url

    @env.macro
    def button(label, url):
        "Add a button"
        chatter("Display a button:", label, url)
        url = fix_url(url)
        HTML = """<a class='md-button' href="%s">%s</a>"""
        return HTML % (url, label)

    
    env.variables.special_docs_dir = env.variables.config['docs_dir']



def on_post_build(env):
    "Post build action"
    # activate trace
    chatter = env.start_chatting("Simple module (post-build)")
    chatter("This means `on_post_build(env)` works")