# Setting up Azure AD applications for Documaster

ℹ️  Please take careful note of the sentences marked  with 🔵 as you will need to provide this information to Documaster.

## User groups
When setting up Documaster to work against an Azure AD instance, there are several requirements for the users and groups created in Azure AD.
The Documaster applications perform access control based on the groups a user is a member of. For this reason, it is very important that all users are a member of at least one Security or Office365 group.

⚠️  Users who are not members of any groups will not be able to log into the application!

🔵 The Azure Group IDs that must be used for access control and authorization purposes must be provided to Documaster for initial setup.

---

## Documaster application
### Create application

Go to *Azure Active Directory → App registrations → New Application registration*

INSERT_IMAGE

Create the new application:
1. **Name:** Documaster (whatever would make it easy for you to distinguish the application)
2. **Application type:** Web
3. **Redirect URI:** `https://YOUR_DOCUMASTER_APPLICATION_URL/login` (e.g. `https://demo.documaster.com/login`)
4. Click Register

INSERT_IMAGE

### Retrieve Application ID
🔵 Take note of the **Application ID** (which is used as Client ID) and the **Directory (tenant) ID**

INSERT_IMAGE

### Create a new Key (client secret)
⚠️ Key values are only visible right after their creation.

Go to *Azure Active Directory → App registrations → Documaster→ Certificates & secrets → New client secret*
1. **Description:** Documaster
2. **Expires:** Never expires
3. Click Save

INSERT_IMAGE

🔵 Take note of the generated key value (which is used as Client Secret)

### Grant permissions to retrieve user groups
Go to *Azure Active Directory → App registrations → Documaster → Manifest → Set groupMembershipClaims to «All» → Save*

INSERT_IMAGE

### Grant API permission
Go to *Azure Active Directory → App registrations → Documaster → API permissions → Add a permission → Microsoft Graph*

INSERT_IMAGE

Click **Delegated***permissions → Sign in and read user profile (User.Read) → Sign users in (openid) → View users’ basic profile (profile) → Add permissions*

Click **Application***Permissions → Read all groups (Group.Read.All) → Read all users’ full profiles (User.Read.All) → Add permissions*

Grant admin consent → Yes *requires administrative privileges)

INSERT_IMAGE


### **Add login and logout URLs**
Go to *Azure Active Directory → App registrations → Documaster → Authentication → Under the Redirect URIs add `https://INSTALLATION_URL/login` → Under Logout URL add `https://INSTALLATION_URL/logout` → Save*

INSERT_IMAGE

### **Allow ID Tokens in Implicit Grant**
Go to *Azure Active Directory → App registrations → Documaster → Authentication → Under the Implicit Grant toggle «ID Tokens» → Save*

INSERT_IMAGE

---
## Application for integrating parties
There are two possible approaches when creating an application for integrating parties:
1. The client application has a User Interface
2. The client application does not have a User Interface

Note that in both cases, tokens must be requested from Azure with the **openid**, **profile**, and **`https://graph.microsoft.com/.default`** scopes. URL encoded, this is:

```
openid%20profile%20https%3A%2F%2Fgraph.microsoft.com%2F.default
```

Additionally, the **id_token** must be sent to Documaster.


### UI-based client applications
In the case of UI-based client applications, a new Azure AD application must be created by following the same steps as for the Documaster application.

The only changes that would have to be made are:

* the name of the application (to better describe the application)
* the sign-on URL (which is application-specific)
* the reply URL (which is application-specific)
* the logout URL (which is application-specific)
* integrating applications do not need the *User.Read.All* and *Group.Read.All* permissions

With the above in place, applications can use the  [authorization code flow grant](https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-auth-code-flow)  to obtain a token to be used in communication with Documaster Archive.
Note that the linked Microsoft documentation contains sample requests that can be used to test the creation application (Postman).

⚠️ Please take into account any limitations listed in the linked Microsoft documentation.


### Service-based client applications
In the case of service-based client applications, some of the complexity of creating an Azure AD application can be omitted.
In order to create such an application you can follow the Documaster application creating steps and omit the following sections/steps:

* Add a sign-on URL
* Add a reply URL
* Add a logout URL
* integrating applications do not need the *User.Read.All* and *Group.Read.All* permissions

With the above in place, applications can use the  [resource owner password credentials grant](https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth-ropc)  to obtain a token to be used in communication with Documaster Archive.

Note that the linked Microsoft documentation contains sample requests that can be used to test the creation application (Postman).

⚠️ Please take into account any limitations listed in the linked Microsoft documentation.
