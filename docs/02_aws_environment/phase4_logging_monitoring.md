# Phase 4 Implementation Design – Logging & Monitoring

## 6. Logging & Monitoring

### 6.1 CloudWatch Logs
- Lambda: `/aws/lambda/<function-name>`
- ECS Tasks: `/ecs/<ecs-task-name>`
- Retention: 30–60 days debug logs, longer for audit

### 6.2 Metrics
- Lambda: Invocations, Duration, Errors, Throttles, IteratorAge
- ECS: CPU, Memory, Task Count, Failures
- Step Functions: Execution count, duration, failed executions, Map state failures

### 6.3 Alarms
- CloudWatch Alarms trigger SNS:
  - Lambda errors > 1%
  - ECS task failures
  - Step Function execution failures/timeouts
  - SQS queue depth thresholds
- SNS Topics: `ocr-sns-errors-prod`

### 6.4 Dashboards
- Visualize per-pipeline:
  - Lambda invocation success/failure
  - Step Function execution timeline
  - ECS resource usage
  - SQS queue depth

### 6.5 X-Ray
- Tracing for all Lambda, ECS, Step Functions
- Sampling enabled to reduce cost
- Bottleneck identification & performance optimization

### 6.6 Compliance
- Logs do not store PII
- CloudTrail enabled for all account activity
- Audit trails for pipeline executions, manifest updates, S3 operations

