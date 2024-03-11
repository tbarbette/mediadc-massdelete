# MediaDC Mass Deleter

Use the json export of MediaDC (NextCloud app) to massively delete files

usage: MediaDC - Mass deleter [-h] [--exclude EXCLUDE [EXCLUDE ...]] [--dry-run] --host HOST --login LOGIN --password PASSWORD json

Takes the json export from MediaDC and massively delete all replicates

positional arguments:
  json                  Path to the json file

optional arguments:
  -h, --help            show this help message and exit
  --exclude EXCLUDE [EXCLUDE ...]
                        Never delete files whose path contains this
  --dry-run             Do not actually delete files
  --host HOST           WebDav full URL as given in the bottom left of the root URL
  --login LOGIN         Login
  --password PASSWORD   Password