import hashlib
import os
import glob
import argparse


def compute_checksum( file_path: str ):
    sha256_hash = hashlib.sha256()
    with open( file_path, "rb" ) as f:
        for byte_block in iter( lambda: f.read( 4096 ), b"" ):
            sha256_hash.update( byte_block )
    return sha256_hash.hexdigest()


def main( pattern: str, suffix: str, subfolder: str, files_ignore: list[str] ):
    for filepath in glob.glob( pattern, recursive=True ):
        parent_path, basename = os.path.split( filepath )
        file_extension        = os.path.splitext( filepath )[1]

        if ( os.path.isdir( filepath ) or # skip folders.
             file_extension == suffix  or # skip checksum files.
             basename in files_ignore
        ):
            continue

        checksum = compute_checksum( filepath )

        subfolder_path = os.path.join( parent_path, subfolder )
        if not os.path.exists( subfolder_path ):
             os.mkdir( subfolder_path )
        elif not os.path.isdir( subfolder_path ):
             raise Exception( "Subfolder already exist but is not a folder." )

        with open( os.path.join( subfolder_path, f"{basename}.{suffix}" ), "w" ) as f:
            f.write( checksum )


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
    parser.add_argument(
        "--files_ignore", required=False, default=[], help="Files to ignore"
    )

    args = parser.parse_args()
    main( pattern=args.pattern, suffix=args.suffix, subfolder=args.subfolder, files_ignore=args.files_ignore )
