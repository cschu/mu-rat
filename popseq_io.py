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

def readMutationData(fn, scaffoldData, delimiter=' '):
    """
    Provides a generator to the mutation data, i.e. to each row in the input file fn
    that has data in scaffoldData.
    """
    with open(fn) as fi:
        reader = csv.reader(fi, delimiter=delimiter, quotechar='"')
        for row in reader:
            if len(row) >= 13:
                chrBin = scaffoldData.get(row[0], None)
                if chrBin is not None:
                    assert row[7] in ('hom', 'het'), row[7]
                    yield chrBin, row


def main():
    pass

if __name__ == '__main__': main()
