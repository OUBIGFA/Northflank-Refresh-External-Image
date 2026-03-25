# Northflank External Image Auto Refresh

[中文](./README.md) | [English](./README.en.md)

One-line summary: this package calls the Northflank restart API on a schedule so a service that already uses `External image` can pull the newest Docker Hub image again.

## 3-Minute Setup

### Step 0: create a new Northflank API token first

Go to the Northflank dashboard:

- https://app.northflank.com

Create or rotate your token first. You will store it in GitHub as `NF_API_TOKEN`.

Important:

- the token you posted earlier is already exposed
- do not reuse it
- rotate it first

### Step 1: copy this directory into your own private GitHub repository

Do not run this from a public repository if you can avoid it.  
The workflow will contain your real `project ID` and `service ID`.

### Step 2: replace the two example IDs in the workflow

Open this file:

- `.github/workflows/northflank-refresh-external-image.yml`

You will see this example URL:

```text
https://api.northflank.com/v1/projects/a86/services/b94/restart
```

Meaning:

- `a86` = example `project ID`
- `b94` = example `service ID`

Replace both values with your own.

### Step 3: add the GitHub secret and run the workflow once

Go to:

- `Settings -> Secrets and variables -> Actions`

Add this secret:

- `NF_API_TOKEN`

Then open:

- `Actions`

Run the workflow manually once and confirm your service restarts successfully.

## You only need to change 3 things

1. your `project ID`
2. your `service ID`
3. your `NF_API_TOKEN`

Everything else can usually stay as-is.

## Full Example

Example URL:

```text
https://api.northflank.com/v1/projects/a86/services/b94/restart
```

Field mapping:

- `a86` is an example `project ID`
- `b94` is an example `service ID`

Again:

- `a86 / b94` are example values only
- replace them with your own real values before deploying

## Why this works

This method assumes:

- your Northflank service already uses `External image`
- your image tag is `latest`

The workflow calls the `restart` API.  
When the service starts again, Northflank pulls the external image again, so it can get the newest version.

## If your image is not latest

If you use a fixed tag such as:

```text
my-image:1.2.3
```

then a restart will still pull that same fixed tag.  
This workflow is best for images that update behind `latest`.

## Change the schedule

Edit the `cron` value in:

- `.github/workflows/northflank-refresh-external-image.yml`

Current example:

```yaml
schedule:
  - cron: "17 4 * * 2"
```

Meaning:

- every Tuesday
- 04:17 UTC

## Local Dry Run

```powershell
$env:NF_API_TOKEN='your_new_token'
python .\scripts\refresh_northflank_external_image.py --dry-run
```

`--dry-run` prints the target URL only. It does not call the API.

## Files

- [workflow](/E:/_BIGFA%20Free/_code/_Mywork/Northflank%20Refresh%20External%20Image/.github/workflows/northflank-refresh-external-image.yml)
- [script](/E:/_BIGFA%20Free/_code/_Mywork/Northflank%20Refresh%20External%20Image/scripts/refresh_northflank_external_image.py)

## Official Docs

- [Run an image from a container registry](https://northflank.com/docs/v1/application/run/run-an-image-from-a-container-registry)
- [Manage CI/CD](https://northflank.com/docs/v1/application/release/manage-ci-cd)
- [Restart service API](https://northflank.com/docs/v1/api/project/services/restart-service)
