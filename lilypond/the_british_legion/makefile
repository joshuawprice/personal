piece := TheBritishLegion

LILY_CMD := lilypond -dno-point-and-click

.DEFAULT_GOAL := parts

PDFDIR := PDFs
MIDIDIR := MIDI

# Input and output files are searched in the directories listed in
# the VPATH variable.
VPATH := Parts \
         $(PDFDIR) \
         $(MIDIDIR)

%.pdf %.midi : %.ly | $(PDFDIR) $(MIDIDIR)
	$(LILY_CMD) $<
	mv "$*.pdf" $(PDFDIR)/
	mv "$*.midi" $(MIDIDIR)/




$(PDFDIR):
	-mkdir $(PDFDIR)

$(MIDIDIR):
	-mkdir $(MIDIDIR)


common := Globals.ily

# TODO: If at all possible, try to remove $(piece) from everything but finala output PDF/MIDI.
# TODO: Make this also recompile if the midi is missing.
$(piece)-CornetOne.pdf: $(piece)-CornetOne.ly $(common)
$(piece)-CornetSolo.pdf: $(piece)-CornetSolo.ly $(common)
$(piece)-HornSolo.pdf: $(piece)-HornSolo.ly $(common)


.PHONY: parts
parts: \
  $(piece)-CornetOne.pdf \
  $(piece)-CornetSolo.pdf \
  $(piece)-HornSolo.pdf


.PHONY: clean
clean:
	-rm -r $(PDFDIR) $(MIDIDIR)
