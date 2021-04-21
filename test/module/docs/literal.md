---
# YAML header
ignore_macros: true
---


# In this document, macros are ignored (`ignore_macros: true`)

## Some pre-existing directive (not Jinja2)

`{% Vimeo ID}`


## Offending LaTeX

```LaTeX
\begin{tabular}{|ccc|}
    \hline
    2   & 9     & 4\\
    7   & \multicolumn{2}{c|} {\multirow{2}*{{?}}} \\
    6   &       &\\
    \hline
\end{tabular}
```