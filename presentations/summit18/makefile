TEXFILES=*.tex

poster.pdf : $(TEXFILES) api.pdf images/*.tex images/*.tbl baposter.cls pyarb-example.py
	pdflatex --shell-escape poster.tex

api.pdf : images/api.tex
	pdflatex --shell-escape images/api.tex

force : poster.pdf
	pdflatex --shell-escape poster

open : poster.pdf
	open poster.pdf

clean:
	rm -f poster.pdf
	rm -f api.pdf
	rm -f *.aux
	rm -f *.log
	rm -f *.toc
	rm -f *.out

