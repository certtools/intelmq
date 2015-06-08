
# Microsoft DCU collector

## Config parameters

### Description
  * rate_limit: set this to 1 day
  * azure_account_name: the login for azure (Microsoft's cloud)
  * azure_account_key : a base64 encoded key. Microsoft will provide this for you
  * date: what blob to fetch from the Azure cloud. Each blob of data is in a container with a specific date.
Here you can either specify ```yesterday``` or a fixed date. If the value is null, all data will be fetched!
Please note that this can take very long for a year of data. Specifying a fixed date makes sense for debugging.
In most cases in production, you will want to specify ```yesterday```.
  * rate_limit: the usual rate limiting parameter. Please note that this must be 1 day (in seconds 86400 seconds)



### Example
 "microsoft-dcu-collector": {
        "azure_account_name": "azureaccountname",
        "azure_account_key": "ABCDEF01234567890abcdef42==",   
        "date": "yesterday",
        "rate_limit": 86400
 }

