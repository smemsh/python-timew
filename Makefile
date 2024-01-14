#

LIB := timew
PYBASE := python3.9
VERSION := 0.1.0

REQIN = requirements.in
REQOUT = requirements.txt
REQDEVIN = requirements-dev.in
REQDEVOUT = requirements-dev.txt
REQINFILES := $(REQIN) $(REQDEVIN)
REQOUTFILES := $(REQOUT) $(REQDEVOUT)

WHEEL := dist/timew-$(VERSION)-py3-none-any.whl
SDIST := dist/timew-$(VERSION).tar.gz

SYNCFILE := venv/.pip-synced
PYTHONEXE := venv/bin/python3
PIPTOOLEXE := venv/bin/pip-compile

export PATH := $(HOME)/bin:$(CURDIR)/venv/bin:/usr/local/bin:/bin:/usr/bin

dist: $(WHEEL) $(SDIST)

test: venv $(SDIST) $(WHEEL)
	pytest

wheel $(WHEEL): $(SDIST)
	$(PYBASE) -m build --no-isolation --wheel

sdist $(SDIST): pyproject.toml venv $(REQOUT) $(REQDEVOUT) $(SYNCFILE)
	$(PYBASE) -m build --no-isolation --sdist

venv: $(PYTHONEXE) $(PIPTOOLEXE)

$(PYTHONEXE):
	$(PYBASE) -m venv --symlinks venv

sync $(SYNCFILE): venv $(REQOUTFILES)
	pip-sync -q $(REQOUTFILES)
	@# might not have changed so avoid rebuild every time
	touch $(SYNCFILE)

pkgup $(PIPTOOLEXE):
	pip3 install -q -U pip wheel setuptools pip-tools

reqs $(REQOUT): $(REQIN)
	pip-compile -q --no-strip-extras $(REQIN)

devreqs $(REQDEVOUT): $(REQDEVIN)
	pip-compile -q --no-strip-extras -o $(REQDEVOUT) $(REQINFILES)

clean:
	rm -rf build venv dist $(LIB).egg-info

rebuild: clean sdist wheel

.PHONY: wheel sdist test sync pkgup reqs devreqs clean rebuild
