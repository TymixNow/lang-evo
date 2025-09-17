from manual import run

links = open(input("input links' file name> "), "r").read().split("\n")[0:5]
run(*links)
