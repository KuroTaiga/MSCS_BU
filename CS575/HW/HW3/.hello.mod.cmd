savedcmd_/home/jdong/CS575/HW3/hello.mod := printf '%s\n'   hello.o | awk '!x[$$0]++ { print("/home/jdong/CS575/HW3/"$$0) }' > /home/jdong/CS575/HW3/hello.mod
