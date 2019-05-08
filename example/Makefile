#Makes the example files. If you want matrix.py to generate a new random letter-cascade, use make -B. 

array.tex :
	python3 ../src/matrix.py > array.tex

matrix.pdf : array.tex matrix.tex
	lualatex matrix.tex
