# All Sites from DattoRMM API

[Justin Cooksey](https://github.com/jscooksey), 29th May 2023

---

Pulls all Sites from a [DattoRMM](https://www.datto.com/au/products/rmm/) environment and export basic details in to CSV formatted file.
Removes the system sites of Managed, OnDemand & Deleted Devices.

Gets the API URL, Key and Secret from .env or environment variables (example below)

Functions to interact with the DattoRMM API are in the [dattormmapi.py](https://github.com/jscooksey/DattoRMM-API/blob/main/dattormmapi.py) Python file.

Main function to do the API requests and export to CSV is in the [export_sites.py](https://github.com/jscooksey/DattoRMM-API/blob/main/export_sites.py) Python file.

Not much error/exception managment in this at the moment.

---

**.env Example**

```
API_URL=https://xxxxx-api.centrastage.net
API_KEY=KEYVALUEGOESHERE
API_SECRET_KEY=SECRETGOESHERE
```

**Example Output CSV**

```
id,name,description,autotaskCompanyName,autotaskCompanyId,portalUrl,numberOfDevices,numberOfOnlineDevices,numberOfOfflineDevices
16272,Alpha Dynamics,Alpha Dynamics,Alpha Dynamics Pty Ltd,777,https://xxxxx.centrastage.net/csm/profile/summary/16272,200,198,2
16273,Acme Explosives,Acme Explosives,Wile E. Coyote Investments Pty Ltd,1861,https://syrah.centrastage.net/csm/profile/summary/16273,500,499,1
```
