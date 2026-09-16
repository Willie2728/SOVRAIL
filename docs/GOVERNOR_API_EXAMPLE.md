# Governor API example

Create a governed objective:

```json
POST /v1/governor/jobs
{
  "objective": "Finish Nuvolare Pro MVP",
  "total_budget": 100,
  "protected_reserve": 10
}
```

The response contains a `job_id`, recommended `model_tier`, budget mode, and action.

After each implementation batch, report authoritative consumption and objective progress:

```json
POST /v1/governor/jobs/<job_id>/events
{
  "credits": 4.5,
  "changed_files": 8,
  "tests_changed": 2,
  "tests_passed": 12,
  "state_changes": 1,
  "deployment_changes": 0
}
```

A blocked batch can report a normalized failure:

```json
{
  "credits": 2.0,
  "failure": "database migration test failed: duplicate column",
  "changed_files": 0,
  "tests_passed": 0
}
```

The external execution adapter must honor SOVRAIL's returned decision. `stop` means no further autonomous model spend; `checkpoint` means persist/verify the current state before further work; `execute` carries the currently recommended tier.
