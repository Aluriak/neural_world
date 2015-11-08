IMAGE_VIEWER=feh

remold:
	./delete_old_archives.sh

clearall:
	rm -r ./sim_*

shown: remold
	$(IMAGE_VIEWER) sim_*/archive*cln.png

showg: remold
	$(IMAGE_VIEWER) sim_*/tree.png
