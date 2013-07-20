all: gendocs upload uploadexamples

gendocs:
	python gendocs.py
	rsync --delete -rlvz api pyj.be:/var/www/pyj.be/htdocs/

upload:
	cp -aux pyjs_site/output/* .
	rsync --exclude=pygit --exclude=examples --exclude=api --exclude=wiki \
          --delete -rlvz * pyj.be:/var/www/pyj.be/htdocs/

uploadexamples:
	rsync -rlvz ../examples pyj.be:/var/www/pyj.be/htdocs/

# use this to _just_ upload the web site, not everything else
uploadsitehtml:
	cp -aux pyjs_site/public/* .
	rsync -rlvz pyjs_site/public/* pyj.be:/var/www/pyj.be/htdocs/

