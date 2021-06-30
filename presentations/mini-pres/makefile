SOURCES := slides.tex images/backend-api.tex images/api.tex images/strong.tex images/weak.tex images/transistors.tex images/frequency.tex images/fp-performance.tex

LATEXMK := latexmk -e '$$clean_ext=q/snm/; $$clean_full_ext=q/nav/' -pdf -pdflatex='pdflatex --interaction=nonstopmode' -use-make
LUALATEXMK := latexmk -e '$$clean_ext=q/snm/; $$clean_full_ext=q/nav/' -pdf -pdflatex='lualatex --interaction=nonstopmode' -use-make

all: slides.pdf

slides.pdf: slides.tex cajal.pdf beamerthemeCSCS.sty
	$(LATEXMK) $<

clean:
	for s in $(SOURCES); do $(LATEXMK) -c "$$s"; done

realclean:
	for s in $(SOURCES); do $(LATEXMK) -C "$$s"; done
