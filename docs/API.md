# Atlas AI API

Base path: `/api/v1`

## Health

### `GET /health`

Returns application, database, and Redis health status.

## Research

### `POST /research/preview`

Runs configured research providers for a topic and optional niche, then returns provider evidence without creating an opportunity or storing evidence.

Request:

```json
{
  "topic": "best espresso machines",
  "niche": "coffee"
}
```

Response:

```json
{
  "topic": "best espresso machines",
  "niche": "coffee",
  "evidence": [
    {
      "source": "mock_research",
      "signal_type": "demand",
      "value": 65,
      "summary": "Mock demand estimate from topic length and niche context for 'best espresso machines'.",
      "confidence_score": 70
    }
  ]
}
```

Research preview includes `affiliate_programs` evidence when stored affiliate programs match the submitted topic or niche.

## Affiliate Programs

### `POST /affiliate-programs`

Creates a stored affiliate program.

Request:

```json
{
  "name": "Coffee Gear Partner",
  "network": "Impact",
  "category": "coffee",
  "website_url": "https://example.com/coffee",
  "commission_type": "percent",
  "commission_rate": 12.5,
  "cookie_duration_days": 30,
  "approval_required": true,
  "notes": "espresso machines and coffee gear"
}
```

Response: `AffiliateProgramResponse`.

### `GET /affiliate-programs`

Lists stored affiliate programs.

### `GET /affiliate-programs/{id}`

Returns one stored affiliate program.

## Opportunities

### `POST /opportunities`

Creates an opportunity from manually supplied scores.

Request:

```json
{
  "topic": "best espresso machines",
  "niche": "coffee",
  "demand_score": 80,
  "competition_score": 40,
  "buyer_intent_score": 90,
  "affiliate_score": 70,
  "pinterest_score": 60,
  "seo_score": 50
}
```

Response: `OpportunityResponse`.

### `POST /opportunities/evaluate`

Evaluates and stores an opportunity from topic and optional niche only. The mock research provider creates score signals and evidence rows; no external research APIs are called.

Request:

```json
{
  "topic": "best espresso machines",
  "niche": "coffee"
}
```

Response:

```json
{
  "id": 1,
  "topic": "best espresso machines",
  "niche": "coffee",
  "demand_score": 65,
  "competition_score": 57,
  "buyer_intent_score": 58,
  "affiliate_score": 67,
  "pinterest_score": 44,
  "seo_score": 57,
  "opportunity_score": 59.25,
  "recommendation": "WATCH",
  "reasoning": "best espresso machines scored 59.25/100 with recommendation WATCH. Demand=65, Competition=57, BuyerIntent=58, Affiliate=67, Pinterest=44, SEO=57."
}
```

Evidence rows are stored with the opportunity and can be retrieved from the detail endpoint.

### `POST /opportunities/portfolio`

Evaluates multiple topics with the research orchestrator, ranks them by Business Opportunity Score, and returns the ranked portfolio without creating `Opportunity` records.

Request:

```json
{
  "topics": [
    "best espresso machines",
    "home office ideas",
    "standing desk accessories"
  ],
  "niche": "affiliate"
}
```

`topics` must contain at least one topic. Topics are trimmed and de-duplicated case-insensitively before evaluation.

Response:

```json
{
  "results": [
    {
      "rank": 1,
      "topic": "best espresso machines",
      "business_score": 66.55,
      "recommendation": "WATCH",
      "confidence": 70,
      "demand_score": 65,
      "competition_score": 57,
      "buyer_intent_score": 58,
      "affiliate_score": 67,
      "pinterest_score": 44,
      "seo_score": 57
    }
  ]
}
```

Results are sorted by highest `business_score`. Scores are calculated from provider evidence using the evidence-based scoring service, and missing score inputs use the documented neutral default of `50`. `confidence` is the rounded average confidence across collected evidence for the topic, or `0` if no evidence is available.

### `POST /opportunities/evaluate-with-evidence`

Evaluates and stores an opportunity from topic, optional niche, and manually submitted research evidence. This endpoint does not call OpenAI, scrape websites, or call external search providers.

Request:

