SOURCES := braincomp2017-slides.tex images/transistors.tex images/frequency.tex images/fp-performance.tex

XELATEXMK := latexmk -e '$$clean_ext=q/snm/; $$clean_full_ext=q/nav/' -xelatex -use-make

all: braincomp2017-slides.pdf transistors.pdf frequency.pdf fp-performance.pdf

braincomp2017-slides.pdf: braincomp2017-slides.tex network-weak.pdf transistors.pdf frequency.pdf fp-performance.pdf beamerthemeCSCS.sty $(wildcard logos/*) $(wildcard cscs_images/*)
	$(XELATEXMK) $<


network-weak.pdf: images/network-weak.tex images/network-weak.tbl
	$(XELATEXMK) $<

transistors.pdf: images/transistors.tex images/transistors-cpu.tbl
	$(XELATEXMK) $<

frequency.pdf: images/frequency.tex images/frequency.tbl
	$(XELATEXMK) $<

fp-performance.pdf: images/fp-performance.tex images/preshing-spec-fp.tbl images/specfp-loess.tbl
	$(XELATEXMK) $<

clean:
	for s in $(SOURCES); do $(XELATEXMK) -c "$$s"; done

realclean:
	for s in $(SOURCES); do $(XELATEXMK) -C "$$s"; done
