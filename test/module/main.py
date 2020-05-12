import os

SOURCE_DIR = os.path.dirname(os.path.abspath(__file__))


def define_env(env):
    """
    This is the hook for the functions (new form)
    """

    env.variables.cwd = os.getcwd()

    env.variables.project_dir = env.project_dir

    # use dot notation for adding
    env.variables.baz = env.variables.fix_url('foo')

    @env.macro
    def include_file(filename, start_line=0, end_line=None):
        """
        Include a file, optionally indicating start_line and end_line
        (start counting from 0)
        The path is relative to the top directory of the documentation
        project.
        """
        full_filename = os.path.join(SOURCE_DIR, filename)
        with open(full_filename, 'r') as f:
            lines = f.readlines()
        line_range = lines[start_line:end_line]
        return '\n'.join(line_range)
    
