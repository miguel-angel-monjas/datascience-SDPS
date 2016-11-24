import boto3
import os
import threading
import argparse
import logging


def new_s3_client():
    # initialize an S3 client with a private session so that multithreading
    # doesn't cause issues with the client's internal state
    session = boto3.session.Session()
    return session.client('s3')


def collect_parts(s3, folder, preffix):
    file_list = []
    for item in _list_all_objects_with_size(s3, folder):
        if preffix in item[0]:
            file_list.append(item)
    return file_list


def _list_all_objects_with_size(s3, folder):
    def resp_to_filelist(resp):
        return [(x['Key'], x['Size']) for x in resp['Contents']]

    objects_list = []
    resp = s3.list_objects(Bucket=BUCKET, Prefix=folder)
    objects_list.extend(resp_to_filelist(resp))
    while resp['IsTruncated']:
        # if there are more entries than can be returned in one request, the key
        # of the last entry returned acts as a pagination value for the next request
        logging.warning("Found {} objects so far".format(len(objects_list)))
        last_key = objects_list[-1][0]
        resp = s3.list_objects(Bucket=BUCKET, Prefix=folder, Marker=last_key)
        objects_list.extend(resp_to_filelist(resp))
    return objects_list


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="S3 file combiner")
    parser.add_argument("--bucket", help="base bucket to use")
    parser.add_argument("--folder", help="folder whose contents should be combined")
    parser.add_argument("--preffix", help="preffix of files to include in the combination")

    args = parser.parse_args()

    BUCKET = args.bucket
    s3 = new_s3_client()
    parts_list = collect_parts(s3, args.folder, args.preffix)
    # print parts_list

    small_parts = []
    ouptput_filename = 'results_.txt'
    for source_part in parts_list:
        temp_filename = "/tmp/{}".format(source_part[0].replace("/", "_"))
        s3.download_file(Bucket=BUCKET, Key=source_part[0], Filename=temp_filename)

        with open(temp_filename, 'rb') as f:
            small_parts.append(f.read())
            # os.remove(temp_filename)
    if len(small_parts) > 0:
        total_part = ''.join(small_parts)
    total_lines = total_part.splitlines()
    g = open(ouptput_filename, 'w')
    for line in sorted(total_lines):
        print line
        g.write(line.strip() + '\n')
    g.close()
