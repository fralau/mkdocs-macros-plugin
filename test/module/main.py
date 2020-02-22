import os

import subprocess
def define_env(env):
    """
    This is the hook for the functions (new form)
    """

    env.variables['cwd'] = os.getcwd()

    env.variables['project_dir'] = env.project_dir
    
    GIT_VERSION = ['git', 'describe', '--tags']
    env.variables['git_version'] = subprocess.check_output(GIT_VERSION, 
                                            text=True).strip()
