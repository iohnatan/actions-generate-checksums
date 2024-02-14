import hashlib
import os
import glob
import argparse


def compute_checksum(file_path: str):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def main(pattern: str, suffix: str, subfolder: str):
    for filename in glob.glob(pattern):
        parent, base = os.path.split(filename)
        checksum = compute_checksum(filename)

        parent = os.path.join(parent, subfolder)
        if not os.path.exists(parent):
             os.mkdir(parent)
        elif not os.path.isdir(parent):
             raise Exception("Subfolder already exist but is not a folder.")
        
        with open(os.path.join(parent, f"{base}.{suffix}"), "w") as f:
            f.write(checksum)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate checksums for multiple files"
    )
    parser.add_argument(
        "--pattern", required=True, help="Pattern to search for files (glob)"
    )
    parser.add_argument(
        "--suffix", default="checksum", help="Suffix for the checksum files"
    )
    parser.add_argument(
        "--subfolder", required=False, help="Subfolder to put the checksum files"
    )

    args = parser.parse_args()
    main(pattern=args.pattern, suffix=args.suffix, subfolder=args.subfolder)
