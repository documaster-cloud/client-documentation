# 🐞 Troubleshooting: Connecting to SFTP server

This article provides help and guidance when troubleshooting issues you might have connecting to our SFTP server.
The following sections describes errors you might face and tips on how to solve them.

## 1. You are asked to provide a password when using your SSH key

When trying to connect using the username and domain that we provide (on the format
`<storage-account>.<company-username>@.<storage-account>.blob.core.windows.net`), you are asked to provide a password:

```bash
> sftp storageaccount.exampleuser@storageaccount.blob.core.windows.net
storageaccount.exampleuser@storageaccount.blob.core.windows.net's password:
```

This will typically happen if either of your keys can be used for connection. It can be many reasons why neither of your
keys work (that does not necessarily mean that there is something wrong with the key(s)). Hence, the following sections
are meant to provide debugging help so that you can find the actual reason.

### Use the `verbose` option when trying to connect (for debugging)

When you connect, try to include the `verbose` option:

```bash
sftp -v storageaccount.exampleuser@storageaccount.blob.core.windows.net
```

Running with the `-v` option might tell you why you cannot connect.

### Check your key format

Azure currently supports SSH protocol 2 (SSH-2) RSA (minimum 2048 bits) and ECDSA keys only. The supported algorithms
are presented [here](https://learn.microsoft.com/en-us/azure/storage/blobs/secure-file-transfer-protocol-support#supported-algorithms).

This means that your public key file should look like one of the following keys:

#### SSH2
```
---- BEGIN SSH2 PUBLIC KEY ----
Comment: "rsa-key"
AAAA<LONG RANDOM STRING>
---- END SSH2 PUBLIC KEY ----
```

#### OpenSSH
```
ssh-rsa AAAA<LONG RANDOM STRING> <OPTIONAL COMMENT>
```

#### ECDSA
```
ecdsa-sha2-nistp256 AAAA<LONG RANDOM STRING> <OPTIONAL COMMENT>
```


### Make sure that your SSH key is added to the ssh-agent

You do so by making sure the ssh-agent is running in the background:

```
$ eval "$(ssh-agent -s)"
```

and modifying your `~/.ssh/config` file to include your new key.

Please refer to the [documentation](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)
provided by GitHub for a full description of these steps.


### SSH-RSA key rejected with message "no mutual signature algorithm"

When running the command `sftp -v ...`, the following output can be seen:

```bash
debug1: Authentications that can continue: publickey,password
debug1: Next authentication method: publickey
debug1: Offering public key: /home/user/.ssh/id_rsa RSA ... agent
debug1: send_pubkey_test: no mutual signature algorithm
```

`send_pubkey_test: no mutual signature algorithm` typically means that ssh-rsa is not enabled. Please refer to documentation
specific to your operating system for how to handle this.

If you have a Mac, this is a common issue on MacOS Ventura since the OpenSSH that ships with MacOS Ventura disables RSA
signatures by default. [This article](https://osxdaily.com/2022/12/22/fix-ssh-not-working-macos-rsa-issue/) explains what
you can do to fix it.


## 2. Timeout error

```bash
> sftp storageaccount.exampleuser@storageaccount.blob.core.windows.net
Received disconnect from <IP> port 22:11:  - RequestId:47cbcb74-d01e-0052-45f4-7103cc000000 Time:2023-04-18T12:54:26.2767690Z
Disconnected from <IP> port 22
Connection closed
```

The reason for this is often caused by you trying to access the server from an IP address that is not approved/whitelisted. 
Please send us the IPs you need to whitelist. 
