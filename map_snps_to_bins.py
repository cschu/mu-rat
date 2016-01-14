#!/usr/bin/env python
import sys
import csv

from popseq_io import readScaffoldData

def main():
    scaffoldData, _ = readScaffoldData(sys.argv[1], delimiter=',')

    reader = csv.reader(open(sys.argv[2]), delimiter='\t', quotechar='"')
    for row in reader:
        contig, pos, sus_AO, sus_DP, sus_AF, res_AO, res_DP, res_AF = row
        # scaffoldData: scaffold_id: (chromosome, bin)
        chromosome_bin = scaffoldData.get(contig, None)
        if chromosome_bin is None:
            continue
        chromosome, bin = chromosome_bin
        out_row = map(str, [chromosome, bin, sus_AF, res_AF])
        sys.stdout.write('\t'.join(out_row) + '\n')





    pass

if __name__ == '__main__': main()
