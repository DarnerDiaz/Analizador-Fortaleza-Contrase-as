# API Method 4

## Description
Detailed description of api_method_4 functionality.

## Parameters
- param1: Type explanation
- param2: Type explanation
- param3: Type explanation

## Returns
Returns object with properties:
- result: Boolean indicating success
- data: Response data
- error: Error message if failed

## Example Usage
\\\python
from app.api import api_method_4

response = api_method_4(
    param1="value",
    param2=42,
    param3=True
)
if response.result:
    print(response.data)
\\\

## Error Handling
Raises: ValueError, RuntimeError

## Performance Notes
- Complexity: O(n)
- Caching Support: Yes
- Rate Limit: 1000 req/min

## See Also
- Related API 1
- Related API 2
- Related API 3
