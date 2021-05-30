# S3 Policy Updater for Cloudflare's IP Pool

Easily keeps your AWS S3 Bucket Policy up to date with Cloudflare's latest set of IP addresses. It is expected that the policy is set to the one as shown in [Configuring an Amazon Web Services static site to use Cloudflare](https://support.cloudflare.com/hc/en-us/articles/360037983412-Configuring-an-Amazon-Web-Services-static-site-to-use-Cloudflare), else, you may need to adjust the statement index on line 44.

Designed for running with [AWS Lambda](https://aws.amazon.com/lambda/) using Python 3.8.

Ensure that the role used with your Lambda function has sufficient access to retrieve and modify the bucket's policy.

Two environment variables must be created, which can be set by heading to the `Configuration` then `Environmental variables` tab.
| Key    | Value            |
|--------|------------------|
| Bucket | Your Bucket Name |
| Region | Your AWS Region (ex. `us-east-1`)  |

The function can be automatically run on a schedule using the `EventBridge (CloudWatch Events)` trigger. For example, if you would like it to run every 6 hours, select `Schedule expression` as your rule type and enter `rate(6 hours)` for the schedule expression.
