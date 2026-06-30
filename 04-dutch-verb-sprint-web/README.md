# Dutch Verb Sprint Web

A browser-based Dutch verb flashcard game built with Vite, React, and TypeScript.

The app shows one English infinitive at a time. Type the Dutch infinitive, press Enter or click **Check**, and get instant feedback. Wrong, skipped, and revealed answers come back soon so you can practise them again.

## Local development

Install dependencies:

```bash
npm install
```

Start the local development server:

```bash
npm run dev
```

Vite will print a local URL, usually `http://localhost:5173/`.

## Build

Create a production build:

```bash
npm run build
```

The built files will be written to `dist/`.

Preview the production build locally:

```bash
npm run preview
```

## Deploying to GitHub Pages

1. Push this folder to a GitHub repository.
2. Run `npm run build`.
3. Deploy the `dist/` folder with your preferred GitHub Pages workflow.

For a simple GitHub Actions deployment, create `.github/workflows/deploy.yml` in the repository:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: npm
      - run: npm ci
      - run: npm run build
      - uses: actions/upload-pages-artifact@v3
        with:
          path: dist

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - id: deployment
        uses: actions/deploy-pages@v4
```

Then enable GitHub Pages in the repository settings and choose **GitHub Actions** as the source.
