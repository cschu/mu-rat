#!/usr/bin/env python
import sys
import csv


def readScaffoldData(fn, delimiter=' '):
    """
    Reads scaffold data and builds up two dictonaries:
    scaffoldData: scaffold_id: (chromosome, bin)
    homHetRatios: (chromosome, bin): hom count, het count, het/hom ratio (NA if hom==0)
    By default assumes that data is in space(!)-delimited format, if tab-delimited then delimiter has to be set.
    """
    scaffoldData = {}
    homHetRatios = {}
    with open(fn) as fi:
        reader = csv.reader(fi, delimiter=delimiter, quotechar='"')
        for row in reader:
            if len(row) >= 3:
                scaffoldData[row[0]] = (row[1], row[2])
                homHetRatios[(row[1], row[2])] = {'hom': 0.0, 'het': 0.0}
    return scaffoldData, homHetRatios

def readMutationData(fn, scaffoldData, homHetRatios, delimiter=' '):
    """
    Reads mutation data, counts the number of hom/het mutations per bin, and
    calculates het/hom ratio. The hom/het counts are stored in another dictonary per bin
    such that we can directly count the number of occurrences of "het" and "hom".
    """
    with open(fn) as fi:
        reader = csv.reader(fi, delimiter=delimiter, quotechar='"')
        for row in reader:
            if len(row) >= 13:
                chrBin = scaffoldData.get(row[0], None)
                if chrBin is not None:
                    assert row[7] in ('hom', 'het'), row[7]
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
    scaffoldData, homHetRatios = readScaffoldData(sys.argv[1])
    homHetRatios = readMutationData(sys.argv[2], scaffoldData, homHetRatios)

    # for each bin: output chromosome, bin, hom, het, ratio
    for chrBin in sorted(homHetRatios):
        print '\t'.join(map(str, list(chrBin) + homHetRatios[chrBin]))




    pass

if __name__ == '__main__': main()