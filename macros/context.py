"""
Basic context for the jinja2 templates.

"Batteries included": It defines standard variables, macros and filters
that a template designer is likely to need.

It contains in particular documentation functions.

Laurent Franceschetti (c) 2020
"""
import os, sys, subprocess, platform
import pkg_resources
import datetime



import mkdocs, jinja2
from jinja2 import Template
from markdown import markdown


# ---------------------------------
# Initialization
# ---------------------------------
# Local directory
SOURCE_DIR = os.path.dirname(os.path.abspath(__file__))

# Name of the package (for version)
PACKAGE_NAME = 'mkdocs-macros-plugin'

# ---------------------------------
# Documentation utilities
# ---------------------------------


def list_items(obj):
    """
    Returns a list of key,value pairs for the content of an object
    Creates an abstraction layer so that we do not have to worry.
    """
    try:
        return obj.items()
    except AttributeError:
            # it's an object
            return obj.__dict__.items()
    except TypeError:
        # it's a list: enumerate
        return enumerate(list(obj))


def get_first_para(s):
    "Get the first para of a docstring"
    first_lines = []
    for row in s.strip().splitlines():
        if not row:
            break
        else:
            first_lines.append(row)
    r = ' '.join(first_lines).strip()
    # fix last character that ends with a semi-colon
    if r.endswith(':'):
        r = r[:-1] + '.'
    return r
    


def format_value(value):
    "Properly format the value, to make it descriptive"
    # those classes will be processed as "dictionary type"
    # NOTE: using the name does nto force us to import them
    LISTED_CLASSES = 'Config', 'File', 'Section'
    # those types will be printed without question
    SHORT_TYPES = int, float, str, list  
    if callable(value):
        # for functions
        docstring = get_first_para(value.__doc__)
        # we interpret the markdown in the docstring, 
        # since both jinja2 and ourselves use markdown, 
        # and we need to produce a HTML table:
        docstring = markdown(docstring)
        try:
            varnames = ', '.join(value.__code__.co_varnames)
            return "(<i>%s</i>)<br/> %s" % (varnames, docstring)
        except AttributeError:
            # code not available
            return docstring
    elif (isinstance(value, dict) or 
        type(value).__name__ in LISTED_CLASSES):
        # print("Processing:", type(value).__name__, isinstance(value, SHORT_TYPES))
        r_list = []
        for key, value in list_items(value):
            if isinstance(value, SHORT_TYPES):
                r_list.append("%s = %s" % (key, repr(value)))
            else:
                # object or dict: write minimal info:
                r_list.append("<b>%s</b> [<i>%s</i>]" % 
                            (key, type(value).__name__))
        return ', '.join(r_list)
    else:
        return repr(value)




def make_html(rows, header=[], tb_class='pretty'):
    "Produce an HTML table"
    back_color = "#F0FFFF" # light blue
    grid_color = "#DCDCDC"
    padding = "5px"
    style = "border:1px solid %s; padding: %s" % (grid_color, padding)
    templ = Template("""
<table class="{{ tb_class }}" style="background-color: {{ back_color}}; {{ style }}">
    {% for item in header %}
    <th style="{{ style }}">{{ item }}</th>
    {% endfor %}
    {% for row in rows %}
        <tr>
        {% for item in row %}
            <td style="vertical-align:top; {{ style }}">{{ item }}</td>
        {% endfor %}
        </tr>
    {% endfor %}
</table>
    """)
    return templ.render(locals())


def get_git_info():
    """
    Get the abbreviated commit version (not provided by get_git_info())
    Returns a dictionary
    """
    COMMANDS = {
        'short_commit' : ['git', 'rev-parse', '--short', 'HEAD'],
        'commit' : ['git', 'rev-parse', 'HEAD'],
        'author': ['git', 'log', '-1', "--pretty=format:%an"],
        'tag' : ['git', 'describe', '--tags'],
        'date' : ['git', '--no-pager', 'log', '-1', '--format=%ai'],
        'message' : ['git', 'log', '-1', "--pretty=%B"],
        'raw' : ['git', 'log', '-1'],
        }
    try:
        r = {}
        for var, command in COMMANDS.items():
            r[var] = subprocess.check_output(command, 
                                            text=True).strip()
        # keep first part
        r['tag'] = r['tag'].split('-')[0]
        return r
    except subprocess.CalledProcessError:
        # no git repository
        return {}

