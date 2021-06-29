SOURCES := slides.tex

LATEXMK := latexmk -e '$$clean_ext=q/snm/; $$clean_full_ext=q/nav/' -pdf -pdflatex='pdflatex --interaction=nonstopmode' -use-make
XELATEXMK := latexmk -e '$$clean_ext=q/snm/; $$clean_full_ext=q/nav/' -lualatex -use-make

all: slides.pdf

slides.pdf: slides.tex beamerthemeCSCS.sty $(wildcard logos/*) $(wildcard cscs_images/*)
	$(LATEXMK) $<

clean:
	for s in $(SOURCES); do $(LATEXMK) -c "$$s"; done
	rm -f *.nav
	rm -f slides.pdf

realclean:
	for s in $(SOURCES); do $(LATEXMK) -C "$$s"; done
