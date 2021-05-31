#
# MIT License
#
# Copyright (c) 2021 Jayson Fong
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import json
import boto3
import os
import urllib.request


def update():
    ips = []
    with urllib.request.urlopen("https://api.cloudflare.com/client/v4/ips") as url:
        data = json.loads(url.read().decode())

        for ip4 in data['result']['ipv4_cidrs']:
            ips.append(ip4)

        for ip6 in data['result']['ipv6_cidrs']:
            ips.append(ip6)

    s3_client = boto3.client('s3', os.environ['Region'])
    for bucket in os.environ['Buckets'].split(','):
        bucket_policy = s3_client.get_bucket_policy(Bucket=bucket)
        bucket_policy_dict = json.loads(bucket_policy['Policy'])
        bucket_policy_dict['Statement'][0]['Condition']['IpAddress']['aws:SourceIp'] = ips
        s3_client.put_bucket_policy(Bucket=bucket, Policy=json.dumps(bucket_policy_dict))


def lambda_handler(event, context):
    update()
