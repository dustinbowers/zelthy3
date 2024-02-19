## Communications Package

### Overview

Communication Package will have models to store communication related configs and transactions and it exposes certain APIs and interfaces to support various communication functionalities.

### Python APIs exposed by the communication package:

1. Sending SMS: Programmatically send SMS

```python
from ..packages.communication.sms import SMS

# if key is not provided, sms is attempted to be sent with default config
sms_uuid = SMS.send_msg(destination="+919999911111", msg="Hello World", key=None)

```

2. Retry sending SMS: Retry sending SMS with a known msg_uuid

```python
from ..packages.communication.sms import SMS

# if key is not provided, sms is attempted to be sent with default config
sms_uuid = SMS.retry_send(msg_uuid="abcde-fghi")

```

3. Sync delivery Report: Attemps syncing delivery report of all such messages for which delivery report is not available.

```python

from ..packages.communication.sms import SMS
SMS.sync_delivery_report()

```

4. Sending Email: Programmatically send an Email

```python
from ..packages.communication.email import Email

# if key is not provided, sms is attempted to be sent with default config
email = Email()
email.attach()
email.send()

```

5. Retry sending Email: Retry sending Email with a known msg_uuid

```python
from ..packages.communication.email import Email

# if key is not provided, sms is attempted to be sent with default config
email_uuid = Email.retry_send(msg_uuid="abcde-fghi")

```

3. Sync inbox: Attemps syncing inbox.

```python

from ..packages.communication.sms import SMS
SMS.sync_delivery_report()

```

4. List of messages in transaction record: #### TODO

### Web interfaces exposed by the communication package:

Communication package exposes certain web interfaces to easily allow enabling a communications functionality in any application. The endpoints exposed are:

1. Email page

2. SMS page

3. Telephony page

### Rest APIs exposed by the communication package:

1. #### Create configurations: Allows storing configurations.

Endpoint

```css
[POST] /<pkg_root_route>/config/create

```

HTTP Method

```csharp
[POST]
```

Request body

```json
{
  "provider": "",
  "provider_pkg_name": "",
  "type": "sms",
  "config": {
    "config_key1": "value1",
    "config_key1": "value2"
  }
}
```

Response body

```json
{
    "success": true,
    "msg": "Successfully created",
    "data": {
        "id" 1
    }
}

```

2. #### Update configurations: Allows updating configurations.
   Endpoint

```css
[POST] /<pkg_root_route>/config/update

```

HTTP Method

```csharp
[POST]
```

Request body

```json
{
  "id": "1",
  "provider": "",
  "provider_pkg_name": "",
  "type": "sms",
  "config": {
    "config_key1": "value1",
    "config_key1": "value2"
  }
}
```

Response body

```json
{
    "success": true,
    "msg": "Successfully created",
    "data": {
        "id" 1
    }
}

```

3. #### List available configurations: Allows updating configurations.
   Endpoint

```css
[POST] /<pkg_root_route>/config/list/?type=sms&provider=msg91

```

HTTP Method

```csharp
[GET]
```

Response body

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "provider": "",
      "provider_pkg_name": "",
      "type": "sms",
      "config": {
        "config_key1": "value1",
        "config_key1": "value2"
      }
    }
  ]
}
```

4. ### Delete configuration

````css
[GET] /<pkg_root_route > /config/delete/?id=1 Response body ```json {
  "success":true,"msg": "Successfully deleted";
}
````

### Building provider integrations packages for enabling communication through certain providers.

Communincations package needs to leverage third party providers for delegating various downstream functionalities of sms, telephony etc. Provider packages can be easily developed by utilizing the various APIs
exposed by the base communications package. Also Communications packages expects the provider packages
to implement certain APIs following the mandated specifications.

Steps involved in implementing a provider package:

- Implement a configuration page that allows storing or updating provider specific configurations. This will
  require the provider package to integrated with the configurational APIs of the communications package.
- Implements APIs required by the Communications Package:

  ### For SMS packages

  1. #### Send SMS.
     Endpoint

  ```css
  [POST] /<pkg_root_route>/sms/send/

  ```

  HTTP Method

  ```csharp
  [POST]
  ```

  Request body

  ```json
  {
     "msg": "Hello World",
     "destination": "+919999911111"
      "config": {
          "config_key1": "value1",
          "config_key1": "value2"
      }
  }

  ```

  Response body

  ```json
  {
    "success": true,
    "msg": "Successfully queued",
    "data": {
      "msg_uuid": "",
      "extra_data": {}
    }
  }
  ```

  2. #### Retry sending SMS.
     Endpoint

  ```css
  [POST] /<pkg_root_route>/sms/retry/

  ```

  HTTP Method

  ```csharp
  [POST]
  ```

  Request body

  ```json
  {
    "msg_uuid": "abdioioio-akdidui"
  }
  ```

  Response body

  ```json
  {
    "success": true,
    "msg": "Successfully queued"
  }
  ```

  3. #### Fetch delivery report

  Endpoint

  ```css
  [POST] /<pkg_root_route>/sms/delivery_report/

  ```

  HTTP Method

  ```csharp
  [POST]
  ```

  Request body

  ```json
  {
    "msg_uuids": ["abdioioio-akdidui"]
  }
  ```

  Response body

  ```json
  {
    "success": true,
    "data": [
      {
        "msg_uuid": "",
        "status": "delivered"
      }
    ]
  }
  ```

?? How will frontend js integration happen (for e.g. Nice alerts notif for incoming call)
