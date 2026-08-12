# Vue 3 + TypeScript + Vite

This template should help get you started developing with Vue 3 and TypeScript in Vite. The template uses Vue 3 `<script setup>` SFCs, check out the [script setup docs](https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup) to learn more.

Learn more about the recommended Project Setup and IDE Support in the [Vue Docs TypeScript Guide](https://vuejs.org/guide/typescript/overview.html#project-setup).

## End-to-end tests

This project includes Playwright automation for the prompt browse and add flows.

Run the tests from the `frontend/` directory:

```bash
npm install
npm run test:e2e
```

The Playwright config starts the Vite dev server automatically and mocks the `/api/prompts` requests in the browser, so the tests stay fast and do not require a live backend.
