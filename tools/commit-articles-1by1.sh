#!/bin/bash
# @author: mawenbao@hotmail.com
# @date: 2014-05-12
# @desc: find all the untracked/modified files
#        in content/ directory and commit them one at a time

COMMIT_MSG="update article"

function filter_articles() {
    echo `echo $1 | grep '^content' | grep -E '(md|rst)$'`
}

git reset > /dev/null

MODIFIED_FILES=`filter_articles $(git ls-files -m)`
UNTRACKED_FILES=`filter_articles $(git ls-files -o --exclude-standard)`

for f in ${MODIFIED_FILES} ${UNTRACKED_FILES}; do
    git add ${f}
    git commit -m "${COMMIT_MSG}"
done

