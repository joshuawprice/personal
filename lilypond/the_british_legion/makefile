piece = TheBritishLegion

LILYFLAGS = -dno-point-and-click
MAKEFLAGS += -j$(shell nproc)

sources = $(patsubst parts/%,%,$(wildcard parts/*.ly))

.PHONY: parts
parts: $(sources:%.ly=out/$(piece)-%.pdf)

out:; mkdir out

out/$(piece)-%.pdf out/$(piece)-%.midi: parts/%.ly Globals.ily | out
	lilypond $(LILYFLAGS) -o $(basename $@) $<

.SECONDEXPANSION:
$(sources:.ly=): out/$(piece)-$$@.pdf

.PHONY: clean
clean:
	rm -r out/
