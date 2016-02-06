from optparse import OptionParser
import sys

filename = sys.argv[1]

varParser = OptionParser()

f = open(filename,"r")
string = f.read()
print(string)
