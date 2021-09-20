LTX=pdflatex -shell-escape
SRC=main.tex
BIB=biber

all: main.pdf

main.pdf: $(SRC) references.bib
	$(LTX) $(SRC)
	$(BIB) $(SRC:tex=bcf)
	$(LTX) $(SRC)
	$(LTX) $(SRC)

# src/arbor.pdf: src/model.py src/cell.swc src/fit.json src/nrn.csv src/utils.py
# 	cd src; python3.8 model.py

.PHONY: clean
clean:
	-rm -f *.log *.snm *.out *.nav *.toc *.aux *.bbl *.bcf *.blg *.vrb
