# Ansible VAST Collection

A set of generated ansible modules for the VAST Management Service (VMS).
Modules are idempotent and support check_mode with unit tests run against VMS 4.7.
For documentation on module specific arguments refer to the documentation on your cluster located at https://VMS_IP/docs/.

## Requirements

Python [vastsdk](https://github.com/ryanph/vastsdk) library version 1.4.0

## Installing

```
pip3 install https://github.com/ryanph/vastsdk/releases/download/v1.4.0/vastsdk-python-1.4.0.tgz
ansible-galaxy collection install https://github.com/ryanph/ansible-vast/releases/download/v1.4.0/ryanph-vast-1.4.0.tar.gz
```

## Common Arguments

All modules use the following common self-descriptive arguments:

- *vms_hostname*: The hostname of the VMS instance
- *vms_username*: The username to authenticate with
- *vms_password*: The password to authenticate with
- *vms_verify_ssl*: Whether to verify SSL certificates
- *vms_auth_type*: Whether to use basic or token auth

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
- **name**: _Group Name (string)_

#### Examples

```
    name: Lookup a group by name (groupquery)
    ryanph.vast.groupquery:
      name: AllStaffAccounts
    register: group_query_result
```
### ryanph.vast.permissionrepair

VAST Management Service (VMS) Permission Repair

#### Arguments
- **target_path**: _The path to repair permissions on relative to the View (string)_
- **template_dir_path**: _The path to the directory template relative to the Template View (string)_
- **template_file_path**: _The path to the file template relative to the Template View (string)_
- **template_view_id**: _The ID of the View containing the template directory and file (integer)_

#### Examples

```
    name: Bulk Permission Repair (permissionrepair)
    ryanph.vast.permissionrepair:
      view_id: 1
      template_view_id: 2
      template_dir_path: template/template_dir
      template_file_path: template/template_file
      target_path: path/to/folder/to/repair
    register: repair_task
```
### ryanph.vast.protectedpath

VAST Management Service (VMS) Protected Path Management

#### Arguments
- **name**: _The name for the Protected Path (string)_
- **protection_policy_id**: _The ID of the Protection Policy to apply to the Protected Path (integer)_
- **source_dir**: _The Protected Path (string)_

#### Examples

```
    name: Create a Protected Path (protectedpath)
    ryanph.vast.protectedpath:
      name: example_protectedpath
      source_dir: /my_path
      protection_policy_id: '{{ protectionpolicy.resource.id }}'
      state: present
```
```
    name: Delete a Protected Path and wait for the background job to finish (protectedpath)
    ryanph.vast.protectedpath:
      source_dir: /my_path
      state: absent
    register: protectedpath
    until: protectedpath.resource is not defined
    retries: 10
    delay: 10
```
### ryanph.vast.protectionpolicy

VAST Management Service (VMS) Protection Policy Management

#### Arguments
- **clone_type**: _CLOUD_REPLICATION is S3 backup. LOCAL means local snapshots without replication. (string)_
- **frames**: _The schedule for snapshot creation, and the local and remote retention policies. (array)_
- **indestructible**: _Whether created snapshots should be indestructible (boolean)_
- **name**: _The name of the protection policy (string)_
- **prefix**: _The prefix to apply to snapshots taken by this policy (string)_

#### Examples

```
    name: Create a Protection Policy (protectionpolicy)
    ryanph.vast.protectionpolicy:
      name: example_policy
      prefix: example
      clone_type: LOCAL
      indestructible: false
      frames:
      - every: 1D
        start-at: '2020-01-01 18:00:00'
        keep-local: 2D
      - every: 1W
        start-at: '2020-01-01 18:00:00'
        keep-local: 1M
      state: present
    register: protectionpolicy
```
```
    name: Delete a Protection Policy and wait for the background job to finish (protectionpolicy)
    ryanph.vast.protectionpolicy:
      name: example_policy
      state: absent
    register: protectedpath
    until: protectedpath.resource is not defined
    retries: 10
    delay: 10
```
### ryanph.vast.quota

VAST Management Service (VMS) Quota Management

#### Arguments
- **create_dir**: _Whether to create the path if it does not already exist (boolean)_
- **hard_limit**: _The hard limit in bytes (integer)_
- **hard_limit_inodes**: _The hard file and directory count limit (integer)_
- **name**: _A name describing the quota (string)_
- **path**: _The path the quota applies to (string)_
- **soft_limit**: _The quota soft limit in bytes (integer)_
- **soft_limit_inodes**: _The soft file and directory count limit (integer)_

#### Examples

```
    name: Create a quota (quota)
    ryanph.vast.quota:
      name: my_quota
      path: /mixed
      create_dir: false
      state: present
      hard_limit: '10000'
```
```
    name: Delete a quota (quota)
    ryanph.vast.quota:
      name: my_quota
      state: absent
```
### ryanph.vast.taskquery

VAST Management Service (VMS) Async Task Query

#### Arguments
- **id**: _The ID of the task (integer)_

#### Examples

```
    name: Wait for Bulk Permission Repair to complete (taskquery)
    ryanph.vast.taskquery:
      id: '{{ repair_task.resource.async_task.id }}'
    register: task_status
    until:
    - task_status.resource.state != "RUNNING"
    retries: 900
    delay: 15
```
### ryanph.vast.user

VAST Management Service (VMS) User Management

#### Arguments
- **allow_create_bucket**: _Whether the user is permitted to create S3 buckets (boolean)_
- **allow_delete_bucket**: _Whether the user is permitted to delete S3 buckets (boolean)_
- **name**: _The name of the user (username) (string)_
- **s3_superuser**: _Whether the user is an S3 Superuser and permitted to bypass ACLs (boolean)_
- **uid**: _Numeric UID for the user (integer)_

#### Examples

```
    name: Create a local User (user)
    ryanph.vast.user:
      name: s3_user
      uid: 1000
      state: present
    register: s3_user
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
- **name**: _The name of the user (username) (string)_

#### Examples

```
    name: Lookup a user by name (userquery)
    ryanph.vast.userquery:
      name: vastdata
    register: user_query_result
```
### ryanph.vast.view

VAST Management Service (VMS) View Management

#### Arguments
- **alias**: _Alias for NFS export, must start with / and only ASCII characters are allowed. If configured, this supersedes the exposed NFS export path (string)_
- **allow_s3_anonymous_access**: _Allow S3 anonymous access (boolean)_
- **bucket**: _S3 Bucket name (string)_
- **bucket_owner**: _Owner of the S3 bucket (string)_
- **create_dir**: _Create directory if it does not exist (boolean)_
- **nfs_interop_flags**: _Indicates whether the view should support simultaneous access to NFS3/NFS4/SMB protocols (string)_
- **path**: _The Element Store path exposed by the view. Begin with a forward slash. Do not include a trailing slash (string)_
- **policy_id**: _ID of the View Policy to apply (integer)_
- **protocols**: _Protocols the view will be accessible via (array)_
- **s3_locks**: _S3 Object Locking enabled on S3 bucket. (boolean)_
- **s3_locks_retention_mode**: _S3 Locks retention mode (string)_
- **s3_versioning**: _S3 Versioning enabled on S3 bucket (boolean)_
- **share**: _Name of the SMB share (string)_
- **share_acl**: _SMB Share Level ACL (object)_

#### Examples

```
    name: Create a Mixed Protocol View (view)
    ryanph.vast.view:
      path: /mixed
      share: my_mixed_view
      policy_id: '{{ mixed_policy.resource.id }}'
      protocols:
      - SMB
      - NFS
      share_acl:
        enabled: true
        acl:
        - perm: FULL
          grantee: users
          sid_str: '{{ user_query_result.resource.sid }}'
          is_sid: true
        - perm: CHANGE
          grantee: groups
          sid_str: '{{ group_query_result.resource.sid }}'
          is_sid: true
      state: present
```
```
    name: Create a Native S3 View (view)
    ryanph.vast.view:
      path: /s3
      bucket: my-s3-view
      policy_id: '{{ s3_policy.resource.id }}'
      bucket_owner: s3_user
      protocols:
      - S3
      state: present
```
```
    name: Create a NFS View (view)
    ryanph.vast.view:
      path: /nfs
      alias: /export/application
      policy_id: '{{ nfs_policy.resource.id }}'
      protocols:
      - NFS
      state: present
    register: nfs_view
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
- **allowed_characters**: _The permitted character set for files stored in the view (string)_
- **auth_source**: _Source of group memberships for authenticated users (string)_
- **enable_listing_of_snapshot_dir**: _Whether the .snapshot directory is visible (boolean)_
- **enable_snapshot_lookup**: _Whether the .snapshot directory is accessible (boolean)_
- **flavor**: _How file and directory permissions are applied (string)_
- **gid_inheritance**: _How files receive their owning group when created (string)_
- **name**: _The unique name of the View Policy (string)_
- **nfs_all_squash**: _List of IP addresses or subnets that should have the all remote users mapped to 'nobody' (array)_
- **nfs_case_insensitive**: _Case insensitivity for NFS clients (boolean)_
- **nfs_no_squash**: _List of IP addresses or subnets that should not have any remote user mapping applied (array)_
- **nfs_posix_acl**: _Support for extended POSIX ACLs for NFSv3 clients (boolean)_
- **nfs_read_only**: _List of IP addresses or subnets that have Read Only access via NFS (array)_
- **nfs_read_write**: _List of IP addresses or subnets that have Read and Write access via NFS (array)_
- **nfs_root_squash**: _List of IP addresses or subnets that should have the remote root user mapped to 'nobody' (array)_
- **path_length**: _The maximum allowed path length for files stored in the view (string)_
- **protocols**: _Protocols to audit (array)_
- **protocols_audit**: _Protocol audit settings (object)_
- **s3_visibility**: _Users with permission to list buckets that are created using this policy (array)_
- **s3_visibility_groups**: _Groups with permission to list buckets that are created using this policy (array)_
- **smb_is_ca**: _Enables SMB Continuous Availability (boolean)_
- **use_32bit_fileid**: _Support legacy 32-bit applications running over NFS (boolean)_
- **vip_pools**: _An array of VIP Pool Identifiers that associated views will be accessible from (array)_

#### Examples

```
    name: Create a Mixed Protocol View Policy with SMB Auditing (viewpolicy)
    ryanph.vast.viewpolicy:
      name: mixed_policy
      flavor: MIXED_LAST_WINS
      auth_source: PROVIDERS
      nfs_read_write:
      - 192.168.1.1
      nfs_read_only: []
      protocols:
      - SMB
      protocols_audit:
        read_data: true
        log_username: true
        log_full_path: true
        modify_data_md: true
        create_delete_files_dirs_objects: true
      state: present
    register: mixed_policy
```
```
    name: Create a Native S3 View Policy (viewpolicy)
    ryanph.vast.viewpolicy:
      name: s3_policy
      flavor: S3_NATIVE
      auth_source: PROVIDERS
      allowed_characters: NPL
      path_length: NPL
      state: present
    register: s3_policy
```
```
    name: Create a NFS View Policy (viewpolicy)
    ryanph.vast.viewpolicy:
      name: nfs_policy
      flavor: NFS
      auth_source: PROVIDERS
      allowed_characters: LCD
      path_length: LCD
      nfs_read_only: []
      nfs_read_write:
      - 192.168.0.0/24
      - 10.0.0.1
      state: present
    register: nfs_policy
```
```
    name: Delete a View Policy (viewpolicy)
    ryanph.vast.viewpolicy:
      name: mixed_policy
      state: absent
    register: nfs_policy
```
### ryanph.vast.vippoolsquery

VAST Management Service (VMS) VIP Pools Query

#### Arguments
- **name**: _The Name of the VIP Pool (string)_

#### Examples

```
    name: Look up a VIP Pool (vippoolsquery)
    ryanph.vast.vippoolsquery:
      name: campus
    register: vippools_query_result
```
