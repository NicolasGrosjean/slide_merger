# Slide Merger Frontend

Angular SPA for selecting configured slide parts and creating a merged PowerPoint presentation through the FastAPI backend.

This project was generated using [Angular CLI](https://github.com/angular/angular-cli) version 21.2.24.

## Run the frontend

Start the [backend](../backend/README.md), then run the Angular development server in another terminal:

```bash
cd frontend
npm install
npm audit fix
npm start
```

Open [http://localhost:4200](http://localhost:4200). The frontend uses the slide definitions from `cli/settings.yaml` through the backend configuration endpoint.

The frontend container healthcheck requests `/ping` through Nginx, which proxies the request to the backend. The container is healthy only while the backend ping endpoint is reachable.

## Testing

Run the frontend unit tests with:

```bash
npm test -- --watch=false
```

Tests cover the API request contract, slide path construction, placeholder fallback, and filename search behavior.

## Additional Resources

For more information on using the Angular CLI, including detailed command references, visit the [Angular CLI Overview and Command Reference](https://angular.dev/tools/cli) page.
