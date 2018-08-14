# WMF Fraud Detection API Frontend

## API SPECS

### Transaction

#### Resource Definition

|  |  |
:-----------:|:----------:
| **Base Path** | /api/v1/transaction |
| **Functionality** | Validates transactions as fraud/not fraud |
| **Verb** | POST |

#### Request Definition

| parameter | description |
:----------:|:-----------:|
| `contrib_id` | `int` - contribution_id, used for logging |
| `name`	| `string` - donor name |
| `financial_type_id` | `int` - financial_type_id |
| `payment_instrument_id` | `int` - payment_instrument_id |
| `total_amount` | `float` - donation amount |
| `currency` | `string` - abbrv. currency info |
| `gateway` | `string` - payment gateway |
| `payment_method` | `string` - mode of payment |
| `country` | `string` - abbrv. country name |
| `utm_medium` | `string` - utm_medium |
| `utm_campaign` | `string` - utm_campaign truncated to first 3 letters |
| `avs_filter` | `float` - avs_filter values |
| `cvv_filter` | `float` - cvv_filter values |
| `country_filter` | `float` - country_filter_values |
| `email_domain_filter` | `float` - email_domain_filter values |
| `utm_filter` | `float` - utm_filter values |
| `ip_filter` | `float` - ip_velocity_filter values |
| `minfraud_filter` | `float` - minfraud scores |
| `receive_date` | `string` - receive date in mysql format |

##### Examples

**cURL**

```bash
curl -X POST \
  -d 'http://localhost:5000/api/v1/transaction?contrib_id=1234567&name=Jon%20Big%20Birdman&financial_type_id=9&payment_instrument_id=16&total_amount=15.99&currency=USD&gateway=globalcollect&payment_method=cc&country=US&utm_medium=Waystogive&utm_campaign=C18&avs_filter=0&cvv_filter=0&country_filter=0&email_domain_filter=0&utm_filter=0&ip_filter=0&minfraud_filter=0.10000000149011612&receive_date=2015-03-15%2018:04:55'
```

**PHP**

```php
<?php

$curl = curl_init();

curl_setopt_array($curl, array(
  CURLOPT_PORT => "5000",
  CURLOPT_URL => "http://localhost:5000/api/v1/transaction",
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_ENCODING => "",
  CURLOPT_MAXREDIRS => 10,
  CURLOPT_TIMEOUT => 30,
  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
  CURLOPT_CUSTOMREQUEST => "POST",
  CURLOPT_POSTFIELDS => array(
  	'contrib_id' => 1234567,
  	'name' => "Jane Doe",
  	'financial_type_id' => 9,
  	'payment_instrument_id' => 15,
  	'receive_date' => "2018-08-01 02:12:42",
  	'total_amount' => 3.00,
  	'currency' => "USD",
  	'gateway' => "globalcollect",
  	'payment_method' => "cc",
  	'country' => "SE",
  	'utm_medium' => "sidebar",
  	'utm_campaign' => "C13",
  	'avs_filter' => 50,
  	'cvv_filter' => 0,
  	'email_domain_filter' => 0,
  	'utm_filter' => 0,
  	'ip_filter' => 0,
  	'minfraud_filter' => 0.05000000074505806,
  	'country_filter' => 0,
  );,
));

$response = curl_exec($curl);
$err = curl_error($curl);

curl_close($curl);

if ($err) {
  echo "cURL Error #:" . $err;
} else {
  echo $response;
}
```

#### Response

| response variable | description |
:------------------:|:-----------:|
| `prediction` | `int` - 1 for fraud, 0 for not fraud |
| `proba_score` | `float` - probability score of txn being fraud |

##### Example

```json
{
    "prediction": 1,
    "proba_score": 0.985672492234017
}
```

## Installation and usage
* Install the required python libraries using pip install. Strongly recommended that you do that in a virtualenv as there are dependencies on old scikit libraries.
* Make sure the private folder is populated with the required files. In order to generate them, follow - https://github.com/saurabhbatra96/wmf-fraud-pipeline#pipeline-steps---importing-a-freshupdated-version-of-the-model-into-the-api
* Move into the api version directory - `$ cd v1`.
* Start the api with `$ python main.py`
* The api should be ready to receive POST requests at http://localhost:5000/api/v1/transaction
