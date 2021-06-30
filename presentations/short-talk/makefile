SOURCES := slides.tex images/backend-api.tex images/api.tex images/strong.tex images/weak.tex images/transistors.tex images/frequency.tex images/fp-performance.tex

LATEXMK := latexmk -e '$$clean_ext=q/snm/; $$clean_full_ext=q/nav/' -pdf -pdflatex='pdflatex --interaction=nonstopmode' -use-make
LUALATEXMK := latexmk -e '$$clean_ext=q/snm/; $$clean_full_ext=q/nav/' -pdf -pdflatex='lualatex --interaction=nonstopmode' -use-make

all: slides.pdf api.pdf backend-api.pdf strong.pdf weak.pdf transistors.pdf frequency.pdf fp-performance.pdf

slides.pdf: slides.tex api.pdf backend-api.pdf strong.pdf weak.pdf transistors.pdf frequency.pdf fp-performance.pdf beamerthemeCSCS.sty $(wildcard logos/*) $(wildcard cscs_images/*)
	$(LATEXMK) $<

api.pdf: images/api.tex
	$(LATEXMK) $<

backend-api.pdf: images/backend-api.tex
	$(LATEXMK) $<

strong.pdf: images/strong.tex
	$(LATEXMK) $<

weak.pdf: images/weak.tex
	$(LATEXMK) $<

transistors.pdf: images/transistors.tex images/transistors-cpu.tbl
	$(LATEXMK) $<

frequency.pdf: images/frequency.tex images/frequency.tbl
	$(LATEXMK) $<

fp-performance.pdf: images/fp-performance.tex images/preshing-spec-fp.tbl images/specfp-loess.tbl
	$(LUALATEXMK) $<

clean:
	for s in $(SOURCES); do $(LATEXMK) -c "$$s"; done

realclean:
	for s in $(SOURCES); do $(LATEXMK) -C "$$s"; done
