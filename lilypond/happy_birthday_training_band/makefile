piece := happy-birthday

LILYFLAGS := -dno-point-and-click
MAKEFLAGS += -j$(shell nproc)

sources := $(wildcard parts/*.ly)

.PHONY: parts
parts: $(sources:parts/%.ly=out/$(piece)_%.pdf)

out:; mkdir -p out

out/$(piece)_score.pdf out/$(piece)_score.midi &: parts/score.ly parts/*.ily | out
	lilypond $(LILYFLAGS) -o $(basename $@) $<

out/$(piece)_%.pdf out/$(piece)_%.midi: parts/%.ly parts/%.ily parts/defs.ily | out
	lilypond $(LILYFLAGS) -o $(basename $@) $<

%: out/$(piece)_%.pdf ;

.PHONY: clean
clean:
	rm -rf out/
