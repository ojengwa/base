.PHONY: all

DIRTY_FILES=$$(git status --porcelain --untracked-files=all | awk '{$$1=""}1')
COMPOSE:=docker-compose


help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}';

clean: ## Deletes unneded files (*.pyc, *.DS_Store, etc.)
	find . -name "*.pyc" -exec rm -f {} \;
	find . -name "*.DS_Store" -exec rm -f {} \;


submodules:
	git submodule init;
	git submodule update;

validate:
	bash ./bin/get_static_validation.sh;

analysis:
	@echo "----- Running frontend static analysis -----";;
	bash ./bin/static_validate_frontend.sh;
	@echo "--------------------------------------------";
	@echo "----- Running backend static analysis -----";
	bash ./bin/static_validate_backend.sh;
	@echo "--------------------------------------------";


test:
	@echo "----- Running frontend tests -----";
	bash ./bin/test_local_frontend.sh;
	@echo "----------------------------------";
	@echo "----- Running frontend tests -----";
	bash ./bin/test_local_backend.sh;
	@echo "----------------------------------";


pip-compile: ## Creates new pip requirement files, add  --generate-hashes
	@echo "\033[92mCreating new requirement-files from *.in-Files...\033[0m";
	pip-compile --output-file requirements.txt requirements.in;
	@echo "\nYou can use 'make pip-update' to update the requirements and 'make pip-install to install the requirments locally";

pip-update: ## Updates the pip requirements, add  --generate-hashes
	@echo "\033[92mUpdating all pip requirements...\033[0m";
	pip-compile -U --output-file requirements.txt requirements.in;


# Atomic commits : https://www.reddit.com/r/programming/comments/7i5424/atomic_commits_telling_stories_with_git
commit: clean
	@for path in $(DIRTY_FILES); do \
		git add $$path; \
		git commit -sm "commit changes to $$path" --no-verify; \
	done; \
	git push;
