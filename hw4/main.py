import sys

import truss

try:
    a = truss.Truss(sys.argv[1], sys.argv[2])
    a.PlotGeometry()
except RuntimeError as e:
    print('ERROR: {}'.format(e))
    sys.exit(2)