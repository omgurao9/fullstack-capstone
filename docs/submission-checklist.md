# Capstone submission evidence checklist

Create these files/screenshots only after you have run the application and observed the real result.

- `django_server`: terminal showing `python manage.py runserver` running.
- `loginuser`: login cURL command and actual response.
- `logoutuser`: logout cURL command and actual response.
- `getdealerreviews`: reviews endpoint command and actual response.
- `getalldealers`: all dealers endpoint command and actual response.
- `getdealerbyid`: dealer detail endpoint command and actual response.
- `getdealersbyState`: Kansas filter endpoint command and actual response.
- `getallcarmakes`: car makes/models endpoint command and actual response.
- `analyzereview`: sentiment endpoint command and actual response.
- `CICD`: successful GitHub Actions workflow run output / evidence.
- `deploymentURL`: real public deployment URL.
- `admin_login.png`, `admin_logout.png`: screenshots of actual Django admin login/logout.
- `get_dealers.png`, `get_dealers_loggedin.png`, `dealersbystate.png`, `dealer_id_reviews.png`, `dealership_review_submission.png`, `added_review.png`: screenshots of local browser pages.
- `deployed_landingpage.png`, `deployed_loggedin.png`, `deployed_dealer_detail.png`, `deployed_add_review.png`: screenshots from your deployed site.

## Recommended evidence workflow
1. Install requirements and migrate the database.
2. Seed demo data.
3. Create a superuser for admin screenshots.
4. Run tests.
5. Run the server and capture the actual cURL outputs.
6. Use the browser to capture the required screenshots, with the address bar visible where required.
7. Push to GitHub and confirm the repository is public.
8. Confirm the GitHub Actions workflow succeeds.
9. Deploy to a hosting provider and capture screenshots from the real deployment.
