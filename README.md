# WMF Fraud Detection API Frontend

## API SPECS

### Transaction

#### Resource Definition

|  |  |
:-----------:|:----------:
| **Base Path** | /v1/transaction |
| **Functionality** | Validates transactions as fraud/not fraud |
| **Verbs** | VALIDATE |

#### Request
```json
{
	"feature1": "param definition",
	"feature2": "param definition"
}
```
#### Response
```json
{
	"fraud": True/False
}
```
