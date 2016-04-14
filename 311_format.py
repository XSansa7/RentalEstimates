import sys
for line in sys.stdin:
	line = line.strip()
	cols = line.split(",")
	realcols = []
	instr = False
	for col in cols:
		if not instr:
			if col.startswith('"'):
				if col.endswith('"'):
					realcols.append(col[1:-1])
				else:
					instr = True
					mystr = col
			else:
				realcols.append(col)
		else:
			if col.endswith('"'):
				realcols.append((mystr + col)[1:-1])
				instr = False
			else:
				mystr += "," + col
	print "\t".join(realcols)