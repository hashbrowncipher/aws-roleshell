aws-roleshell
=============

[aws-cli]: https://github.com/aws/aws-cli

A plugin for [aws-cli][aws-cli], designed to simplify
the task of loading credentials for assumed roles into environment variables.
This plugin retrieves credentials using AssumeRole, sets the appropriate
environment variables, and then executes a wrapped command. This is designed to
serve as an adapter for software which is not capable of assuming a role by
itself.

aws-roleshell makes use of the aws-cli temporary credentials cache, so multiple
roleshells can re-use the same temporary credentials until they expire. This is
especially useful for IAM roles that require MFA, because an MFA token is only
required once per hour, no matter how many shells are launched.

install
-------

First, `pip install` this egg.

Next, add the following into your ~/.aws/config:

    [plugins]
    roleshell = aws_roleshell

Or paste this into your terminal:

    cat<<EOF >> ~/.aws/roleshell
    [plugins]
    roleshell = aws_roleshell
    EOF

usage
-----

[role-docs]: https://docs.aws.amazon.com/cli/latest/topic/config-vars.html#using-aws-iam-roles

Configure an IAM Role based [aws-cli][aws-cli] profile. The
[documentation][role-docs] should assist you, but here's an example to save you
some reading:

    $ cat<<EOF >> ~/.aws/credentials

    [readonly]
    role_arn = arn:aws:iam::123456789012:role/readonly
    mfa_serial = arn:aws:iam::123456789012:mfa/myuser
    source_profile = default
    EOF

Now that you've set up your profile, you should be able to use it to launch a
roleshell roleshell:

    $ aws ec2 describe-instances # runs as 'user/myuser'
    $ aws --profile readonly roleshell
    Enter MFA code: ******
    $ aws ec2 describe-instances # runs as 'role/readonly'
