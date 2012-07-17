python-termstyle
============

A small python module for styling terminal output
using natural descriptions of the style.

Examples
--------------
```python
from termstyle import termstyle

message = "I am stylish."

# blue
print termstyle.blue(message)

# underlined
print termstyle.underlined(message)

# blinking with a magenta background
print termstyle.blinking.on.magenta(message)

# yellow on white text, bold and dark
print termstyle.yellow.on.white.bold.dark(message)
```

Every termstyle object is immutable and can be stored:

```python
# save error styling
error = termstyle.red.bold

# red and bold
print error("I'm an error!")

# red and bold and blinking
print error.blinking("I'm a really bad error!")
```


Available text colors and backgrounds
---------------------
 - grey
 - red
 - green
 - yellow
 - blue
 - magenta
 - cyan
 - white


Available attributes
--------------------
 - bold
 - dark
 - underlined
 - blinking
 - reversed
 - concealed

Not all attributes are available on all terminals:
```
============ ======= ==== ========== ========== ======= =========
Terminal     bold    dark underlined blink      reverse concealed
------------ ------- ---- ---------- ---------- ------- ---------
xterm        yes     no   yes        bold       yes     yes
linux        yes     yes  bold       yes        yes     no
rxvt         yes     no   yes        bold/black yes     no
dtterm       yes     yes  yes        reverse    yes     yes
teraterm     reverse no   yes        rev/red    yes     no
aixterm      normal  no   yes        no         yes     yes
PuTTY        color   no   yes        no         yes     no
Windows      no      no   no         no         yes     no
Cygwin SSH   yes     no   color      color      color   yes
Mac Terminal yes     no   yes        yes        yes     yes
============ ======= ==== ========== ========== ======= =========
```

Testing
-------------------
Testing is best conducted by sight, run the module
and it will attempt to print the styles that it can.
