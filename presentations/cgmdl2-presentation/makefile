SOURCES := cgmdl2-slides.tex 

XELATEXMK := latexmk -e '$$clean_ext=q/snm/; $$clean_full_ext=q/nav/' -lualatex -use-make

all: cgmdl2-slides.pdf

cgmdl2-slides.pdf: cgmdl2-slides.tex beamerthemeCSCS.sty $(wildcard logos/*) $(wildcard cscs_images/*)
	$(XELATEXMK) $<

clean:
	for s in $(SOURCES); do $(XELATEXMK) -c "$$s"; done

realclean:
	for s in $(SOURCES); do $(XELATEXMK) -C "$$s"; done
