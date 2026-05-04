# Athena
##  AthenaReader [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/athena/#llama_index.readers.athena.AthenaReader "Permanent link")
Bases: 
Athena reader.
Follow AWS best practices for security. AWS discourages hardcoding credentials in code. We recommend that you use IAM roles instead of IAM user credentials. If you must use credentials, do not embed them in your code. Instead, store them in environment variables or in a separate configuration file.
Source code in `llama-index-integrations/readers/llama-index-readers-athena/llama_index/readers/athena/base.py`  
| 
```
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
```
 | 
```
classAthenaReader(BaseReader):
"""
    Athena reader.

    Follow AWS best practices for security.
    AWS discourages hardcoding credentials in code.
    We recommend that you use IAM roles instead of IAM user credentials.
    If you must use credentials, do not embed them in your code.
    Instead, store them in environment variables or in a separate configuration file.

    """

    def__init__(
        self,
    ) -> None:
"""Initialize with parameters."""

    defcreate_athena_engine(
        self,
        aws_access_key: Optional[str] = None,
        aws_secret_key: Optional[str] = None,
        aws_region: str = None,
        s3_staging_dir: str = None,
        database: str = None,
        workgroup: str = None,
    ):
"""
        Args:
        aws_access_key is the AWS access key from aws credential
        aws_secret_key is the AWS secret key from aws credential
        aws_region is the AWS region
        s3_staging_dir is the S3 staging (result bucket) directory
        database is the Athena database name
        workgroup is the Athena workgroup name.

        """
        if not aws_access_key or not aws_secret_key:
            conn_str = (
                "awsathena+rest://:@athena.{region_name}.amazonaws.com:443/"
                "{database}?s3_staging_dir={s3_staging_dir}?work_group={workgroup}"
            )

            engine = create_engine(
                conn_str.format(
                    region_name=aws_region,
                    s3_staging_dir=s3_staging_dir,
                    database=database,
                    workgroup=workgroup,
                )
            )

        else:
            warnings.warn(
                "aws_access_key and aws_secret_key are set. We recommend to use IAM role instead."
            )
            boto3.client(
                "athena",
                aws_access_key_id=aws_access_key,
                aws_secret_access_key=aws_secret_key,
                region_name=aws_region,
            )

            conn_str = (
                "awsathena+rest://:@athena.{region_name}.amazonaws.com:443/"
                "{database}?s3_staging_dir={s3_staging_dir}?work_group={workgroup}"
            )

            engine = create_engine(
                conn_str.format(
                    region_name=aws_region,
                    s3_staging_dir=s3_staging_dir,
                    database=database,
                    workgroup=workgroup,
                )
            )
        return engine

```
 |  
| --- | --- |  
###  create_athena_engine [#](https://developers.llamaindex.ai/python/framework-api-reference/readers/athena/#llama_index.readers.athena.AthenaReader.create_athena_engine "Permanent link")

```
create_athena_engine(
    aws_access_key: Optional[] = None,
    aws_secret_key: Optional[] = None,
    aws_region:  = None,
    s3_staging_dir:  = None,
    database:  = None,
    workgroup:  = None,
)

```

Args: aws_access_key is the AWS access key from aws credential aws_secret_key is the AWS secret key from aws credential aws_region is the AWS region s3_staging_dir is the S3 staging (result bucket) directory database is the Athena database name workgroup is the Athena workgroup name.
Source code in `llama-index-integrations/readers/llama-index-readers-athena/llama_index/readers/athena/base.py`  
| 
```
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
```
 | 
```
defcreate_athena_engine(
    self,
    aws_access_key: Optional[str] = None,
    aws_secret_key: Optional[str] = None,
    aws_region: str = None,
    s3_staging_dir: str = None,
    database: str = None,
    workgroup: str = None,
):
"""
    Args:
    aws_access_key is the AWS access key from aws credential
    aws_secret_key is the AWS secret key from aws credential
    aws_region is the AWS region
    s3_staging_dir is the S3 staging (result bucket) directory
    database is the Athena database name
    workgroup is the Athena workgroup name.

    """
    if not aws_access_key or not aws_secret_key:
        conn_str = (
            "awsathena+rest://:@athena.{region_name}.amazonaws.com:443/"
            "{database}?s3_staging_dir={s3_staging_dir}?work_group={workgroup}"
        )

        engine = create_engine(
            conn_str.format(
                region_name=aws_region,
                s3_staging_dir=s3_staging_dir,
                database=database,
                workgroup=workgroup,
            )
        )

    else:
        warnings.warn(
            "aws_access_key and aws_secret_key are set. We recommend to use IAM role instead."
        )
        boto3.client(
            "athena",
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=aws_region,
        )

        conn_str = (
            "awsathena+rest://:@athena.{region_name}.amazonaws.com:443/"
            "{database}?s3_staging_dir={s3_staging_dir}?work_group={workgroup}"
        )

        engine = create_engine(
            conn_str.format(
                region_name=aws_region,
                s3_staging_dir=s3_staging_dir,
                database=database,
                workgroup=workgroup,
            )
        )
    return engine

```
 |  
| --- | --- |  
options: members: - AthenaReader
