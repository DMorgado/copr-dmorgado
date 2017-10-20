# copr-dmorgado

    https://copr.fedorainfracloud.org/coprs/<username>/<coprname>/package/<package_name>/status_image/last_build.png
    https://copr.fedorainfracloud.org/coprs/g/<group_name>/<coprname>/package/<package_name>/status_image/last_build.png


### My Repo is at:
https://copr.fedorainfracloud.org/coprs/dmorgado/myel7.repo/repo/epel-7/dmorgado-myel7.repo-epel-7.repo


```
[dmorgado-myel7.repo]
name=Copr repo for myel7.repo owned by dmorgado
baseurl=https://copr-be.cloud.fedoraproject.org/results/dmorgado/myel7.repo/epel-7-$basearch/
type=rpm-md
skip_if_unavailable=True
gpgcheck=1
gpgkey=https://copr-be.cloud.fedoraproject.org/results/dmorgado/myel7.repo/pubkey.gpg
repo_gpgcheck=0
enabled=1
enabled_metadata=1
```