```json
{
  "topic": "best espresso machines",
  "niche": "coffee",
  "evidence_items": [
    {
      "source": "manual_search",
      "signal_type": "demand",
      "value": 80,
      "summary": "Search demand appears strong.",
      "confidence_score": 90
    },
    {
      "source": "manual_search",
      "signal_type": "competition",
      "value": 45,
      "summary": "SERP competition looks manageable.",
      "confidence_score": 80
    },
    {
      "source": "manual_search",
      "signal_type": "buyer_intent",
      "value": 85,
      "summary": "Queries show clear buying language.",
      "confidence_score": 85
    }
  ]
}
```

Supported `signal_type` values:

- `demand`
- `competition`
- `buyer_intent`
- `affiliate` or `affiliate_potential`
- `pinterest` or `pinterest_potential`
- `seo` or `seo_potential`

Multiple evidence items for the same signal are combined with a confidence-weighted average. Missing signals default to `50`, the documented neutral midpoint.

Evidence signal mapping:

- `demand` -> `demand_score`
- `competition` -> `competition_score`
- `buyer_intent` -> `buyer_intent_score`
- `affiliate` or `affiliate_potential` -> `affiliate_score`
- `pinterest` or `pinterest_potential` -> `pinterest_score`
- `seo` or `seo_potential` -> `seo_score`

`confidence_score` must be an integer from `0` to `100`, where `0` means no confidence and `100` means maximum confidence.

Response: `OpportunityResponse`. Evidence rows are stored and can be retrieved from `GET /opportunities/{opportunity_id}`.

When `OPENAI_API_KEY` is configured, Atlas also synthesizes the submitted evidence and calculated scores into AI analysis fields stored on the opportunity. If the key is missing or the AI response is unusable, Atlas stores deterministic fallback analysis instead.

### `GET /opportunities/{opportunity_id}`

Returns one opportunity plus the evidence used to score it.

Response:

```json
{
  "id": 1,
  "topic": "best espresso machines",
  "niche": "coffee",
  "demand_score": 65,
  "competition_score": 57,
  "buyer_intent_score": 58,
  "affiliate_score": 67,
  "pinterest_score": 44,
  "seo_score": 57,
  "opportunity_score": 59.25,
  "recommendation": "WATCH",
  "reasoning": "best espresso machines scored 59.25/100 with recommendation WATCH. Demand=65, Competition=57, BuyerIntent=58, Affiliate=67, Pinterest=44, SEO=57.",
  "ai_executive_summary": "best espresso machines in coffee scored 59.25/100 with a WATCH recommendation.",
  "ai_key_strengths": [
    "Strongest signal: demand at 65/100.",
    "Buyer intent score: 58/100."
  ],
  "ai_key_risks": [
    "Weakest signal: competition at 43/100.",
    "Competition score: 57/100."
  ],
  "ai_recommendation_reason": "The deterministic analysis recommends WATCH based on the calculated opportunity score.",
  "ai_suggested_next_actions": [
    "Review the stored evidence for signal gaps.",
    "Add higher-confidence evidence for any weak signals.",
    "Compare this opportunity against at least two alternatives."
  ],
  "evidence": [
    {
      "id": 1,
      "opportunity_id": 1,
      "source": "mock_research",
      "signal_type": "demand",
      "value": 65,
      "summary": "Mock demand estimate from topic length and niche context for 'best espresso machines'.",
      "confidence_score": 70
    }
  ]
}
```

### `GET /opportunities`

Lists stored opportunities in newest-first order.

### `POST /opportunities/{opportunity_id}/business-plan`

Creates a deterministic business plan from a stored opportunity.

Request:

```json
{
  "brand_id": null,
  "brand_name": "WorkspaceHQ",
  "user_constraints": {
    "monthly_budget": 500,
    "hours_per_week": 8,
    "target_monthly_revenue": 1000
  }
}
```

Response: `BusinessPlanResponse`.

The endpoint uses existing Opportunity scores and evidence. It does not call OpenAI in this sprint.

## Brands

### `POST /brands`

Creates a brand.

### `GET /brands`

Lists brands.

### `GET /brands/{brand_id}`

Returns one brand.

## Business Plans

### `GET /business-plans`

Lists business plans with basic `offset` and `limit` pagination.

### `GET /business-plans/{business_plan_id}`

Returns one business plan.
