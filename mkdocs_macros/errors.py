import textwrap
import traceback
from functools import singledispatch

from jinja2 import TemplateSyntaxError
from mkdocs.structure.pages import Page


@singledispatch
def format_error(error: Exception, markdown: str, page: Page) -> str:
    """Default error message for a generic exception."""
    error_type = type(error).__name__
    return textwrap.dedent(
        f'''
        # _Macro Rendering Error_

        _File_: `{page.file.src_path}`
        
        _{error_type}_: {error}
        
        ```
        %s
        ```
        ''',
    ).strip() % traceback.format_exc()


@format_error.register
def _format_template_syntax_error(
    error: TemplateSyntaxError,
    markdown: str,
    page: Page,
) -> str:
    """Template rendering failed."""
    line = markdown.splitlines()[error.lineno - 1]
    return textwrap.dedent(
        f'''
        # _Macro Syntax Error_

        _File_: `{page.file.src_path}`
        
        _Line {error.lineno} in Markdown file:_ **{error.message}**
        ```markdown
        {line}
        ``` 
        '''
    ).strip()
