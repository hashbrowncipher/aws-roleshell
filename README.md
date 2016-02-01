aws-roleshell
=============

[aws-cli]: https://github.com/aws/aws-cli

An [aws-cli][aws-cli] plugin that loads IAM Role credentials into environment
variables. This plugin retrieves credentials using sts:AssumeRole, sets the
equivalent environment variables, and then executes a wrapped command. This
plugin is designed to serve as an adapter for software which is not capable of
assuming a role by itself.

Usage is like so:

    $ aws --profile readonly roleshell -- mycommand

In the above example, `mycommand` will run with IAM role credentials defined by
the `readonly` profile.

Or you could load the appropriate environment variables into your shell by
invoking roleshell without arguments:

    $ eval $(aws --profile readonly roleshell)

aws-roleshell makes use of the [aws-cli][aws-cli] temporary credentials cache,
so multiple roleshells can re-use the same temporary credentials until they
expire. This is especially useful for IAM roles that require MFA, because an
MFA token is only required once per hour (by default), no matter how many
shells are launched.

install
-------

After installing this egg into your `$PYTHONPATH`, add the following into your `~/.aws/config`:

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

After loading credentials, `aws roleshell` will launch whatever command you
specify on the command line. If no command is given, roleshell will output
shell-compatible variable exports for use with eval.

    $ aws ec2 describe-instances # runs as 'user/myuser'
    $ eval $(aws --profile readonly roleshell)
    Enter MFA code: ******
    $ aws ec2 describe-instances # runs as 'role/readonly'
    ...

similar projects
----------------

When I started working on this, I wasn't aware of quite how many other projects
provide STS-based role switching. As far as I am aware, this project is the
only one that both provides an aws-cli plugin and integrates with aws-cli's
configuration and caching features. But if an aws-cli plugin isn't your style,
try out one of the below options:

* [asagage/aws-mfa-script](https://github.com/asagage/aws-mfa-script) Bash, with dependency on aws-cli
* [boamski/aws-mfa](https://github.com/broamski/aws-mfa) Python, with dependency on boto3
* [civisanalytics/iam-role-injector](https://github.com/civisanalytics/iam-role-injector) Bash, with dependency on aws-cli
* [dcoker/awsmfa](https://github.com/dcoker/awsmfa/) Python, with dependency on botocore
* [jbuck/assume-aws-role](https://github.com/jbuck/assume-aws-role) Node.js
* [jimbrowne/aws-sts-helpers](https://github.com/jimbrowne/aws-sts-helpers) Bash and Python, with dependency on boto
* [lonelyplanet/aws-mfa](https://github.com/lonelyplanet/aws-mfa) Ruby, with dependency on aws-cli
* [paperg/awsudo](https://github.com/paperg/awsudo) Python, with dependency on boto
* [paybyphone/aws-role-init](https://github.com/paybyphone/aws-role-init) Python, with dependency on boto3
* [remind101/assume-role](https://github.com/remind101/assume-role) Go, with dependency on aws-cli