def python_version():
    "Get the python version"
    try:
        return sys.version.split('(')[0].rstrip()
    except (AttributeError, IndexError) as e:
        return str(e)

def system_name():
    "Get the system name"
    r = platform.system()
    if not r:
        # you never know
        return "<UNKNOWN>"
    # print("Found:", r)
    CONV = {'Win': 'Windows', 'Darwin':'MacOs'}
    return CONV.get(r, r)
    

def system_version():
    "Get the system version"
    try:
        return platform.mac_ver()[0] or platform.release()
    except (AttributeError, IndexError) as e:
        return str(e)

# for the navigation
from mkdocs.structure.files import File
from mkdocs.structure.nav import get_navigation
class Files(object):
    "This helper class is needed to rebuild the navigation"
    def __init__(self, config):
        self.config = config
        self._filenames = []

    @property
    def filenames(self):
        "The list of filenames (not used at the moment"
        return self._filenames

    def get_file_from_path(self, path):
        "Build the filenames"
        self._filenames.append(path)
        file = File(os.path.basename(path), 
                    os.path.dirname(path),
                    os.path.dirname(path), True)
        return file

    def documentation_pages(self):
        return []


# ---------------------------------
# Exports to the environment
# ---------------------------------

def define_env(env):
    """
    This is the hook for declaring variables, macros and filters
    """

    # Get data:
    try:
        system = {
            'system': system_name(),
            'system_version': system_version(),
            'python_version': python_version(),
            'mkdocs_version': mkdocs.__version__,
            'macros_plugin_version': 
                    pkg_resources.get_distribution(PACKAGE_NAME).version,
            'jinja2_version': jinja2.__version__,
            # 'site_git_version': site_git_version(),
        }
    except Exception as e:
        # Avoid breaking the system if error in reading the system info:
        system = ("<i><b>Cannot read system info!</b> %s: %s</i>" % 
                    (type(e).__name__, str(e)))
    env.variables['environment'] = system



    # git information:
    env.variables['git'] = get_git_info()

    def render_file(filename):
        """
        Render an external page (filename) containing jinj2 code
        Do not declare as macro, as this is pointless.
        """
        SOURCE_FILE = os.path.join(SOURCE_DIR, filename)
        with open(SOURCE_FILE) as f:
            s = f.read()
        # now we need to render the jinja2 directives:
        return env.render(s)

    @env.macro
    def context(obj=env.variables):
        "*Default mkdocs_macro* List the defined variables"
        try:
            return [(var, type(value).__name__, format_value(value))
                        for var, value in list_items(obj)]
        except jinja2.exceptions.UndefinedError as e:
            return [("<i>Error!</i>", type(e).__name__, str(e))]
        except AttributeError:
            # Not an object or dictionary (int, str, etc.)
            return [(obj, type(obj).__name__, repr(obj))]

    @env.filter
    def pretty(var_list):
        """ *Default mkdocs_macro* Prettify a dictionary or object 
        (used for environment documentation, or debugging)"""
        if not var_list:
            return ''
        else:
            rows = [("<b>%s</b>" % var, "<i>%s</i>" % var_type, 
                    content.replace('\n', '<br/>'))
                    for var, var_type, content in var_list]
            header = ['Variable','Type', 'Content']
            return make_html(rows, header)

    @env.macro
    def macros_info():
        """
        Test/debug function:
        list useful documentation on the mkdocs_macro environment.
        """
        return render_file('macros_info.md')

    @env.macro
    def now():
        """
        Get the current time (returns a datetime object). 
        Used alone, it provides a timestamp.
        To get the year use `now().year`, for the month number 
        `now().month`, etc.
        """
        return datetime.datetime.now()
