
# Utilites for working with AWS S3 objects

```shell

# extract data from S3 objects and store them into a JSON file for later use
python get_file_list.py --prefix="video/" --bucket=brick.vino9.net --output=video_file_list.json

# compare the file listed in input file and check if the corresponding local file exists and is of the same size
python check_files.py --input=video_file_list.json --base=/volume1/media

# using bulk delete API to delete objects from S3 bucket quickly
python bulk_del.py --bucket=brick.vino9.net --prefix=blackhole/old

```

## AWS CLI for restore files from Glacier

```shell

# get a list of files
aws s3api list-objects --bucket bucket_name_ --query 'Contents[].Key' --prefix="prefix/" | jq -r '.[]' > obj_list.txt

# check the restore status for objects in a list, initiate restore if it is yet to start
./restore_status < obj_list.txt


```
