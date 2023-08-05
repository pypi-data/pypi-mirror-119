# pysecretserver
Python API client library for [SecretServer] (https://thycotic.com/products/secret-server/)

## Quick Start

### Installation

- Clone this git repository to a working directory.
- Setup and activate a `venv` if desired.
- Install the package using `pip` from the working directory.

  `pip install .`

The working directory can be removed if desired.

### Usage

To begin, import pysecretserver and instantiate the API. For example:

```
>>> import pysecretserver
>>> ss = pysecretserver.api(
    site='https://daisyops.secretservercloud.eu/',
    username='flex_api',
    password='SuperSecretPassword'
)
```

Instantiating the API automatically authenticates the session and stores the
Bearer token within the instance.

The token has an TTL of 5 minutes. This should be fine when this module is
used in scripts but the token may expire during an extended interactive
session. The API instance has an `update_auth_token()` method which can be
used to renew the token. For example:

```
>>> ss.token
'AgIUG-ZX-WerVLj4b6pLrd3Ho_F3iZAAtnuiLKrLVB3VFcHgloK-yfuCN2qHQM10JDeBjwuUwvBT_H749Tsa50fUkFOaIVPyMZOGOYBasMHQoG2phXyWzRF_QMjdbGBdJWttXNY67frKiD-qRw9PrHdzFNG4ZjVXPsIZ9iz_Rlx1arecmQ7BNv4tq-RH3Ryh0vsFL9x2aM2fandtUmpM6YOckCL9Gno7gQJuGRaJFI4KAwBSEsbeRaKh5MlmdasAFd_6S9jG9Cyp-Dhvw3a2pybO_jZuhJaJ2lggrOm7H1oFs9dPJClzzKCDTIG_wkYW7fsr5qsWeWhUDuyO9esCpnKSFrMig9XKhdLZ_JJCFZGYHXlPACNWlkSoIcwmDNZOflsz1G2KQcRn0n5S7R9KYS-z2AOWvfBP_t6-Ue68geUQbT3OH-YB3GMULSG4GnXtIw-T_pjTL7T5SZ_PslJWUb1NvsevbsVBUzUbVt0rgFUXcuk7rH5wSe5GjOmmyIffFeUG-NtYfWy1alUh4MGWnfXOCX9yrVDODtbS0rIwYgLivF6SJGMyNag8bxeRMVZPe8cVbQOuCX2BdVgCDehqgQLk'
>>> ss.update_auth_token()
>>> ss.token
'AgJMttsOGDJIWf6kw0ywt8e4cnzgZzMJdvi_wSs6DUimEHHRmTnCmN2u_rEB8wyt_pYjxnm8eRev8ZuI28THYp5PHjVz0Y_40xaQEKuS5O_o5j7xZZz9SEy0VVnoi1aVlGd2pz3YPFWp_3xHmWCAMtlycjvHFX6_c8WtWBAp6H-j_OM7ylAOsXIZMt1i0Fj70La1X7xtndxvOLTRaTROCBX9xuBLTfZlZOXYRQ421CpyRTMbHbAOe4sGeogHSOs9whCEg3UnqmWHfUSsyCXP9UihF0mZlcCz6FCgpDIxcBgXSKyvsAhQ4GSp2k69urmWbPecb3W81ubcLA7DWwCcUDaSHgPWf0TmYZCHyCIdw4-oOG0fJu9G7bY_x2YoljlXz2YMx_w0dkoXNu500zl4s3mUcoBSJedGMyCbHkRJNG4iIR5OKz1LelnZ9Y8I79fsQ8_ZgsH1wwh107xvDvny7_c5JfyRfOnNz8mgrshKGBduHH5TH520ZnTR135jhGZOIKzdySUx5Aq10kLQ6OUVgBAk2VBb8-cvHUXaw05YglcJxwdy49fiqizh4VqoT7lNrdlcRVLmkccg_kZmdb0cSjGP'
```

An instance of the API exposes 3 sub-classes:
- `Secrets`
- `Folders`
- `Metadata`

`Secrets` and `Folders` are both child classes of a generic `Items` class. They
provide the following common methods:
- `get_item(item_id)`: Retrieve an item by ID
- `search_item(filters={}, params={})`: Retrieve a list of items matching the specified filters
- `create_item(data={})`: Create a new item using the parameters specified in the `data` `dict()`
- `update_item(item_id, data={})`: Update (PUT) an item
- `delete_item(item_id)`: Delete an item
- `get_item_metadata(item_id, meta_field_id=None)`: Retrieve the metadata defined on an item
- `create_item_metadata(item_id, data={})`: Create a new metadata field using the parameters specified in the `data` `dict()`
- `update_item_metadata(item_id, data={})`: Update an exsting metadata field using the parameters specified in the `data` `dict()`
- `delete_item_metadata(item_id, metadata_id)`: Delete a metadata field from the item

Metadata provides the following methods:
- `get_fields()`: Retrieve a all metadata fields as a `list()` of `dict()`
- `get_field_sections(item_id)`: Retrieve a list of field sections for an item.

Refer to the Thycotic Secret Server documentation for details of the required parameters for
filters, parameters and create/update data at:
https://daisyops.secretservercloud.eu/documents/restapi/TokenAuth

## Example Usage

Retrieve a Secret:
```
>>> import pysecretserver
>>> ss = pysecretserver.api(
    site='https://daisyops.secretservercloud.eu/',
    username='flex_api',
    password='SuperSecretPassword'
)
>>> ss.Secrets.get_item(2610)
{'id': 2610, 'name': 'New XXX UPDATED Secret Name', 'secretTemplateId': 6007, 'folderId': 1809, 'active': True, 'items': [{'itemId': 24052, 'fileAttachmentId': None, 'filename': None, 'itemValue': 'Create Test', 'fieldId': 108, 'fieldName': 'Machine', 'slug': 'machine', 'fieldDescription': 'The Server or Location of the Unix Machine.', 'isFile': False, 'isNotes': False, 'isPassword': False}, {'itemId': 24053, 'fileAttachmentId': None, 'filename': None, 'itemValue': 'root', 'fieldId': 111, 'fieldName': 'Username', 'slug': 'username', 'fieldDescription': 'The Unix Machine Username.', 'isFile': False, 'isNotes': False, 'isPassword': False}, {'itemId': 24054, 'fileAttachmentId': None, 'filename': None, 'itemValue': 'newpassword', 'fieldId': 110, 'fieldName': 'Password', 'slug': 'password-1', 'fieldDescription': 'The password of the Unix Machine.', 'isFile': False, 'isNotes': False, 'isPassword': True}, {'itemId': 24055, 'fileAttachmentId': None, 'filename': None, 'itemValue': 'Initial Notes Value', 'fieldId': 109, 'fieldName': 'Notes', 'slug': 'notes', 'fieldDescription': 'Any additional notes.', 'isFile': False, 'isNotes': True, 'isPassword': False}, {'itemId': 24056, 'fileAttachmentId': None, 'filename': None, 'itemValue': '*** Not Valid For Display ***', 'fieldId': 189, 'fieldName': 'Private Key', 'slug': 'private-key', 'fieldDescription': 'The SSH private key.', 'isFile': True, 'isNotes': False, 'isPassword': False}, {'itemId': 24057, 'fileAttachmentId': None, 'filename': None, 'itemValue': '', 'fieldId': 190, 'fieldName': 'Private Key Passphrase', 'slug': 'private-key-passphrase', 'fieldDescription': 'The passphrase for decrypting the SSH private key.', 'isFile': False, 'isNotes': False, 'isPassword': True}], 'launcherConnectAsSecretId': -1, 'checkOutMinutesRemaining': 0, 'checkedOut': False, 'checkOutUserDisplayName': '', 'checkOutUserId': -1, 'isRestricted': False, 'isOutOfSync': False, 'outOfSyncReason': '', 'autoChangeEnabled': False, 'autoChangeNextPassword': None, 'requiresApprovalForAccess': False, 'requiresComment': False, 'checkOutEnabled': False, 'checkOutIntervalMinutes': -1, 'checkOutChangePasswordEnabled': False, 'accessRequestWorkflowMapId': -1, 'proxyEnabled': False, 'sessionRecordingEnabled': False, 'restrictSshCommands': False, 'allowOwnersUnrestrictedSshCommands': False, 'isDoubleLock': False, 'doubleLockId': -1, 'enableInheritPermissions': True, 'passwordTypeWebScriptId': -1, 'siteId': 1, 'enableInheritSecretPolicy': False, 'secretPolicyId': -1, 'lastHeartBeatStatus': 'Pending', 'lastHeartBeatCheck': '0001-01-01T00:00:00', 'failedPasswordChangeAttempts': 0, 'lastPasswordChangeAttempt': '0001-01-01T00:00:00', 'secretTemplateName': 'Unix Account (SSH)', 'responseCodes': [], 'webLauncherRequiresIncognitoMode': False}
```

Retreive Metadata for a folder:
```
>>> ss.Folders.get_item_metadata(1814)
[{'metadataItemDataId': 1, 'metadataFieldTypeName': None, 'metadataFieldDataType': 'String', 'metadataType': 'Folder', 'metadataTypeName': None, 'itemId': 1814, 'metadataFieldId': 1, 'metadataFieldName': 'Test', 'metadataFieldSectionId': 1, 'metadataFieldSectionName': 'Test', 'createUserId': 34, 'createUserName': 'Christopher Kay', 'createDateTime': '2021-05-19T11:41:03.983', 'sortOrder': None, 'valueString': 'Test', 'valueBit': None, 'valueNumber': None, 'valueDateTime': None, 'valueInt': None, 'valueUserDisplayName': None}, {'metadataItemDataId': 2, 'metadataFieldTypeName': None, 'metadataFieldDataType': 'String', 'metadataType': 'Folder', 'metadataTypeName': None, 'itemId': 1814, 'metadataFieldId': 2, 'metadataFieldName': 'Test 2', 'metadataFieldSectionId': 1, 'metadataFieldSectionName': 'Test', 'createUserId': 34, 'createUserName': 'Christopher Kay', 'createDateTime': '2021-05-19T12:53:19.047', 'sortOrder': None, 'valueString': 'Test 2', 'valueBit': None, 'valueNumber': None, 'valueDateTime': None, 'valueInt': None, 'valueUserDisplayName': None}]
```

Create a folder:
```
>>> ss.Folders.create_item({'folderName': 'Test Folder', 'folderTypeId': 1, 'parentFolderId': 1814})
{'id': 1928, 'folderName': 'Test Folder', 'folderPath': '\\Flex_API_Testing\\Daisy Group\\Test Folder', 'parentFolderId': 1814, 'folderTypeId': 1, 'secretPolicyId': -1, 'inheritSecretPolicy': True, 'inheritPermissions': True, 'childFolders': None, 'secretTemplates': None}
```

Update a folder:
```
>>> folder = ss.Folders.get_item(1928)
>>> folder.update({'folderName':'Updated Test Folder'})
>>> ss.Folders.update_item(1928, folder)
{'id': 1831, 'folderName': 'Extra Double Secret 009', 'folderPath': '\\Flex_API_Testing\\Daisy Group 101\\Extra Double Secret 009', 'parentFolderId': 1821, 'folderTypeId': 1, 'secretPolicyId': -1, 'inheritSecretPolicy': True, 'inheritPermissions': True, 'childFolders': None, 'secretTemplates': None}
```

Create a metadata field on a Folder:
```
>>> data = {
...     "data": {
...         "fieldDataType": "string",
...         "metadataFieldName": "Customer Code",
...         "metadataFieldSectionName": "Customer Details",
...         "valueString": "TST",
...     }
... }
>>> ss.Folders.create_item_metadata(1928, data)
{'metadataItemDataId': 25, 'itemId': 1928, 'metadataFieldId': 5, 'sortOrder': None, 'valueString': 'TST', 'valueBit': None, 'valueInt': None, 'valueNumber': None, 'valueDateTime': None, 'valueUserDisplayName': None, 'createUserId': 232, 'createUserName': None, 'createDateTime': '2021-09-01T13:11:57.4384354Z', 'metadataTypeName': None, 'metadataFieldName': None, 'metadataFieldTypeId': None, 'metadataFieldTypeName': None, 'metadataFieldSectionId': 3, 'metadataFieldSectionName': None}
```

Update a metadata field on a Folder:
```
>>> data = {
...     'data':{
...         'metadataItemDataId':25,
...         'valueString': {
...             'dirty':True,
...             'value': 'XXX'
...         }
...     }
... }
>>> ss.Folders.update_item_metadata(1928, data)
{'metadataItemDataId': 25, 'itemId': 1928, 'metadataFieldId': 5, 'sortOrder': None, 'valueString': 'XXX', 'valueBit': None, 'valueInt': None, 'valueNumber': None, 'valueDateTime': None, 'valueUserDisplayName': None, 'createUserId': 232, 'createUserName': 'flex_api', 'createDateTime': '2021-09-01T13:14:31.2', 'metadataTypeName': None, 'metadataFieldName': 'Customer Code', 'metadataFieldTypeId': 1, 'metadataFieldTypeName': None, 'metadataFieldSectionId': 3, 'metadataFieldSectionName': 'Customer Details'}
```

Delete a metadata field on a Folder:
```
>>> ss.Folders.delete_item_metadata(1929, 25)
{'success': True}
```

Delete a folder:
```
>>> ss.Folders.delete_item(1928)
{'id': 1928, 'objectType': 'Folder', 'responseCodes': []}
```

Retrieve a list of all available Metadata fields:
```
>>> ss.Metadata.get_fields()
[{'metadataFieldId': 3, 'metadataFieldName': 'Secret Test', 'defaultSortOrder': None, 'metadataFieldSectionId': 2, 'fieldDataType': 'String', 'metadataFieldSectionName': 'Secret Section'}, {'metadataFieldId': 4, 'metadataFieldName': 'Secret Test 2', 'defaultSortOrder': None, 'metadataFieldSectionId': 2, 'fieldDataType': 'String', 'metadataFieldSectionName': 'Secret Section'}, {'metadataFieldId': 1, 'metadataFieldName': 'Test', 'defaultSortOrder': None, 'metadataFieldSectionId': 1, 'fieldDataType': 'String', 'metadataFieldSectionName': 'Test'}, {'metadataFieldId': 2, 'metadataFieldName': 'Test 2', 'defaultSortOrder': None, 'metadataFieldSectionId': 1, 'fieldDataType': 'String', 'metadataFieldSectionName': 'Test'}]
```

Retrieve all secrets in a folder:
```
>>> ss.Secrets.search_item(filters={'filter.folderId': 1809})
[{'id': 2608, 'name': 'New Updated Secret Name', 'secretTemplateId': 6007, 'secretTemplateName': 'Unix Account (SSH)', 'folderId': 1809, 'siteId': 1, 'active': True, 'checkedOut': False, 'isRestricted': False, 'isOutOfSync': False, 'outOfSyncReason': '', 'lastHeartBeatStatus': 'Pending', 'lastPasswordChangeAttempt': '0001-01-01T00:00:00', 'responseCodes': None, 'lastAccessed': None, 'extendedFields': None, 'checkOutEnabled': False, 'autoChangeEnabled': False, 'doubleLockEnabled': False, 'requiresApproval': False, 'requiresComment': False, 'inheritsPermissions': True, 'hidePassword': False, 'createDate': '2021-05-18T06:57:38.433', 'daysUntilExpiration': 26}, {'id': 2610, 'name': 'New XXX UPDATED Secret Name', 'secretTemplateId': 6007, 'secretTemplateName': 'Unix Account (SSH)', 'folderId': 1809, 'siteId': 1, 'active': True, 'checkedOut': False, 'isRestricted': False, 'isOutOfSync': False, 'outOfSyncReason': '', 'lastHeartBeatStatus': 'Pending', 'lastPasswordChangeAttempt': '0001-01-01T00:00:00', 'responseCodes': None, 'lastAccessed': None, 'extendedFields': None, 'checkOutEnabled': False, 'autoChangeEnabled': False, 'doubleLockEnabled': False, 'requiresApproval': False, 'requiresComment': False, 'inheritsPermissions': True, 'hidePassword': False, 'createDate': '2021-05-18T10:12:41.18', 'daysUntilExpiration': 26}, {'id': 2620, 'name': 'Secret 007', 'secretTemplateId': 6007, 'secretTemplateName': 'Unix Account (SSH)', 'folderId': 1809, 'siteId': 1, 'active': True, 'checkedOut': False, 'isRestricted': False, 'isOutOfSync': False, 'outOfSyncReason': '', 'lastHeartBeatStatus': 'Pending', 'lastPasswordChangeAttempt': '0001-01-01T00:00:00', 'responseCodes': None, 'lastAccessed': None, 'extendedFields': None, 'checkOutEnabled': False, 'autoChangeEnabled': False, 'doubleLockEnabled': False, 'requiresApproval': False, 'requiresComment': False, 'inheritsPermissions': True, 'hidePassword': False, 'createDate': '2021-05-21T08:37:11.22', 'daysUntilExpiration': 29}, {'id': 2621, 'name': 'Secret 008', 'secretTemplateId': 6007, 'secretTemplateName': 'Unix Account (SSH)', 'folderId': 1809, 'siteId': 1, 'active': True, 'checkedOut': False, 'isRestricted': False, 'isOutOfSync': False, 'outOfSyncReason': '', 'lastHeartBeatStatus': 'Pending', 'lastPasswordChangeAttempt': '0001-01-01T00:00:00', 'responseCodes': None, 'lastAccessed': None, 'extendedFields': None, 'checkOutEnabled': False, 'autoChangeEnabled': False, 'doubleLockEnabled': False, 'requiresApproval': False, 'requiresComment': False, 'inheritsPermissions': True, 'hidePassword': False, 'createDate': '2021-05-21T08:45:17.293', 'daysUntilExpiration': 29}]
```

Search for folders by folder name:
```
>>> ss.Folders.search_item(filters={'filter.folderName':'Daisy Group'})
[{'id': 1814, 'folderName': 'Daisy Group', 'folderPath': '\\Flex_API_Testing\\Daisy Group', 'parentFolderId': 1809, 'folderTypeId': 1, 'secretPolicyId': -1, 'inheritSecretPolicy': True, 'inheritPermissions': True}, {'id': 1821, 'folderName': 'Daisy Group 101', 'folderPath': '\\Flex_API_Testing\\Daisy Group 101', 'parentFolderId': 1809, 'folderTypeId': 1, 'secretPolicyId': -1, 'inheritSecretPolicy': True, 'inheritPermissions': True}, {'id': 1831, 'folderName': 'Extra Double Secret 009', 'folderPath': '\\Flex_API_Testing\\Daisy Group 101\\Extra Double Secret 009', 'parentFolderId': 1821, 'folderTypeId': 1, 'secretPolicyId': -1, 'inheritSecretPolicy': True, 'inheritPermissions': True}, {'id': 1809, 'folderName': 'Flex_API_Testing', 'folderPath': '\\Flex_API_Testing', 'parentFolderId': -1, 'folderTypeId': 1, 'secretPolicyId': -1, 'inheritSecretPolicy': False, 'inheritPermissions': False}, {'id': 1830, 'folderName': 'Folder 007', 'folderPath': '\\Flex_API_Testing\\Daisy Group 101\\Folder 007', 'parentFolderId': 1821, 'folderTypeId': 1, 'secretPolicyId': -1, 'inheritSecretPolicy': True, 'inheritPermissions': True}]
```

Create a secret:
```
>>> ss.Secrets.create_item({
...     "name": "Secret 010",
...     "folderId": 1831,
...     "secretTemplateId": 6007,
...     "siteId": 1,
...     'items': [
...         {
...             'fieldId': 108,
...             'itemValue': 'Create 007 Test',
...         },
...         {
...             'fieldId': 111,
...             'itemValue': 'root',
...         },
...         {
...             'fieldId': 110,
...             'itemValue': 'newpassword',
...         },
...         {
...             'fieldId': 109,
...             'itemValue': 'Initial Notes Value',
...             'slug': 'notes'
...         },
...         {
...             'fieldId': 189,
...             'itemValue': '*** Not Valid For Display ***',
...         },
...         {
...             'fieldId': 190,
...             'itemValue': '',
...         }
...     ],
... })
{'id': 2623, 'name': 'Secret 010', 'secretTemplateId': 6007, 'folderId': 1831, 'active': True, 'items': [{'itemId': 24216, 'fileAttachmentId': None, 'filename': None, 'itemValue': 'Create 007 Test', 'fieldId': 108, 'fieldName': 'Machine', 'slug': 'machine', 'fieldDescription': 'The Server or Location of the Unix Machine.', 'isFile': False, 'isNotes': False, 'isPassword': False}, {'itemId': 24217, 'fileAttachmentId': None, 'filename': None, 'itemValue': 'root', 'fieldId': 111, 'fieldName': 'Username', 'slug': 'username', 'fieldDescription': 'The Unix Machine Username.', 'isFile': False, 'isNotes': False, 'isPassword': False}, {'itemId': 24218, 'fileAttachmentId': None, 'filename': None, 'itemValue': 'newpassword', 'fieldId': 110, 'fieldName': 'Password', 'slug': 'password-1', 'fieldDescription': 'The password of the Unix Machine.', 'isFile': False, 'isNotes': False, 'isPassword': True}, {'itemId': 24219, 'fileAttachmentId': None, 'filename': None, 'itemValue': 'Initial Notes Value', 'fieldId': 109, 'fieldName': 'Notes', 'slug': 'notes', 'fieldDescription': 'Any additional notes.', 'isFile': False, 'isNotes': True, 'isPassword': False}, {'itemId': 24220, 'fileAttachmentId': 5, 'filename': 'Private Key', 'itemValue': '*** Not Valid For Display ***', 'fieldId': 189, 'fieldName': 'Private Key', 'slug': 'private-key', 'fieldDescription': 'The SSH private key.', 'isFile': True, 'isNotes': False, 'isPassword': False}, {'itemId': 24221, 'fileAttachmentId': None, 'filename': None, 'itemValue': '', 'fieldId': 190, 'fieldName': 'Private Key Passphrase', 'slug': 'private-key-passphrase', 'fieldDescription': 'The passphrase for decrypting the SSH private key.', 'isFile': False, 'isNotes': False, 'isPassword': True}], 'launcherConnectAsSecretId': -1, 'checkOutMinutesRemaining': 0, 'checkedOut': False, 'checkOutUserDisplayName': '', 'checkOutUserId': 0, 'isRestricted': False, 'isOutOfSync': False, 'outOfSyncReason': '', 'autoChangeEnabled': False, 'autoChangeNextPassword': None, 'requiresApprovalForAccess': False, 'requiresComment': False, 'checkOutEnabled': False, 'checkOutIntervalMinutes': -1, 'checkOutChangePasswordEnabled': False, 'accessRequestWorkflowMapId': -1, 'proxyEnabled': False, 'sessionRecordingEnabled': False, 'restrictSshCommands': False, 'allowOwnersUnrestrictedSshCommands': False, 'isDoubleLock': False, 'doubleLockId': 0, 'enableInheritPermissions': True, 'passwordTypeWebScriptId': -1, 'siteId': 1, 'enableInheritSecretPolicy': False, 'secretPolicyId': -1, 'lastHeartBeatStatus': 'Pending', 'lastHeartBeatCheck': '0001-01-01T00:00:00', 'failedPasswordChangeAttempts': 0, 'lastPasswordChangeAttempt': '0001-01-01T00:00:00', 'secretTemplateName': 'Unix Account (SSH)', 'responseCodes': [], 'webLauncherRequiresIncognitoMode': False}
```

Delete a secret:
```
>>> ss.Secrets.delete_item(2621)
{'id': 2621, 'objectType': 'Secret', 'responseCodes': []}
```
