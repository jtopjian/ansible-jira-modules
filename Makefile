CURDIR := $(shell pwd)
TEST_PATH := $(CURDIR)/test/acceptance

ANSIBLE_CMD := ansible-playbook -vvv

check-auth:
ifndef JIRA_URL
	$(error JIRA_URL is not defined)
endif
ifndef JIRA_USERNAME
	$(error JIRA_USERNAME is not defined)
endif
ifndef JIRA_PASSWORD
	$(error JIRA_PASSWORD is not defined)
endif

check-test:
ifndef TEST
	$(error TEST is not defined)
endif

testacc: check-auth check-test
	@cd $(TEST_PATH) ; \
	$(ANSIBLE_CMD) $(TEST).yml

testacc-all: check-auth
	@cd $(TEST_PATH) ; \
	for i in *.yml; do \
	  echo "\n\nRunning: $$i\n\n" ; \
		$(ANSIBLE_CMD) $$i ; \
		if [ $$? != 0 ]; then \
			exit 1 ; \
		fi ; \
	done
