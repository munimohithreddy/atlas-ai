# Atlas AI Database

## Tables

### `brands`

Stores named Atlas brands that own opportunities and plans.

Key columns:

- `id`
- `name`
- `slug`
- `market`
- `description`
- `status`
- `created_at`
- `updated_at`

### `sites`

Stores owned or planned Atlas sites.

Key columns:

- `id`
- `name`
- `domain`
- `niche`
- `status`
- `created_at`

### `opportunities`

Stores evaluated business opportunities and calculated decision outputs.

Key columns:

- `id`
- `topic`
- `niche`
- score columns for demand, competition, buyer intent, affiliate, Pinterest, and SEO
- `opportunity_score`
- `recommendation`
- `reasoning`
- AI analysis columns
- `created_at`

### `opportunity_evidence`

Stores evidence rows supporting opportunity scores.

Key columns:

- `id`
- `opportunity_id`
- `source`
- `signal_type`
- `value`
- `summary`
- `confidence_score`
- `created_at`

### `affiliate_programs`

Stores curated affiliate program intelligence for monetization evaluation.

Key columns:

- `id`
- `name`
- `network`
- `category`
- `website_url`
- `commission_type`
- `commission_rate`
- `cookie_duration_days`
- `approval_required`
- `notes`
- `created_at`

### `business_plans`

Stores deterministic v1 plans derived from a ranked opportunity and optional brand.

Key columns:

- `id`
- `opportunity_id`
- `brand_id`
- `primary_monetization`
- `secondary_monetization`
- `primary_acquisition_channel`
- `secondary_acquisition_channels`
- `recommended_assets`
- `target_audience`
- `value_proposition`
- `revenue_low_monthly`
- `revenue_high_monthly`
- `revenue_confidence_score`
- `effort_level`
- `estimated_launch_days`
- `recommendation_summary`
- `next_action`
- `status`
- `created_at`
- `updated_at`

### `campaigns`

Stores launch-ready campaign plans derived from approved business plans.

Key columns:

- `id`
- `business_plan_id`
- `brand_id`
- `opportunity_id`
- `name`
- `slug`
- `goal`
- `status`
- `priority`
- `expected_monthly_revenue`
- `estimated_build_hours`
- `launch_target_date`
- `approved_at`
- `created_at`
- `updated_at`

### `campaign_tasks`

Stores ordered campaign execution tasks.

Key columns:

- `id`
- `campaign_id`
- `title`
- `description`
- `category`
- `status`
- `priority`
- `estimated_hours`
- `started_at`
- `completed_at`
- `blocked_reason`
- `completion_notes`
- `actual_hours` - fractional hours stored as `NUMERIC(8,2)` and allowed to be null
- `assigned_to`
- `due_date`
- `depends_on_task_id`
- `order_index`
- `created_at`
- `updated_at`

### `campaign_assets`

Stores planned campaign assets.

Key columns:

- `id`
- `campaign_id`
- `asset_type`
- `title`
- `channel`
- `status`
- `planned_quantity`
- `generated_quantity`
- `published_quantity`
- `created_at`
- `updated_at`
