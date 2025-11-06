# TODO:
#   - Can I build using `make cornetone` (using default rule)?

piece = TheBritishLegion

LILYFLAGS = -dno-point-and-click

sources = $(patsubst Parts/%,%,$(wildcard Parts/*.ly))

.PHONY: parts
parts: $(sources:%.ly=out/$(piece)-%.pdf)

out:; mkdir out

out/$(piece)-%.pdf out/$(piece)-%.midi: Parts/%.ly Globals.ily | out
	lilypond $(LILYFLAGS) -o $(basename $@) $<

.PHONY: clean
clean:
	rm -r out/
