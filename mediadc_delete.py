from webdav3.client import Client
from webdav3.exceptions import RemoteResourceNotFound,ResponseErrorCode
import argparse
import json
import pathlib

parser = argparse.ArgumentParser(
                    prog='MediaDC - Mass deleter',
                    description='Takes the json export from MediaDC and massively delete all replicates',
                    )

parser.add_argument('--exclude',type=str,nargs='+',
                    help='Do not delete files whose path contains this (if size is similar)')
parser.add_argument('--include',type=str,nargs='+',
                    help='Prefer to delete files whose path contains this (if size is similar)')
parser.add_argument('--dry-run',action='store_true',default=False,
                    help='Do not actually delete files')

parser.add_argument('--different-path-only',action='store_true',default=False,
                    help='Only delete files in different path (to avoid deleting pictures just a bit similar). Applicable only to files with different sizes. Files in the same folder with the exact same size are most probably duplicates.')
parser.add_argument('--different-path-only-except',dest="diff_except", nargs='+',type=str,default=["WA"],
        help='Exception to the previous option. Typicall if you imported pictures from a smartphone non-carefully, you have an original version of your picture and one you might have sent on whatsapp. By adding WA you will delete files that contains WA even if they are in the same folder. Default: [WA]')

parser.add_argument('--host',type=str,required=True,
                    help='WebDav full URL as given in the bottom left of the root URL')
parser.add_argument('--login',type=str,required=True,
                    help='Login')
parser.add_argument('--password',type=str,required=True,
                    help='Password')
parser.add_argument('--verify-ssl',action='store_true',default=False,
                    help='Do verify SSL certificate')


parser.add_argument('json',type=str,
                    help='Path to the json file')


args = parser.parse_args()
if args.exclude is None:
    args.exclude = []
if args.include is None:
    args.include = []

# Connect to webdav
options = {
 'webdav_hostname': args.host,
 'webdav_login':    args.login,
 'webdav_password': args.password,
}


client = Client(options)
client.verify = args.verify_ssl

def remove(path):
    """
    Actually removes a remote file given its path
    """
    if path.startswith("files/"):
        path=path[6:]

    assert(path) # Just to be sure we won't delete everything
    try:
        if args.dry_run:
            print("Would delete : ",client.info(path))
        else:
            client.clean(path)
    except RemoteResourceNotFound:
        print(f"  {path} does not exist anymore...")
    except ResponseErrorCode as e:
        print(f"  error {e} while deleting {path}")

def choose(a,b):
    """
    Select between two copies of the same picture with the same size
    """
    l = [a,b]
    dst = [a,b]
    for e in args.exclude:
        for s in l:
            if e in s['filepath']:
                dst.remove(s)
    if len(dst) == 0:
        print("  Exclusion patterns removed all files...")
        return None
    if len(dst) == 1:
        return dst[0]

    inc = {}
    for e in args.include:
        for s in l:
            if e in s['filepath']:
                inc[s['filepath']] = s
    if len(inc) == 0:
        print("  Inclusion patterns did not select a file...")
        return None
    if len(inc) == 1:
        return next(iter(inc.items()))[1]

    print("  Could not decide...")
    return None

dc = json.load(open(args.json))
for result in dc["Results"]:
    all_files=result["files"]
    files = []
    for f in all_files:
        if f['filepath'].startswith("files_trashbin"):
            continue
        files.append(f)
    if len(files) == 2:
        a = files[0]
        b = files[1]

        if a["filesize"] == b["filesize"]:
            print(f"File with the same size : {a['filepath']} {b['filepath']}")
            f = choose(a,b)
        else:
            if args.different_path_only and \
                pathlib.Path(a["filepath"]).parent.resolve() == pathlib.Path(b["filepath"]).parent.resolve():
                    h = False
                    if args.diff_except:
                        for e in args.diff_except:
                            for s in [a,b]:
                                if e in s['filepath']:
                                    h = True
                    if h:
                        print(f"Deleting the smallest path even if it is in the same folder because it matched an exception pattern.")
                    else:
                        print(f"Ignoring files in the same folder : {a['filepath']} {b['filepath']}")
                        continue
            if a["filesize"] < b["filesize"]:
                f = a
            else:
                f = b
        if f:
            print(f"Deleting {f['filename']} ({a['filepath']} {b['filepath']})")
            try:
                remove(f['filepath'])
            except Exception as e:
                print(f"ERROR while deleting {f['filename']} :", e)
