# Frontend Hosting and Deployment Definition v1

## Purpose
Define the governed deployment safety model for S3 + CloudFront hosted frontends so that destructive live-root deployment failure cannot recur.

## Scope
Applies to:
- company site frontend
- pilot frontend

## Current hosting reality
- company site and pilot are hosted from separate S3 buckets behind separate CloudFront distributions
- current live sites are restored and must remain stable
- S3 versioning is enabled on the frontend buckets
- CloudFront currently serves bucket root, not `current/`

## Prohibited deployment patterns
The following patterns are forbidden for live frontend deployment:
- `aws s3 sync ... --delete` against live root
- any destructive sync against a live shared target
- direct deployment write to bucket root
- promotion by destructive sync
- treating local build success as sufficient deployment safety proof

## Required deployment target model
Frontend deployments must use immutable release folders and controlled promotion.

Required structure per site:
- `releases/<release-id>/`
- `current/`

Example:
- `releases/<release-id>/index.html`
- `releases/<release-id>/assets/...`
- `releases/<release-id>/release.json`
- `current/index.html`
- `current/assets/...`

## Root write rule
Bucket root is logically read-only for deployment purposes.
No deployment may write directly to bucket root.
All deployment writes must target:
- `releases/<release-id>/`

Only controlled promotion logic may update:
- `current/`

## Promotion rule
Promotion must not use `sync --delete`.
Promotion must be a controlled copy or explicit overwrite into `current/`.

## Rollback rule
Rollback must be performed by promoting a prior retained release from:
- `releases/<old-release-id>/`
to:
- `current/`

## Runtime traceability requirement
Each release must include `release.json` containing at minimum:
- site
- environment
- release_id
- git_commit
- built_at_utc

A runtime build marker must be visible either:
- in rendered HTML, or
- via a fetchable runtime metadata file

## Environment isolation rule
Company and pilot must remain separately bounded by bucket and release path.
A deployment for one site must not target the other site.

## Known current gap
CloudFront currently serves bucket root rather than `current/`.
This must be treated as a controlled follow-on implementation gap.
No silent live migration is permitted under this document.
