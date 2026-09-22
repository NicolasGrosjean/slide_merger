# Slide Merger Frontend

Angular SPA for selecting configured slide parts and creating a merged PowerPoint presentation through the FastAPI backend.

This project was generated using [Angular CLI](https://github.com/angular/angular-cli) version 21.2.24.

## Run the frontend

Start the [backend](../backend/README.md), then run the Angular development server in another terminal:

```bash
cd frontend
npm install
npm start
```

Open [http://localhost:4200](http://localhost:4200). The frontend uses the slide definitions from `cli/settings.yaml` through the backend configuration endpoint.

## Development

To start a local development server, run:
From this directory, install dependencies and start the local development server:
npm install
npm start

```bash
ng serve
```

Once the server is running, open your browser and navigate to `http://localhost:4200/`. The application will automatically reload whenever you modify any of the source files.

The server runs at `http://localhost:4200` and proxies `/files` and `/slide_merger` to `http://localhost:8899`. Start the backend separately with `task server` from `backend/`.
npm run build
npm test

Angular CLI includes powerful code scaffolding tools. To generate a new component, run:

```bash
ng generate component component-name
```

For a complete list of available schematics (such as `components`, `directives`, or `pipes`), run:

```bash
ng generate --help
```

## Building

To build the project run:

```bash
ng build
```

This will compile your project and store the build artifacts in the `dist/` directory. By default, the production build optimizes your application for performance and speed.

## Running unit tests

To execute unit tests with the [Vitest](https://vitest.dev/) test runner, use the following command:

```bash
ng test
```

The frontend receives its slide-part definitions from `GET /slide_merger/config`. The backend reads the shared `cli/settings.yaml` file through `SLIDES_CONFIG_FILE`; local backend execution defaults to `../cli/settings.yaml`, and Docker mounts that file at `/app/cli-settings.yaml`.

For end-to-end (e2e) testing, run:

```bash
ng e2e
```

Angular CLI does not come with an end-to-end testing framework by default. You can choose one that suits your needs.

## Additional Resources

For more information on using the Angular CLI, including detailed command references, visit the [Angular CLI Overview and Command Reference](https://angular.dev/tools/cli) page.
