upload: build
	PATH=$PATH:/home/dex/.local/share/gem/ruby/3.0.0/bin neocities push generated_files 

build: 
	python create_website.py > generated_files/index.html
	python create_website.py -g > generated_files/index-secret-for-gm.html
	tidy -w 160 -i -q --tidy-mark=no -m generated_files/index.html generated_files/index-secret-for-gm.html 2>/dev/null || exit 0

stats: 
	PATH=$PATH:/home/dex/.local/share/gem/ruby/3.0.0/bin neocities info sr-w-domu
