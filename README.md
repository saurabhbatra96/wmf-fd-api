# WMF Fraud Detection API Frontend

## API SPECS

### Transaction

#### Resource Definition

|  |  |
:-----------:|:----------:
| **Base Path** | /api/v1/transaction |
| **Functionality** | Validates transactions as fraud/not fraud |
| **Verb** | POST |

#### Request
```json
{
	"contrib_id": "int - contribution_id, used for logging",
	"name": "string - donor name",
	"financial_type_id": "int - financial_type_id",
	"payment_instrument_id": "int - payment_instrument_id",
	"total_amount": "float - donation amount",
	"currency": "string - abbrv. currency info",
	"gateway": "string - payment gateway",
	"payment_method": "string - mode of payment",
	"country": "string - abbrv. country info",
	"utm_medium": "string - utm_medium",
	"utm_campaign": "string - utm_campaign truncated to first 3 letters",
	"avs_filter": "float - avs_filter values",
	"cvv_filter": "float - cvv_filter values",
	"country_filter": "float - country_filter values",
	"email_domain_filter": "float - email_domain_filter values",
	"utm_filter": "float - utm_filter values",
	"ip_filter": "float - ip_velocity_filter values",
	"minfraud_filter": "float - minfraud scores",
	"receive_date": "string - receive date in mysql format"
}
```
#### Response
```json
{
	"prediction": "bool - 1 for fraud, 0 for not fraud",
	"proba_score": "float - probability score of txn being fraud"
}
```

## Installation and usage
