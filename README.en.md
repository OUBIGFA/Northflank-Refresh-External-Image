<div align="center">
  <h1>Northflank External Image Auto Refresh</h1>
  <p>Periodically restarts Northflank services using external images, pulling the latest version from Docker Hub</p>
  <p><a href="README.md">简体中文</a> | English</p>
  <p>
    <img alt="Shell" src="https://img.shields.io/badge/language-Shell-4EAA25">
    <img alt="Platform" src="https://img.shields.io/badge/platform-GitHub%20Actions-2088FF">
    <img alt="License" src="https://img.shields.io/badge/license-MIT-111827">
    <img alt="Schedule" src="https://img.shields.io/badge/schedule-Weekly-22c55e">
  </p>
</div>

> Set up in 3 minutes. After that, your Northflank service is restarted on schedule and always pulls the freshest external image.

## 3-Minute Setup

### Step 0: Create a Northflank API Token

Open:

- https://app.northflank.com

Create an API Token with the proper permissions. You will store it in GitHub as `NF_API_TOKEN`.

Screenshots for getting `NF_API_TOKEN`:

![Step 1](./scripts/image/01.png)

![Step 2](./scripts/image/02.png)

![Step 3](./scripts/image/03.png)

### Step 1: Import the repository as a private repo with GitHub Importer

1. Log into GitHub and open https://github.com/new/import
2. Fill in the fields as follows:

| Field | Value |
| --- | --- |
| `Your old repository's clone URL` | `https://github.com/OUBIGFA/Northflank-Refresh-External-Image` |
| `Owner` | your GitHub account |
| `Repository name` | your repo name, e.g. `my-northflank-refresh` |
| `Privacy` | select `Private` |

1. Click `Begin import` and wait (usually under a minute)
2. Once imported, you own a private repository. All subsequent Secret and workflow settings are done here.

### Step 2: Replace the example IDs in the workflow

Open:

- `.github/workflows/northflank-refresh-external-image.yml`

You will see this example URL:

```text
https://api.northflank.com/v1/projects/a86/services/b94/restart
```

Meaning:

- `a86` = example `project ID`
- `b94` = example `service ID`

Replace both with your own values.

### Step 3: Add the GitHub Secret and run manually

Go to:

- `Settings -> Secrets and variables -> Actions`

Add this Secret:

- `NF_API_TOKEN`

Then open `Actions` and run `northflank-image-Update` manually. Confirm that your service restarts successfully.

## You only need to change 3 things

1. your `project ID`
2. your `service ID`
3. your `NF_API_TOKEN`

Everything else can usually stay as-is.

## Full Example

```text
https://api.northflank.com/v1/projects/a86/services/b94/restart
```

- `a86` is an example `project ID`
- `b94` is an example `service ID`

Always replace them with your real values before deploying.

## Why this works

Prerequisites:

- your Northflank service is already configured as `External image`
- your image tag is `latest`

The workflow calls the `restart` API. When the service restarts, Northflank pulls the external image again, so it gets the newest version.

## If your image is not latest

If you use a fixed tag such as:

```text
my-image:1.2.3
```

a restart still pulls that same fixed tag. This workflow is best for rolling tags like `latest`.

## Change the schedule

Edit the `cron` value in `.github/workflows/northflank-refresh-external-image.yml`:

```yaml
schedule:
  - cron: "17 4 * * 2"
```

Meaning:

- every Tuesday
- 04:17 UTC

## Official Docs

- [Run an image from a container registry](https://northflank.com/docs/v1/application/run/run-an-image-from-a-container-registry)
- [Manage CI/CD](https://northflank.com/docs/v1/application/release/manage-ci-cd)
- [Restart service API](https://northflank.com/docs/v1/api/project/services/restart-service)

## License

This project is licensed under the MIT License.

