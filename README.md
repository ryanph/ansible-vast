# Ansible VAST Collection

A set of generated ansible modules for the VAST Management Service (VMS).
Modules are idempotent and support check_mode with unit tests run against VMS 4.7.
For documentation on module specific arguments refer to the documentation on your cluster located at https://VMS_IP/docs/.

## Requirements

Python [vastsdk](https://github.com/ryanph/vastsdk) library version 1.1.0

## Installing

```
pip3 install https://github.com/ryanph/vastsdk/releases/download/v1.1.0/vastsdk-python-1.1.0.tgz
ansible-galaxy install https://github.com/ryanph/ansible-vast/releases/download/v1.1.0/ryanph-vast-1.1.0.tar.gz
```

## Common Arguments

All modules use the following common self-descriptive arguments:

- *vms_hostname*: The hostname of the VMS instance
- *vms_username*: The username to authenticate with
- *vms_password*: The password to authenticate with
- *vms_verify_ssl*: Whether to verify SSL certificates

## Common Return Values

All modules return the following values:

- *resource*: The resource created or updated (view, viewpolicy etc)
- *changes*: The changes made to the resource (if applicable)
- *message*: The action performed by the module

## Module Summary

For full documentation refer to `ansible-doc` after installing the collection.
### ryanph.vast.groupquery

VAST Management Service (VMS) Group Query

#### Arguments
- *name*

#### Examples

```
    name: Lookup a group by name (groupquery)
    register: group_query_result
    ryanph.vast.groupquery:
      name: AllStaffAccounts
```
### ryanph.vast.user

VAST Management Service (VMS) User Management

#### Arguments
- *allow_create_bucket*
- *allow_delete_bucket*
- *name*
- *s3_superuser*
- *uid*

#### Examples

```
    name: Create a local User (user)
    register: s3_user
    ryanph.vast.user:
      name: s3_user
      state: present
      uid: 1000
```
```
    name: Delete a User (user)
    ryanph.vast.user:
      name: s3_user
      state: absent
```
### ryanph.vast.userquery

VAST Management Service (VMS) User Query

#### Arguments
- *name*

#### Examples

```
    name: Lookup a user by name (userquery)
    register: user_query_result
    ryanph.vast.userquery:
      name: vastdata
```
### ryanph.vast.view

VAST Management Service (VMS) View Management

#### Arguments
- *alias*
- *allow_s3_anonymous_access*
- *bucket*
- *bucket_owner*
- *create_dir*
- *nfs_interop_flags*
- *path*
- *policy_id*
- *protocols*
- *s3_locks*
- *s3_locks_retention_mode*
- *s3_versioning*
- *share*
- *share_acl*

#### Examples

```
    name: Create a Mixed Protocol View (view)
    ryanph.vast.view:
      path: /mixed
      policy_id: '{{ mixed_policy.resource.id }}'
      protocols:
      - SMB
      - NFS
      share: my_mixed_view
      share_acl:
        acl:
        - grantee: users
          is_sid: true
          perm: FULL
          sid_str: '{{ user_query_result.resource.sid }}'
        - grantee: groups
          is_sid: true
          perm: CHANGE
          sid_str: '{{ group_query_result.resource.sid }}'
        enabled: true
      state: present
```
```
    name: Create a Native S3 View (view)
    ryanph.vast.view:
      bucket: my-s3-view
      bucket_owner: s3_user
      path: /s3
      policy_id: '{{ s3_policy.resource.id }}'
      protocols:
      - S3
      state: present
```
```
    name: Create a NFS View (view)
    ryanph.vast.view:
      alias: /export/application
      path: /nfs
      policy_id: '{{ nfs_policy.resource.id }}'
      protocols:
      - NFS
      state: present
```
```
    name: Delete a View (view)
    ryanph.vast.view:
      path: /mixed
      state: absent
```
### ryanph.vast.viewpolicy

VAST Management Service (VMS) View Policy Management

#### Arguments
- *allowed_characters*
- *auth_source*
- *enable_listing_of_snapshot_dir*
- *enable_snapshot_lookup*
- *flavor*
- *gid_inheritance*
- *name*
- *nfs_all_squash*
- *nfs_case_insensitive*
- *nfs_no_squash*
- *nfs_posix_acl*
- *nfs_read_only*
- *nfs_read_write*
- *nfs_root_squash*
- *path_length*
- *protocols*
- *protocols_audit*
- *s3_visibility*
- *s3_visibility_groups*
- *smb_is_ca*
- *use_32bit_fileid*
- *vip_pools*

#### Examples

```
    name: Create a Mixed Protocol View Policy with SMB Auditing (viewpolicy)
    register: mixed_policy
    ryanph.vast.viewpolicy:
      auth_source: PROVIDERS
      flavor: MIXED_LAST_WINS
      name: mixed_policy
      nfs_read_only: []
      nfs_read_write:
      - 192.168.1.1
      protocols:
      - SMB
      protocols_audit:
        create_delete_files_dirs_objects: true
        log_full_path: true
        log_username: true
        modify_data_md: true
        read_data: true
      state: present
```
```
    name: Create a Native S3 View Policy (viewpolicy)
    register: s3_policy
    ryanph.vast.viewpolicy:
      allowed_characters: NPL
      auth_source: PROVIDERS
      flavor: S3_NATIVE
      name: s3_policy
      path_length: NPL
      state: present
```
```
    name: Create a NFS View Policy (viewpolicy)
    register: nfs_policy
    ryanph.vast.viewpolicy:
      allowed_characters: LCD
      auth_source: PROVIDERS
      flavor: NFS
      name: nfs_policy
      nfs_read_only: []
      nfs_read_write:
      - 192.168.0.0/24
      - 10.0.0.1
      path_length: LCD
      state: present
```
```
    name: Delete a View Policy (viewpolicy)
    register: nfs_policy
    ryanph.vast.viewpolicy:
      name: mixed_policy
      state: absent
```