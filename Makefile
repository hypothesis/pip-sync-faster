comma := ,

.PHONY: help
help = help::; @echo $$$$(tput bold)$(strip $(1)):$$$$(tput sgr0) $(strip $(2))
$(call help,make help,print this help message)

.PHONY: services

.PHONY: devdata

.PHONY: shell
$(call help,make shell,"launch a Python shell in this project's virtualenv")
shell: python
	@pyenv exec tox -qe dev

.PHONY: lint
$(call help,make lint,"lint the code and print any warnings")
lint: python
	@pyenv exec tox -qe lint

.PHONY: typecheck
$(call help,make typecheck,"type check the code and print any warnings")
typecheck: python
	@pyenv exec tox -qe typecheck

.PHONY: format
$(call help,make format,"format the code")
format: python
	@pyenv exec tox -qe format

.PHONY: checkformatting
$(call help,make checkformatting,"crash if the code isn't correctly formatted")
checkformatting: python
	@pyenv exec tox -qe checkformatting

.PHONY: test
$(call help,make test,"run the unit tests in Python 3.12")
test: python
	@pyenv exec tox -qe tests

.PHONY: test-py311
$(call help,make test-py311,"run the unit tests in Python 3.11")
test-py311: python
	@pyenv exec tox -qe py311-tests

.PHONY: test-py310
$(call help,make test-py310,"run the unit tests in Python 3.10")
test-py310: python
	@pyenv exec tox -qe py310-tests

.PHONY: test-py39
$(call help,make test-py39,"run the unit tests in Python 3.9")
test-py39: python
	@pyenv exec tox -qe py39-tests

.PHONY: coverage
$(call help,make coverage,"run the tests and print the coverage report")
coverage: python
	@pyenv exec tox --parallel -qe 'tests,py{311,310,39}-tests,coverage'

.PHONY: functests
$(call help,make functests,"run the functional tests in Python 3.12")
functests: python
	@pyenv exec tox -qe functests

.PHONY: functests-py311
$(call help,make functests-py311,"run the functional tests in Python 3.11")
functests-py311: python
	@pyenv exec tox -qe py311-functests

.PHONY: functests-py310
$(call help,make functests-py310,"run the functional tests in Python 3.10")
functests-py310: python
	@pyenv exec tox -qe py310-functests

.PHONY: functests-py39
$(call help,make functests-py39,"run the functional tests in Python 3.9")
functests-py39: python
	@pyenv exec tox -qe py39-functests

.PHONY: sure
$(call help,make sure,"make sure that the formatting$(comma) linting and tests all pass")
sure: python
sure:
	@pyenv exec tox --parallel -qe 'checkformatting,lint,typecheck,tests,py{311,310,39}-tests,coverage,functests,py{311,310,39}-functests'

.PHONY: template
$(call help,make template,"update from the latest cookiecutter template")
template: python
	@pyenv exec tox -e template -- $$(if [ -n "$${template+x}" ]; then echo "--template $$template"; fi) $$(if [ -n "$${checkout+x}" ]; then echo "--checkout $$checkout"; fi) $$(if [ -n "$${directory+x}" ]; then echo "--directory $$directory"; fi)

.PHONY: clean
$(call help,make clean,"delete temporary files etc")
clean:
	@rm -rf build dist .tox .coverage coverage .eslintcache node_modules supervisord.log supervisord.pid yarn-error.log
	@find . -path '*/__pycache__*' -delete
	@find . -path '*.egg-info*' -delete

.PHONY: python
python:
	@bin/make_python

-include pip_sync_faster.mk
