#!/usr/bin/env python
import sys
import csv

from popseq_io import readMutationData, readScaffoldData

def main():
    scaffoldData, homHetRatios = readScaffoldData(sys.argv[1], delimiter=',')

    # print each row with data in scaffoldData
    print '\t'.join(['Marker', 'Chr', 'Start', 'End', 'Pheno', 'Color'])
    for chrBin, row in readMutationData(sys.argv[2], scaffoldData, delimiter=','):
        out = [row[0], chrBin[0], chrBin[1], chrBin[1], row[7], 2 if row[7] == 'het' else 1]
        print '\t'.join(map(str, out))
    pass

if __name__ == '__main__': main()
