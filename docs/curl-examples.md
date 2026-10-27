# cURL examples for assignment evidence

Run the Django server first:
```powershell
py manage.py runserver
```
Examples below use PowerShell-friendly line continuations only when shown with backticks. Save the *actual command and output from your terminal* into the required evidence files; don't submit these examples as if they were already run.

## GET all dealers
```bash
curl -s http://127.0.0.1:8000/api/dealers/
```

## GET dealer by ID (example ID 1)
```bash
curl -s http://127.0.0.1:8000/api/dealers/1/
```

## GET reviews for dealer ID 1
```bash
curl -s http://127.0.0.1:8000/api/dealers/1/reviews/
```

## GET dealers in Kansas
```bash
curl -s http://127.0.0.1:8000/api/dealers/state/Kansas/
```

## GET car makes and models
```bash
curl -s http://127.0.0.1:8000/api/carmakes/
```

## Analyze review sentiment
```bash
curl -s -X POST http://127.0.0.1:8000/api/analyze-review/ -H "Content-Type: application/json" -d "{\"review\":\"Fantastic services\"}"
```

## Login/logout with a cookie jar (bash, Git Bash, or WSL)
Django CSRF protection is enabled. First retrieve the CSRF cookie, then submit it with the login request. Run these in Git Bash:
```bash
curl -s -c cookies.txt http://127.0.0.1:8000/ > /dev/null
CSRF=$(grep csrftoken cookies.txt | awk '{print $7}')
curl -i -b cookies.txt -c cookies.txt -X POST http://127.0.0.1:8000/api/login/ -H "Content-Type: application/json" -H "X-CSRFToken: $CSRF" -H "Referer: http://127.0.0.1:8000/" -d "{\"username\":\"demo_user\",\"password\":\"DemoPass123!\"}"
CSRF=$(grep csrftoken cookies.txt | awk '{print $7}')
curl -i -b cookies.txt -c cookies.txt -X POST http://127.0.0.1:8000/api/logout/ -H "X-CSRFToken: $CSRF" -H "Referer: http://127.0.0.1:8000/"
```

## Login/logout from Windows PowerShell
Use a browser or Git Bash for the cookie-based flow above. PowerShell's `curl` alias can behave differently; use `curl.exe` explicitly if using PowerShell.
