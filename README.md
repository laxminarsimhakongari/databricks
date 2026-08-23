# Databricks Daily Job

This repository provisions and runs a small daily Databricks job with a
Databricks Asset Bundle and Jenkins. The job writes a timestamped health record
to a Delta table, which makes it useful as a deployment smoke test and as a
starting point for a real daily pipeline.

## Repository layout

- `databricks.yml` - bundle definition and `dev`/`prod` targets.
- `resources/daily_job.yml` - job, schedule, cluster, and task resources.
- `src/daily_job.py` - Python task executed by Databricks.
- `Jenkinsfile` - validate, deploy, and run pipeline.

## Local prerequisites

Install the Databricks CLI and authenticate with a supported profile or
environment variables:

```bash
export DATABRICKS_HOST="https://<workspace-host>"
export DATABRICKS_TOKEN="<personal-access-token>"
databricks bundle validate -t dev
databricks bundle deploy -t dev
databricks bundle run -t dev daily_job
```

The default `dev` target pauses the schedule. The `prod` target enables the
daily schedule after deployment.

The sample cluster uses the AWS node type `i3.xlarge`. Change
`node_type_id` in `resources/daily_job.yml` to a node type available in your
Databricks cloud and region before deploying.

## Jenkins setup

Create a Jenkins **Secret text** credential with ID `databricks-token`, and
configure the job with a `DATABRICKS_HOST` string parameter or environment
variable containing the workspace URL. The pipeline parameter
`DEPLOY_TARGET` controls whether Jenkins deploys to `dev` or `prod`.

The Jenkins agent must have the Databricks CLI installed and available on
`PATH`. The pipeline validates the bundle, deploys it, and runs the job once
so a deployment failure is visible immediately.