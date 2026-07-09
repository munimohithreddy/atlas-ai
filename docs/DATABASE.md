# Atlas AI Database

## Tables

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
