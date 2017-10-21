import sys
sys.path.append('scripts/')
import re
import os
from optparse import OptionParser
from statistics import mean
from de_bruijn_graph_from_kmers import de_bruijn_graph
from contig_from_collection_of_reads import maximal_nonbranching_paths

def parse_options():
    '''parses the options for script and returns options'''
    parser = OptionParser()
    parser.add_option('-f', '--file',
            dest='filename', help='the fasta file to read from')
    parser.add_option('-k', '--kmer-length',
            dest='k', type='int', default=10,
            help='the value of k for kmers; the default value is k = 10')
    parser.add_option('-e', '--handle-errors',
            dest='handle_errors', action='store_true',
            help='handles errors if this flag is on')
    parser.add_option('-p', '--plot-histogram',
            dest='create_histogram', action='store_true',
            help='will create an png image of the kmer frequencies if this flag is on (the system running the script must have matplotlib installed to be able to use this flag); must be used in conjunction with the -e flag')
    parser.add_option('-v', '--verbose',
            dest='verbose', action='store_true',
            help='if this flag is on, will print out metrics to the console')
    return parser.parse_args()

def get_reads(filename):
    '''takes a fasta file and returns a list of reads with the meta data removed'''
    with open(filename) as file:
        reads = []
        read = ''
        for line in file.readlines():
            line = line.strip()
            if not line.startswith('>'):
                read = read + line
            else:
                reads.append(read)
                read = ''
    reads.append(read)
    reads = reads[1:]
    return reads

def get_kmers(reads, k):
    '''takes a list of reads and returns a list of all kmers of length k found in all reads'''
    kmers = [read[i:i+k] for read in reads for i in range(len(read) - k + 1)]
    return kmers

def get_freqs(kmers):
    '''takes a list of kmers and returns a dictionary of kmers and their counts'''
    freqs = {}
    for kmer in kmers:
        if kmer in freqs:
            freqs[kmer] = freqs[kmer] + 1
        else:
            freqs[kmer] = 1
    return freqs

def create_hist(freqs, options):
    '''creates a histogram for the coverage'''
    counts = get_freqs(list(freqs.values()))
    err_cutoff = sorted(list(counts.keys()))[0]
    for key in sorted(list(counts.keys())):
        if counts[key] > counts[err_cutoff]:
            break
        else:
            err_cutoff = key

    if (options.create_histogram):
        import matplotlib.pyplot as plt
        hist = [key for key, val in counts.items() for i in range(val)]
        n, bins, patches = plt.hist(hist, max(hist), normed=True, facecolor='g', alpha=0.75)
        plt.xlabel('Coverage')
        plt.ylabel('Density')
        plt.grid(True)
        plt.axvline(x=err_cutoff, ls='--', c='r', lw='5')
    #    plt.axis([1, 50, 0, 0.1])

        capture = re.search(r'/(.+.)fasta$', options.filename)
        plt.savefig('coverage/' + capture.group(1) + 'coverage.k.' + str(options.k) + '.png')
    return err_cutoff

def write_output(contigs, options):
    contigs.sort(key=len, reverse=True)
  
    # Get metrics from contigs
    avg_length, n50, num_contigs, max_length = get_metrics(contigs)
    if options.verbose:
        print('K:', options.k)
        print('AVG SIZE:', avg_length)
        print('N50:', n50)
        print('NUM CONTIGS:', num_contigs)
        print('MAX SIZE:', max_length)

    # Configure output file
    out_filename = re.search(r'/(.+.)fasta$', options.filename).group(1)
    out_filename = ''.join(['results/', out_filename, 'contigs.k.', str(options.k),  '.fasta'])

    # Write contigs to output fasta file
    with open(out_filename, 'w') as outfile:
        for i in range(len(contigs)):
            outfile.write('>contig: ')
            outfile.write(str(i))
            outfile.write(' length: ')
            outfile.write(str(len(contigs[i])))
            outfile.write('\n')
            while len(contigs[i]) > 70:
                outfile.write(contigs[i][:70])
                outfile.write('\n')
                contigs[i] = contigs[i][70:]
            outfile.write(contigs[i])
            outfile.write('\n')

    # Write metrics
    metrics_filename =  re.sub(r'contigs.k.\d+', 'metrics', out_filename).replace('fasta', 'tsv')
    if not os.path.exists(metrics_filename):
        with open(metrics_filename, 'w') as metrics_file:
            labels = ['K', 'AVG CONTIG SIZE', 'N50', 'NUM CONTIGS', 'MAX CONTIG SIZE', '\n']
            metrics_file.write('\t'.join(labels))
    with open(metrics_filename, 'a') as metrics_file:
        values = [options.k, avg_length, n50, num_contigs, max_length]
        metrics_file.write('\t'.join([str(x) for x in values]))
        metrics_file.write('\n')

def get_metrics(contigs):
    contig_lengths = [len(contig) for contig in contigs]
    max_length = max(contig_lengths)
    avg_length = mean(contig_lengths)
    num_contigs = len(contig_lengths)
    half_total_length = sum(contig_lengths) / 2

    for length in contig_lengths:
        half_total_length = half_total_length - length
        if half_total_length < 0:
            n50 = length
            break
    
    return avg_length, n50, num_contigs, max_length

if __name__ == '__main__':
    ( options, args ) = parse_options()
    reads = get_reads( options.filename )
    kmers = get_kmers(reads, options.k)
    freqs = get_freqs(kmers)
    kmers = list(set(kmers))
    if (options.handle_errors):
        err_cutoff = create_hist(freqs, options)
        for kmer, freq in freqs.items():
            if freq < err_cutoff:
                kmers.remove(kmer)
    graph = de_bruijn_graph(kmers)
    contigs = maximal_nonbranching_paths(graph) 
    write_output(contigs, options)
