# Synda Debian package upgrade guide

## Synopsis

This document contains instructions to upgrade Synda version using Debian package.

## Procedure

### Pre-upgrade

Backup folders below

    /etc/synda/sdt
    /var/log/synda/sdt
    /var/lib/synda/sdt

### Upgrade

Remove previous package version

    sudo dpkg -P synda

Install new package version using [this guide](deb_install.md)

### Post-upgrade

Stop service with

```
sudo service synda stop
```

As configuration files located in /etc/synda/sdt have been reinitialized
during upgrade, you need to re-enter your openid and password, as well as any
other parameter you may have set to a non-default value.

Note: you can use a diff program to compare post-upgrade configuration files
over pre-upgrade configuration files (from the backup).

Restore database from backup in /var/lib/synda/sdt (replace the existing file).

Run commands below as root to set group permission on Synda data :

```
find /srv/synda/sdt         -print0 | xargs -0 chown :synda
find /srv/synda/sdt -type d -print0 | xargs -0 chmod g+ws
```

Restart service with

```
sudo service synda restart
```
