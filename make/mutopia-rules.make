

$(outdir)/%.gif: $(outdir)/%.ps
	sh $(PS_TO_GIFS) $<
	-mv $(name-stem)-page*.gif $(outdir)/
	ln -s $(name-stem)-page1.gif $@

$(outdir)/%.png: $(outdir)/%.ps
	sh $(PS_TO_PNGS) $<
	-mv $(name-stem)-page*.png $(outdir)/
	ln -s $(name-stem)-page1.png $@

$(outdir)/%.ly.txt: %.ly
	ln -f $< $@

$(outdir)/%.ly.txt: $(outdir)/%.ly
	cp -f $< $@

$(outdir)/%.ly.txt: %.abc
#which file to show here -- abc seems more cute?
	ln -f $< $@

$(outdir)/%.ly: %.abc
	$(PYTHON) $(ABC2LY) --strict -o $@ $< 

$(outdir)/%.dvi: $(outdir)/%.ly
	$(PYTHON) $(LY2DVI) --output=$@ --dependencies $< 

# don't junk intermediate .dvi files.  They're easier to view than
# .ps or .png
.PRECIOUS: $(outdir)/%.dvi

$(outdir)/%.dvi: %.ly
	$(PYTHON) $(LY2DVI) --output=$@ --dependencies $< 

$(outdir)-$(PAPERSIZE)/%.dvi: %.ly
	$(PYTHON) $(LY2DVI) --output=$@ --dependencies --set=papersize=$(PAPERSIZE) $< 


