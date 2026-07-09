# Atlas AI API

Base path: `/api/v1`

## Health

### `GET /health`

Returns application, database, and Redis health status.

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

Evaluates and stores an opportunity from topic and optional niche only. Sprint 004 uses the mock research provider; no external research APIs are called.

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

### `GET /opportunities`

Lists stored opportunities in newest-first order.
