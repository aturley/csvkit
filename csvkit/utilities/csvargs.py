#!/usr/bin/env python

"""
csvargs 
"""

import itertools, subprocess, os

from csvkit import CSVKitReader, CSVKitWriter
from csvkit.cli import CSVKitUtility
from csvkit.headers import make_default_headers

class CSVArgs(CSVKitUtility):
    description = 'Execute a command repeatedly with a row of data as the arguments.'

    def add_arguments(self):
        self.argparser.add_argument('-n', '--names', dest='names_only', action='store_true',
                        help='Display column names and indices from the input CSV and exit.')
        self.argparser.add_argument('-C', '--not-columns', dest='not_columns',
                        help='A comma separated list of column indices or names to be excluded. Defaults to no columns.')
        self.argparser.add_argument('-x', '--delete-empty-rows', dest='delete_empty', action='store_true',
                        help='After cutting, delete rows which are completely empty.')

        self.argparser.add_argument('-c', '--command', dest='command',
                        help='A command to run. May include fixed arguments.')

    def main(self):
        if self.args.names_only:
            self.print_column_names()
            return

        rows = CSVKitReader(self.args.file, **self.reader_kwargs)

        if self.args.no_header_row:
            row = rows.next()

            column_names = make_default_headers(len(row))

            # Put the row back on top
            rows = itertools.chain([row], rows)
        else:
            column_names = rows.next()

        output = CSVKitWriter(self.output_file, **self.writer_kwargs)

        # output.writerow([column_names[c] for c in column_ids])

        for i, row in enumerate(rows):
            out_row = row

            if self.args.delete_empty:
                if ''.join(out_row) == '':
                    continue
            
            raw_command = self.args.command
            for col in out_row:
                raw_command = raw_command.replace("__", col, 1)

            # print raw_command
            # subprocess.call(raw_command)
            os.system(raw_command)
                
def launch_new_instance():
    utility = CSVArgs()
    utility.main()
    
if __name__ == "__main__":
    launch_new_instance()

