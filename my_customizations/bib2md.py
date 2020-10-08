#!/usr/bin/env python

# Script to parse bibtex file and generate a markdown file for my website

#from pybtex.database.input import bibtex
#import pybtex.database.input.bibtex 
#from time import strptime
from pybtex.database import parse_file
import argparse
import string
import html
import os
import re


## HELPER FUNCTIONS
# Function to generate formatted citation
def formatted_citation(bib):
    reference = ''

    for i in range(len(bib.persons['author'])):
        if bib.persons['author'][i].last_names[0] == 'others':
            name = '<i>et al.</i>'
        elif bib.persons['author'][i].middle_names == []:
            name = bib.persons['author'][i].last_names[0] + ' ' + bib.persons['author'][i].first_names[0][0]
        else:
            name = (bib.persons['author'][i].last_names[0]) + ' ' + bib.persons['author'][i].first_names[0][0] + bib.persons['author'][i].middle_names[0][0]

        if i == len(bib.persons['author'])-1:
            reference += name
        else:
            reference += name + ', '
    reference += ' (%s) ' % bib.fields['year']
    reference += '%s. ' % bib.fields['title']
    reference += '<i>%s</i> ' % bib.fields['journal']
    reference += '%s(%s) ' % (bib.fields['volume'], bib.fields['number'])
    reference += ('%s.' % bib.fields['pages']).replace('--', '-')
    
    reference = reference.replace('Pejaver V', '*Pejaver V*')
    #print(reference)
    return reference

# Function to generate formatted markdown
def md_output(key, value):
    md_text = ''
    
    name = key
    paper_title = value.fields['title']
    year = value.fields['year']
    journal = value.fields['journal']
    url = 'http://academicpages.github.io/files/paper1.pdf'
    citation = formatted_citation(value) #'Your Name, You. (2009). &quot;Paper Title Number 1.&quot; <i>Journal 1</i>. 1(1).'
    
    md_text += '---\n'
    md_text += 'title: "%s"\n' % paper_title # Paper title
    md_text += 'collection: "publications"\n'
    md_text += 'permalink: /publication/%s\n' % name # Link
    md_text += 'date: %s-01-01\n' % year # Year
    md_text += 'venue: \'%s\'\n' % journal # Journal
    md_text += 'paperurl: \'%s\'\n' % url # URL
    md_text += 'citation: %s\n' % citation # Citation
    md_text += '---\n'
    md_text += '[Download paper here](%s)\n\n' % url
    md_text += 'Recommended citation: %s\n' % citation
    
    return md_text


## MAIN
if __name__ == '__main__':
    
    # Constants and defaults
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--bibfile', help='<Bibtex file containing references>')
    parser.add_argument('-o', '--outdir', help='<Output directory to place markdown files>')

    # Parse arguments
    args = parser.parse_args()
    
    # Check parameters
    if args.bibfile:
        bibfile = args.bibfile
    if args.outdir:
        outdir = args.outdir

    # Read in bibtex file
    bib_data = parse_file(bibfile)
    for k in sorted(bib_data.entries, key=str.lower):
        outfile = outdir + '/' + k + '.md'
        fh = open(outfile, 'w')
        out_str = md_output(k, bib_data.entries[k])
        fh.write(out_str)
        fh.close()
        
