# How to set up storage in Azure used for migrating data into Documaster

ℹ️ Please take careful note of the sentences marked with 🔵 as you will need to provide this information to Documaster.

This page is documenting the different steps you need to do in order to create a Blob container in Azure that Documaster
can use to do batch processing of your data.

---

## Create an Azure Storage Account
Please see the [Azure documentation](https://learn.microsoft.com/en-us/azure/storage/common/storage-account-create?tabs=azure-portal)
on how you can create a storage account. The only requirement from Documaster is that creation of Blob Containers must be
possible within the storage account.

🔵 Take note of the **storage account name** and **resource group name**, which must be provided to Documaster.

### Recommendations
If you do not have any preferences for your storage account, we recommend to use the following settings:

- Require secure transfer for REST API operations
- Network Access: Disable public access and use private access
- Enable soft delete for blobs
- Enable soft delete for containers


## Create a Blob Container
In your newly created storage account, create a blob container. Please refer to [Azure's documentation](https://learn.microsoft.com/en-us/azure/storage/blobs/blob-containers-portal) on how to create and manage this resource. 

🔵 Take note of the **blob container name**, which must be provided to Documaster.


## Get the access key
In order for Documaster to be able to connect to the blob container, you must provide an access key to the storage account.
You can find this by going to your *storage account → Access keys* and copy one of the two keys. This is described
[here](https://learn.microsoft.com/nb-no/azure/storage/common/storage-account-keys-manage?tabs=azure-portal#view-account-access-keys).

🔵 Take note of the **storage account key**, which must be provided (securely) to Documaster.

## Summary

The following information must be provided to Documaster after the setup is complete:
- 🔵 Your subscription ID
- 🔵 Resource group (of the storage account)
- 🔵 Storage account name
- 🔵 Storage account key
- 🔵 Blob container name


---
# How to grant access to your storage account to Documaster

After you have created a storage account, Documaster will set up a private link from our virtual network to your storage
account. This link must be approved on your end, manually. This connection request can be found by going to the *storage
account resource → Networking → Private endpoint connections*. 

Once this request is approved, Documaster can access the data in the blob container using a private network connection.
