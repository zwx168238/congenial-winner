#!/bin/bash -x

current_path=$(dirname $0)
source ${current_path}/env.properties

first_init_setup()
{
	cd ${CUSTOM_MIRROR_PATH}
	if [ ! -e .repo ]; then
		${CUSTOM_CODE_URL} --mirror
	fi
	#GET CODE
	repo sync -c
}

create_permissions_project()
{
	ssh -p ${MAIN_GERRIT_SSH_PORT} ${MAIN_GERRIT_USER}@${MAIN_GERRIT_HOST} -p All-Projects  -n ${PROJECT_PREFIX} --empty-commit --permissions-only
}

get_latest_pro_list()
{
	repo list -n|tee project.list
}

create_project_on_ts_gerrit()
{
	create_permissions_project
	for i in `cat project.list`;do ssh -p ${MAIN_GERRIT_SSH_PORT} ${MAIN_GERRIT_USER}@${MAIN_GERRIT_HOST} gerrit create-project -p ${PROJECT_PREFIX} ${PROJECT_PREFIX}/$i --empty-commit;done
}

add_remote()
{
	repo forall -c "git remote add njts ssh://${MAIN_GERRIT_USER}@${MAIN_GERRIT_HOST}:${MAIN_GERRIT_SSH_PORT}/${PROJECT_PREFIX}/$REPO_PROJECT"
}

execute_push()
{
	repo forall -c "git push njts HEAD:refs/heads/${PROJECT_BRANCH}"
}

align_mirror()
{
	for l in $(cat project.list) ;do
  	cd ${l}.git
  	remote_tmp=$(git remote|grep -w "njts")
  	if [ -z ${remote_tmp} ]; then
    	ssh -p ${MAIN_GERRIT_SSH_PORT} ${MAIN_GERRIT_USER}@${MAIN_GERRIT_HOST}  gerrit create-project -p ${PROJECT_PREFIX}  ${line} --empty-commit
    	git remote add njts ssh://${MAIN_GERRIT_USER}@${MAIN_GERRIT_HOST}:${MAIN_GERRIT_SSH_PORT}/${l}.git
  	fi
  	git push -u njts HEAD:refs/heads/car-release-master-oneplane
  	cd ${CUSTOM_MIRROR_PATH}
	done
}

generate_default_manifest_repo()
{
	python rebase_help.py -i $1 -o default.xml -u $2 -p $3
}

creaye_manifest_repo()
{
	ssh -p ${MAIN_GERRIT_SSH_PORT} ${MAIN_GERRIT_USER}@${MAIN_GERRIT_HOST} gerrit create-project -p ${PROJECT_PREFIX} ${TARGET_MANIFEST_GIT} --empty-commit
}

get_manifest_and_commit()
{
	creaye_manifest_repo
	git clone ${MANIFEST_URL}  ${MANIFEST_PATH}
	cd ${${MANIFEST_PATH}}
	generate_default_manifest_repo .repo/manifest.xml ${MAIN_GERRIT_HTTP_URL} ${PROJECT_PREFIX}
	git add -A .
	git commit -a -s -m "init commit"
	git push origin HEAD:refs/heads/${PROJECT_BRANCH}
}

do_print()
{
	echo "$*"
}

main()
{
	do_print "now try to init mirror from custom"
	first_init_setup
	get_latest_pro_list
	add_remote
	do_print "now try to init mirror for ts"
	create_project_on_ts_gerrit
	execute_push
	get_manifest_and_commit
	do_print "all done"
}
