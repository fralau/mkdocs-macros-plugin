import os

def define_env(env):

    # test predefined macro
    fix_url = env.variables.fix_url
    fix_url2 = env.macros.fix_url

    @env.macro
    def button(label, url):
        "Add a button"
        url = fix_url(url)
        HTML = """<a class='button' href="%s">%s</a>"""
        return HTML % (url, label)

    @env.macro
    def button2(label, url):
        "Add a button"
        url = fix_url2(url)
        HTML = """<a class='button' href="%s">%s</a>"""
        return HTML % (url, label)

