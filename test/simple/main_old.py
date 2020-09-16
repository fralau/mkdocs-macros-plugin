import os

def define_env(env):
    """
    This is the hook for the functions (new form)
    """

    env.variables['cwd'] = os.getcwd()
