# MediaDC Mass Deleter

Use the json export of MediaDC (NextCloud app) to delete files massively
  

    usage: MediaDC - Mass deleter [-h] [--exclude EXCLUDE [EXCLUDE ...]] [--include INCLUDE [INCLUDE ...]] [--dry-run] [--different-path-only] --host
                                  HOST --login LOGIN --password PASSWORD [--verify-ssl]
                                  json

    Takes the json export from MediaDC and massively delete all replicates

    positional arguments:
      json                  Path to the json file

    optional arguments:
      -h, --help            show this help message and exit
      --exclude EXCLUDE [EXCLUDE ...]
                            Do not delete files whose path contains this (if size is similar)
      --include INCLUDE [INCLUDE ...]
                            Prefer to delete files whose path contains this (if size is similar)
      --dry-run             Do not actually delete files
      --different-path-only
                            Only delete files in different path (to avoid deleting pictures just a bit similar)
      --host HOST           WebDav full URL as given in the bottom left of the root URL
      --login LOGIN         Login
      --password PASSWORD   Password
      --verify-ssl          Do verify SSL certificate

## Getting the json file out of MediaDC

<img width="941" alt="image" src="https://github.com/tbarbette/mediadc-massdelete/assets/248961/df6a2634-d9a1-4d4a-934a-94d71c8695ca">

<img width="321" alt="image" src="https://github.com/tbarbette/mediadc-massdelete/assets/248961/e45bb503-4fdb-4366-b1b3-1ef25b3c6ba1">

## Example

Sample command : `python3 mediadc_delete.py --exclude workspace --include DCIM Temp Import Upload temp --host "https://server.com/nextcloud/remote.php/dav/files/user" --login user --password XXX ../../Downloads/2_task_results_export.json --different-path-only`
