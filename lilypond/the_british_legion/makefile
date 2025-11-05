# TODO:
#   - Remove "TheBritishLegion" from .ly files but keep in output
#   - Make generic
#     - Have piece name var

LILYFLAGS = -dno-point-and-click

sources = $(patsubst Parts/%,%,$(wildcard Parts/*.ly))

.PHONY: parts
parts: $(sources:%.ly=out/%.pdf)

out:; mkdir out

out/%.pdf out/%.midi: Parts/%.ly Globals.ily | out
	lilypond $(LILYFLAGS) -o out/ $<

.PHONY: clean
clean:
	rm -r out/
