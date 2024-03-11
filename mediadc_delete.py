from webdav3.client import Client
from webdav3.exceptions import RemoteResourceNotFound,ResponseErrorCode
import argparse
import json

parser = argparse.ArgumentParser(
                    prog='MediaDC - Mass deleter',
                    description='Takes the json export from MediaDC and massively delete all replicates',
                    )

parser.add_argument('--exclude',type=str,nargs='+',
                    help='Never delete files whose path contains this')
parser.add_argument('--dry-run',action='store_true',default=False,
                    help='Do not actually delete files')

parser.add_argument('--host',type=str,required=True,
                    help='WebDav full URL as given in the bottom left of the root URL')
parser.add_argument('--login',type=str,required=True,
                    help='Login')
parser.add_argument('--password',type=str,required=True,
                    help='Password')

parser.add_argument('json',type=str,
                    help='Path to the json file')


args = parser.parse_args()
if args.exclude is None:
    args.exclude = []

# Connect to webdav
options = {
 'webdav_hostname': args.host,
 'webdav_login':    args.login,
 'webdav_password': args.password,
}


client = Client(options)
client.verify = True #False # To not check SSL certificates (Default = True)
#client.execute_request("rm", '')

def remove(path):
    """
    Actually removes a remote file given its path
    """
    if path.startswith("files/"):
        path=path[6:]

    assert(path) # Just to be sure we won't delete everything
    try:
        if args.dry_run:
            print(" ",client.info(path))
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



    print("  Could not decide...")
    return None

dc = json.load(open(args.json))
for result in dc["Results"]:
    files=result["files"]
    if len(files) == 2:
        a = files[0]
        b = files[1]
        if a["filesize"] == b["filesize"]:
            print(f"File with the same size : {a['filename']} {b['filename']}")
            f = choose(a,b)
        else:
            if a["filesize"] > b["filesize"]:
                f = a
            else:
                f = b
        if f:
            print(f"Deleting {f['filename']}")
            remove(f['filepath'])
