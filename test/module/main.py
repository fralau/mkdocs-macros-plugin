import os

import subprocess
def define_env(env):
    """
    This is the hook for the functions (new form)
    """

    env.variables['cwd'] = os.getcwd()

    env.variables['project_dir'] = env.project_dir
    
