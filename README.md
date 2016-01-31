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

aws-roleshell makes use of the [aws-cli][aws-cli] temporary credentials cache,
so multiple roleshells can re-use the same temporary credentials until they
expire. This is especially useful for IAM roles that require MFA, because an
MFA token is only required once per hour, no matter how many shells are
launched.

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
specify on the command line. If no command is given, roleshell will launch the
binary specified in the $SHELL environment variable.

    $ aws ec2 describe-instances # runs as 'user/myuser'
    $ aws --profile readonly roleshell
    Enter MFA code: ******
    $ aws ec2 describe-instances # runs as 'role/readonly'
    ...

In the example shown above, you may continue using the shell created by
roleshell until the temporary credentials expire. When you are done, exiting
the shell will return you to your original shell.

You might also define a convenience function to assume a role without
nesting shells. The example below has been tested with bash and zsh:

    assume_role() { exec aws --profile "$1" roleshell; }
