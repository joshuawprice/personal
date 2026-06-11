piece := TheBritishLegion

LILYFLAGS := -dno-point-and-click
MAKEFLAGS += -j$(shell nproc)

sources := $(wildcard parts/*.ly)

.PHONY: parts
parts: $(sources:parts/%.ly=out/$(piece)-%.pdf)

out:; mkdir -p out

out/$(piece)-%.pdf out/$(piece)-%.midi: parts/%.ly globals.ily | out
	lilypond $(LILYFLAGS) -o $(basename $@) $<

%: out/$(piece)-%.pdf ;

.PHONY: clean
clean:
	rm -rf out/
