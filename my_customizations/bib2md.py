#!/usr/bin/env python

# Script to parse bibtex file and generate a markdown file for my website

from pybtex.database import parse_file
import argparse
import re

## HELPER FUNCTIONS
# Function to generate formatted citation
def formatted_citation(bib):
    reference = ''

    for i in range(len(bib.persons['author'])):
        if '{' in bib.persons['author'][i].last_names[0] and '}' in bib.persons['author'][i].last_names[0]:
            name = re.sub('\{|\}|\?', '', bib.persons['author'][i].last_names[0])
        elif bib.persons['author'][i].last_names[0] == 'others':
            name = '<i>et al.</i>'
        elif bib.persons['author'][i].middle_names == []:
            name = bib.persons['author'][i].last_names[0] + ' ' + bib.persons['author'][i].first_names[0][0]
        else:
            name = (bib.persons['author'][i].last_names[0]) + ' ' + bib.persons['author'][i].first_names[0][0] + bib.persons['author'][i].middle_names[0][0]
        name = name.replace('$...$', '...')
        name = name.replace('\\', '')

        if i == len(bib.persons['author'])-1:
            reference += name
        else:
            reference += name + ', '
    reference += ' (%s) ' % bib.fields['year']
    reference += '%s. ' % ((bib.fields['title'].replace('{', '')).replace('}', '')).replace('\textit', '')
    if 'journal' in bib.fields:
        reference += '<i>%s</i> ' % bib.fields['journal']
    elif 'booktitle' in bib.fields:
        reference += '<i>%s</i> ' % bib.fields['booktitle']
    if 'volume' in bib.fields and 'number' in bib.fields:
        reference += '%s(%s) ' % (bib.fields['volume'], bib.fields['number'])
    elif 'volume' in bib.fields:
        reference += '%s ' % (bib.fields['volume'])
    reference += ('%s.' % bib.fields['pages']).replace('--', '-')

    # formatting changes
    reference = reference.replace('Pejaver V', '<b>Pejaver V</b>')
    reference = reference.replace('Pejaver VR', '<b>Pejaver VR</b>')
    #reference = reference.replace('*', '\*')
    reference = reference.replace('\string', '')
    reference = reference.replace('\\?', '')
    
    return reference

# Function to generate formatted markdown
def md_output(key, value):
    md_text = ''

    # initialize variables
    paper_title = ((value.fields['title'].replace('{', '')).replace('}', '')).replace('\textit', '')
    year = value.fields['year']
    month = value.fields['month']
    if 'journal' in value.fields:
        journal = value.fields['journal']
    elif 'booktitle' in value.fields:
        journal = value.fields['booktitle']
    citation = formatted_citation(value)
    name = '%s-%s-%s' % (year, MONTHS[month], key)
    url = 'http://vpejaver.github.io/files/%s.pdf' % name
    
    # add to text
    md_text += '---\n'
    md_text += 'title: "%s"\n' % paper_title # Paper title
    md_text += 'collection: publications\n'
    md_text += 'permalink: /publication/%s\n' % name # Link
    md_text += 'excerpt: \'\'\n' # Excerpt (nothing for now)
    md_text += 'date: %s-%s-01\n' % (year, MONTHS[month]) # Year and month
    md_text += 'venue: \'%s\'\n' % journal # Journal
    #md_text += 'paperurl: \'%s\'\n' % url # URL
    md_text += 'citation: \'%s\'\n' % citation # Citation
    md_text += '---\n'
    md_text += '[Download paper here](%s)\n\n' % url
    #md_text += 'Recommended citation: %s\n' % citation
    
    return md_text, name

# Function to make the months dictionary (could improve how I do this)
def init_months():
    global MONTHS
    MONTHS = {}
    MONTHS.update(dict.fromkeys(['Jan', 'Jan.', 'jan', 'jan.', 'JAN', 'JAN.', 'January', 'january', 'JANUARY'], '01'))
    MONTHS.update(dict.fromkeys(['Feb', 'Feb.', 'feb', 'feb.', 'FEB', 'FEB.', 'Febuary', 'february', 'FEBRUARY'], '02'))
    MONTHS.update(dict.fromkeys(['Mar', 'Mar.', 'mar', 'mar.', 'MAR', 'MAR.', 'March', 'march', 'MARCH'], '03'))
    MONTHS.update(dict.fromkeys(['Apr', 'Apr.', 'apr', 'apr.', 'APR', 'APR.', 'April', 'april', 'APRIL'], '04'))
    MONTHS.update(dict.fromkeys(['May', 'May.', 'may', 'may.', 'MAY', 'MAY.', 'May', 'may', 'MAY'], '05'))
    MONTHS.update(dict.fromkeys(['Jun', 'Jun.', 'jun', 'jun.', 'JUN', 'JUN.', 'June', 'june', 'JUNE'], '06'))
    MONTHS.update(dict.fromkeys(['Jul', 'Jul.', 'jul', 'jul.', 'JUL', 'JUL.', 'July', 'july', 'JULY'], '07'))
    MONTHS.update(dict.fromkeys(['Aug', 'Aug.', 'aug', 'aug.', 'AUG', 'AUG.', 'August', 'august', 'AUGUST'], '08'))
    MONTHS.update(dict.fromkeys(['Sep', 'Sep.', 'sep', 'sep.', 'SEP', 'SEP.', 'September', 'september', 'SEPTEMBER'], '09'))
    MONTHS.update(dict.fromkeys(['Oct', 'Oct.', 'oct', 'oct.', 'OCT', 'OCT.', 'October', 'october', 'OCTOBER'], '10'))
    MONTHS.update(dict.fromkeys(['Nov', 'Nov.', 'nov', 'nov.', 'NOV', 'NOV.', 'November', 'november', 'NOVEMBER'], '11'))
    MONTHS.update(dict.fromkeys(['Dec', 'Dec.', 'dec', 'dec.', 'DEC', 'DEC.', 'December', 'december', 'DECEMBER'], '12'))


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

    # Initialize global dictionary for months
    init_months()
    
    # Read in bibtex file
    bib_data = parse_file(bibfile)

    # Loop and process each entry
    for k in sorted(bib_data.entries, key=str.lower):
        out_str, filename = md_output(k, bib_data.entries[k])
        outfile = outdir + '/' + filename + '.md'

        # write to output file
        fh = open(outfile, 'w')
        fh.write(out_str)
        fh.close()
