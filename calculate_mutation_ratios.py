#!/usr/bin/env python
import sys
import csv

from popseq_io import readMutationData, readScaffoldData

def processMutationData(fn, scaffoldData, homHetRatios, delimiter=' '):
    """
    Counts the number of hom/het mutations per bin, and
    calculates het/hom ratio. The hom/het counts are stored in another dictonary per bin
    such that we can directly count the number of occurrences of "het" and "hom".
    """
    for chrBin, row in readMutationData(fn, scaffoldData, delimiter=delimiter):
        homHetRatios[chrBin][row[7]] += 1

    # Finished reading data, now calculate ratios.
    for chrBin in homHetRatios:
        if homHetRatios[chrBin]['hom'] > 0:
            homHetRatios[chrBin]['ratio'] = homHetRatios[chrBin]['het'] / homHetRatios[chrBin]['hom']
        else:
            # if hom-count is zero, no ratio can be calculated
            homHetRatios[chrBin]['ratio'] = 'NA'
        # convert dictionaries to lists [hom, het, ratio]
        homHetRatios[chrBin] = [homHetRatios[chrBin]['hom'], homHetRatios[chrBin]['het'], homHetRatios[chrBin]['ratio']]

    return homHetRatios


def main():
    scaffoldData, homHetRatios = readScaffoldData(sys.argv[1], delimiter=',')
    homHetRatios = processMutationData(sys.argv[2], scaffoldData, homHetRatios)
    # for each bin: output chromosome, bin, hom, het, ratio
    for chrBin in sorted(homHetRatios):
        print '\t'.join(map(str, list(chrBin) + homHetRatios[chrBin]))




    pass

if __name__ == '__main__': main()
