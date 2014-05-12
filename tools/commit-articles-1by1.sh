#!/bin/bash
# @author: mawenbao@hotmail.com
# @date: 2014-05-12
# @desc: find all the modified files in content/ directory
#        and commit them one at a tim

COMMIT_MSG="update article"
MODIFIED_FILES=`git reset >/dev/null && git ls-files -m | grep '^content' | grep -E '(md|rst)$'`

for f in ${MODIFIED_FILES}; do
    git add ${f}
    git commit -m "${COMMIT_MSG}"
done

