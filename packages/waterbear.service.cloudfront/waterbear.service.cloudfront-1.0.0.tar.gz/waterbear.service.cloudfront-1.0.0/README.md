OA# waterbear.service.cloudfront

A Lambda that manages the following CloudFront services:
  * Updates origin security groups with latest CloudFront IP ranges

## Installation

Install zc.buildout with pip:

    $ pip install zc.buildout

Checkout `waterbear.s3release` repo and put it at the same directory level
as this repo (one day we can replace this with a PyPI package).

Change to this directory and run buildout:

    $ cd waterbear.service.cloudfront
    $ buildout

Now you've got everything installed. For your convenience, a `profile.sh` has been created
to put the local environment on your PATH:

    $ source profile.sh

## Development

Deploy dev releases to Waterbear Paco with:

  paco lambda deploy service.cloudfront.tools.us-west-2.notification.groups.lambda.resources.function


## Release

Use zest.releaser to do a release. The release process has 3 parts:

 1. prerelease

    - Add current date to the CHANGELOG.md

    - Choose a version number to release

    - Strip the .dev0 from the version and commit

 2. release

    - Create a git Tag

    - Create a zip file and publish to S3

 3. postrelease

    - Change the version number and add .dev0

    - Create a new entry in CHANGELOG.md
