# How to Publish `usda-fas-sdk`

I have prepared the package locally in the `usda_fas_sdk` folder.
Due to security restrictions, I cannot push to your GitHub or upload to PyPI on your behalf.
Please follow these steps to complete the process.

## 1. Create GitHub Repository

1.  Keep this terminal open or open a new one.
2.  Navigate to the package directory:
    ```bash
    cd usda_fas_sdk
    ```
3.  **If you have the details:**
    Create a new repository named `usda-fas-sdk` on GitHub.
4.  Link and push:
    ```bash
    git remote add origin https://github.com/YOUR_USERNAME/usda-fas-sdk.git
    git branch -M main
    git push -u origin main
    ```

## 2. Publish to PyPI

1.  **Install build tools** (Already done):
    ```bash
    ./.venv/bin/pip install setuptools wheel twine python-dotenv
    ```
2.  **Build the package** (Already done):
    ```bash
    ./.venv/bin/python setup.py sdist bdist_wheel
    ```
3.  **Upload to PyPI**:
    (You will need a PyPI account)
    ```bash
    ./.venv/bin/twine upload dist/*
    ```

## 3. Install via Pip

Once uploaded, you can install it anywhere:
```bash
## 4. CI/CD with GitHub Actions

I have created a workflow in `.github/workflows/publish.yml` that will automatically publish to PyPI **when you create a Release**.

### Setup Required

1.  **Secret**: ensuring `PYPI_API_TOKEN` is set in your repository secrets.
2.  **Workflow**: The workflow uses `pypa/build` (best practice) and triggers on `release: [published]`.

### How to Publish

1.  Bump the version in `setup.py`.
2.  Push your changes to `main`.
3.  Go to the GitHub Interface -> **Releases** -> **Draft a new release**.
4.  Create a tag (e.g., `v0.1.2`, matching your setup.py).
5.  Click **Publish release**.

GitHub Actions will pick this up, build the package, and push it to PyPI.


## Note regarding `setup.py`
I have added placeholder values in `setup.py` for:
- `url`: `https://github.com/USERNAME/usda-fas-sdk`
- `author`: `Your Name`
- `author_email`: `your.email@example.com`

You may want to edit `setup.py` to fill these in before publishing.
