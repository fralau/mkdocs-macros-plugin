---
unit_price: 8
---

# With altered syntax

> **Square brackets instead of curly brackets**.

[# This is a jinja2 comment that will not appear. #]

It costs [[ unit_price ]] EUR.

[[% if unit_price > 10 %]]
**Ouch, this is expensive!**
[[% else %]]
_Yay, this is cheap._
[[% endif %]]
