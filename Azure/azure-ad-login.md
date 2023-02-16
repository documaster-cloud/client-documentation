# Setting up Azure AD applications for Documaster

ℹ️  Please take careful note of the sentences marked  with 🔵 as you will need to provide this information to Documaster.

---

## 1. Azure AD application
### Create the application (app registration)

Go to *Azure Active Directory → App registrations → New Application registration* ( [🔗 Portal link](https://portal.azure.com/#view/Microsoft_AAD_IAM/ActiveDirectoryMenuBlade/~/RegisteredApps) )

<img width="1105" alt="new-app-1" src="https://user-images.githubusercontent.com/40164824/215485412-a05bd67a-f605-4c8f-bb77-4f5b5f0d6718.png">

#### Create the new application with the following information:
1. **Name:** `Your chosen application name`
2. **Application type:** Web
3. **Redirect URI:** `https://<CUSTOMER_NAME>.documaster.cloud/login` (e.g. if your company name is "Example" it would be `https://example.documaster.cloud/login`)
4. Click Register

<img width="830" alt="new-app-2" src="https://user-images.githubusercontent.com/40164824/215747489-543fc4db-1aba-4038-b4e8-f9b5a4f38fbd.png">


### Retrieve Application information
🔵 Take note of the **Application (client) ID** and the **Directory (tenant) ID** and provide the information to Documaster.

<img width="732" alt="client-id" src="https://user-images.githubusercontent.com/40164824/215748200-45553bf5-d971-4e90-a125-cefee78732fe.png">


### Create a new Key (client secret)
⚠️ Key values are only visible right after their creation.

Inside your newly created App registration, go to *Certificates & secrets → New client secret*
1. **Description:** Dcoumaster Login
2. **Expires:** 730 days (24 months)
3. Click Save

🔵 Take note of the generated key **value** (which is used as Client Secret). Note that this is not the "Secret ID".

<img width="1301" alt="client-secret" src="https://user-images.githubusercontent.com/40164824/215748783-b809fd68-ebbe-4490-b64e-f04e1c5ff2c9.png">


### Grant permissions to retrieve user groups
Inside your newly created App registration, go to *Manifest → Set groupMembershipClaims to «All» → Save*

<img width="748" alt="membership-claim" src="https://user-images.githubusercontent.com/40164824/215750429-12de4539-2a2b-40d9-9b6d-4eef75f4f2b4.png">


### Grant API permission
Inside your newly created App registration, go to *API permissions → Add a permission → Microsoft Graph* 

<img width="2491" alt="permissions" src="https://user-images.githubusercontent.com/40164824/215750383-47dbc292-6ec5-49f0-85fb-7f45696393c5.png">

#### Click **Delegated permissions** and check off the following permissions:
- **openid** (Sign users in)
- **profile** (View users’ basic profile)
- **User.Read** (Sign in and read user profile) - this might be checked off by default

→ Add permissions

<img width="780" alt="delegated-permissions-1" src="https://user-images.githubusercontent.com/40164824/215494261-30bea363-51af-4a7c-9e6a-2478c4f9e85b.png">
<img width="780" alt="delegated-permissions-2" src="https://user-images.githubusercontent.com/40164824/215494371-c2a80c32-5a05-4e70-bcbf-0c70e67913cf.png">


#### Click **Application Permissions** and check off the following permissions:
- Group.Read.All (Read all groups)
- User.Read.All (Read all users’ full profiles)

→ Add permissions

<img width="780" alt="app-permissions-1" src="https://user-images.githubusercontent.com/40164824/215496260-256f7af8-2a73-48c2-8397-35a32f6490e5.png">
<img width="780" alt="app-permissions-2" src="https://user-images.githubusercontent.com/40164824/215496379-f1fbb76c-e2bf-48e1-9ba3-37a0dc3def81.png">


#### Grant admin consent → Yes (requires administrative privileges)
<img width="1542" alt="admin-consent" src="https://user-images.githubusercontent.com/40164824/215750718-4ea399ff-2e5d-49fd-92d8-f40bcf3fc7ba.png">


### **Add login and logout URLs**
Inside your newly created App registration, go to *Authentication* 

→ Under the Redirect URIs add `https://<NAME>.documaster.cloud/bff/login`

→ Under Logout URL add `https://<NAME>.documaster.cloud/logout` 

→ Save

<img width="1291" alt="login-logout" src="https://user-images.githubusercontent.com/40164824/215751385-891aabe7-8ad6-4994-afa5-68914a859e6c.png">


### **Allow ID Tokens in Implicit Grant**
Inside your newly created App registration, go to *Authentication* → Under the Implicit Grant toggle «ID Tokens» → Save*

<img width="734" alt="id-token" src="https://user-images.githubusercontent.com/40164824/215499040-f27e47aa-cab2-450e-b009-706b01822eb9.png">

---
## 2. Administration user group
When setting up a Documaster instance with Azure AD, we require an admin group. 

### Create the group
Go to *Azure Active Directory → Groups → New Group* ( [🔗 Portal link](https://portal.azure.com/#view/Microsoft_AAD_IAM/AddGroupBlade) )

Fill in:
- **Group type:** Security
- **Group name:** `<YOUR GROUP NAME>`
- **Group description:** Admin login group for Documaster
- Press **Create**

<img width="692" alt="add-group" src="https://user-images.githubusercontent.com/40164824/215751912-b9f43c1e-ffb4-4c17-a445-9f436a2170b7.png">

🔵 Go to the created group and take note of the Object ID. This must be provided to Documaster. 

<img width="994" alt="group-id" src="https://user-images.githubusercontent.com/40164824/215752360-c32cf636-142c-4933-b3a7-9f8d6c7accbf.png">


### Add external users
If external users (e.g. from Documaster) should be included in the admin group, they must be added to the tenant first.

Go to *Azure Active Directory → Users → New User → Invite external user* ( [🔗 Portal link](https://portal.azure.com/#view/Microsoft_AAD_UsersAndTenants/UserManagementMenuBlade/~/AllUsers) )

<img width="896" alt="invite-user" src="https://user-images.githubusercontent.com/40164824/215501459-ca10147c-7d99-42eb-869c-4182196ef1f9.png">

Fill in the user's email address, write a message, and press *invite*.


### Add users to the admin group
Go to the created group → Members → Add members

Search for the users you wish to add → Click on the user → Press "Select"

<img width="574" alt="Screenshot 2023-01-30 at 15 30 12" src="https://user-images.githubusercontent.com/40164824/215505032-50f08a3b-0478-4967-bb97-093230913771.png">


## Summary
The following information must be provided to Documaster after the setup is complete:
- 🔵 Your tenant ID
- 🔵 App registration's CLIENT ID
- 🔵 App registration's CLIENT SECRET
- 🔵 Admin group's OBJECT ID
