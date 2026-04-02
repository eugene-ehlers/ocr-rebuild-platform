# Frontend Manual Deployment Execution Package v1

## Purpose
Define the governed manual deployment execution model for S3 + CloudFront hosted frontends using immutable releases and controlled promotion.

## Hard rules
1. Do not deploy directly to bucket root.
2. Do not run `aws s3 sync ... --delete` against any live frontend target.
3. Do not promote using destructive sync.
4. Do not deploy without a retained release artifact and release metadata.
5. Do not invalidate CloudFront until promotion is complete and verified.

## Allowed deployment phases
1. Build locally
2. Upload build to `releases/<release-id>/`
3. Verify uploaded release contents
4. Promote approved release into `current/`
5. Invalidate CloudFront
6. Verify runtime title, assets, and build marker

## Required release metadata
Each release must contain `release.json` with:
- site
- environment
- release_id
- git_commit
- built_at_utc

## Rollback procedure
1. Identify prior approved release in `releases/`
2. Copy prior release into `current/`
3. Invalidate CloudFront
4. Verify runtime state

## Explicitly banned commands
- `aws s3 sync dist/ s3://<bucket> --delete`
- `aws s3 sync dist/assets/ s3://<bucket>/assets/ --delete`
- any destructive root-level sync or delete used as promotion logic

## Current state note
This execution package defines the governed target model.
Current live hosting still serves root and requires a controlled follow-on change before `current/` becomes active runtime origin.
