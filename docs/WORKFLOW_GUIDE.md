# Atlas AI Workflow Guide

Atlas guides work through this sequence:

Opportunity -> Business Plan -> Campaign -> Campaign Tasks -> Campaign Assets -> Production Queue -> Ready to Publish

## Task lifecycle

- `pending`: waiting for a completed dependency or for the campaign to become executable.
- `ready`: ready to start.
- `in_progress`: actively being worked.
- `blocked`: paused because a decision or input is missing.
- `review`: waiting for task review.
- `completed`: finished and can unlock dependent pending tasks.
- `cancelled`: removed from executable work. Cancelled dependencies do not unlock downstream tasks.

Only completed dependencies unlock downstream tasks. Blocked and cancelled dependencies keep dependent tasks waiting.

## Asset lifecycle

- `planned`: planned deliverable.
- `queued`: ready to start production.
- `in_production`: actively being produced.
- `review`: waiting for review.
- `rejected`: needs revision.
- `approved`: approved but not yet marked ready to publish.
- `ready_to_publish`: prepared for future publishing workflows.
- `blocked`: paused because a decision or input is missing.
- `cancelled`: removed from active production.

## Action visibility

Task actions:

- pending: explain the dependency; no primary action.
- ready: Start Task.
- in_progress: Complete Task, Block Task.
- blocked: Unblock Task.
- review: Complete Task.
- completed: Reopen.
- cancelled: Reopen.

Asset actions:

- planned: Add to Production Queue.
- queued: Start Production.
- in_production: Send for Review, Block Asset.
- review: Approve, Request Changes.
- rejected: Resume Production.
- approved: Confirm Ready to Publish.
- ready_to_publish: view-only.
- blocked: Unblock Asset.
- cancelled: Reopen.

## Status formatting

Normal UI must display human-readable labels instead of raw enum values:

- `display_ads` -> Display Advertising
- `lead_generation` -> Lead Generation
- `digital_product` -> Digital Product
- `buying_guide` -> Buying Guide
- `comparison_page` -> Comparison Page
- `in_production` -> In Progress
- `ready_to_publish` -> Ready to Publish

## Dashboard next-action rules

The dashboard recommends one next action from real loaded state:

1. Blocked tasks or assets.
2. Assets waiting for review.
3. Ready campaign tasks.
4. Assets ready to start.
5. Campaigns waiting for approval.
6. Business plans without campaigns.
7. Opportunities without business plans.
8. Create first opportunity.
