# configurable-static-code-rain
I needed to create a vector graphic static code-rain of math symbols with a custom color gradient and there wasn't anything out there, so here goes.

I used Latex for the symbols, easy input of an array environment and color configuration with the xcolor package. The parameterization for the output is done in the source code itself, which is a bit lazy but that could be fixed. Also you need to experiment with row/column numbers if you are planning to use a format other than A4, I got my numbers by guessing and checking.

`lualatex` is not required as a TeX driver so feel free to change that in the `Makefile`.
