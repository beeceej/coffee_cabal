# Running The Backend
The backend is a FastAPI application that uses `pip-tools` to manage dependencies
```shell
cd backend

# starts up database
docker compose up -d db

# loads data into database
docker cmpose run --build load_data

# runs coffee_cabal FastAPI server
docker compose up --build coffee_cabal
```

# Running the Frontend
The frontend is an angular application that executes a few HTTP requests to answer a few questons from the backend server
```shell
cd frontend
npm install -g @angular/cli
npm install
ng serve
```

# Improvements to the backend
- Should enforce formatting with `black`
- Should typecheck with a tool like `mypy`
- Should lint with a tool like `pylint`
- Tests should be implemented
- Database Migrations should use a tool like `Alembic`

# Improvements to the frontend
- Each question / response could be put into their own components
- Should be linted with eslint
- Should declare types for Response from API
- Should write tests for the App component
- Should enforce formatting with a tool like `prettier`

# Getting to production:
## Backend
This codebase should deploy a database into the cloud, using an Infrastructure as Code tool like terraform
This codebase should deploy like:
1. Build And Tag Image
2. Push Image to a remote container registry
3. Deployment platform of choice should pull the image and run the application
4. Secrets should be handled outside the codebase, and injected into the running application (AWS Secrets Manager or similar)

## Frontend
1. Define Deployment Target
    - Set up a CDN in front of SPA application with Infrastructure as Code (Terraform)
    - Deploy application to _something_ like AWS S3 as a static website.
    - There are platforms like `Netlify` which make all of this easy enough
2. Build `ng build`
3. Publish bundle
4. Bust CDN Cache, so that clients get the latest version