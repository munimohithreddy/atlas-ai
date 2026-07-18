"use client";

import { FormEvent, useMemo, useState } from "react";

type Recommendation = "BUILD" | "WATCH" | "SKIP";

type PortfolioResult = {
  rank: number;
  topic: string;
  business_score: number;
  recommendation: Recommendation;
  confidence: number;
  demand_score: number;
  competition_score: number;
  buyer_intent_score: number;
  affiliate_score: number;
  pinterest_score: number;
  seo_score: number;
};

type PortfolioResponse = {
  results: PortfolioResult[];
};

type BusinessPlan = {
  id: number;
  opportunity_id: number;
  brand_id: number | null;
  primary_monetization: string;
  secondary_monetization: string | null;
  primary_acquisition_channel: string;
  secondary_acquisition_channels: string[];
  recommended_assets: string[];
  target_audience: string;
  value_proposition: string;
  revenue_low_monthly: number;
  revenue_high_monthly: number;
  revenue_confidence_score: number;
  effort_level: string;
  estimated_launch_days: number;
  recommendation_summary: string;
  next_action: string;
  status: string;
};

type CampaignTask = {
  id: number;
  campaign_id: number;
  title: string;
  description: string | null;
  category: string;
  status: string;
  priority: string;
  estimated_hours: number;
  depends_on_task_id: number | null;
  order_index: number;
};

type CampaignAsset = {
  id: number;
  campaign_id: number;
  asset_type: string;
  title: string;
  channel: string;
  status: string;
  planned_quantity: number;
  generated_quantity: number;
  published_quantity: number;
};

type CampaignDetail = {
  id: number;
  business_plan_id: number;
  brand_id: number | null;
  opportunity_id: number;
  name: string;
  slug: string;
  goal: string;
  status: string;
  priority: string;
  expected_monthly_revenue: number;
  estimated_build_hours: number;
  launch_target_date: string | null;
  approved_at: string | null;
  tasks: CampaignTask[];
  assets: CampaignAsset[];
};

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

export default function DashboardPage() {
  const [niche, setNiche] = useState("");
  const [topicsInput, setTopicsInput] = useState(
    "best espresso machines\nhome office ideas\nstanding desk accessories",
  );
  const [results, setResults] = useState<PortfolioResult[]>([]);
  const [plansByTopic, setPlansByTopic] = useState<Record<string, BusinessPlan>>({});
  const [campaignsByPlanId, setCampaignsByPlanId] = useState<Record<number, CampaignDetail>>({});
  const [isLoading, setIsLoading] = useState(false);
  const [planningTopic, setPlanningTopic] = useState("");
  const [campaignTopic, setCampaignTopic] = useState("");
  const [error, setError] = useState("");

  const topicCount = useMemo(
    () => normalizeTopics(topicsInput).length,
    [topicsInput],
  );

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");

    const topics = normalizeTopics(topicsInput);
    if (topics.length === 0) {
      setResults([]);
      setError("Enter at least one topic to evaluate.");
      return;
    }

    setIsLoading(true);
    try {
      const response = await fetch(
        `${API_BASE_URL}/api/v1/opportunities/portfolio`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            topics,
            niche: niche.trim() || null,
          }),
        },
      );

      if (!response.ok) {
        const message = await readErrorMessage(response);
        throw new Error(message);
      }

      const payload = (await response.json()) as PortfolioResponse;
      setResults(payload.results);
    } catch (caughtError) {
      setResults([]);
      setError(
        caughtError instanceof Error
          ? caughtError.message
          : "Portfolio evaluation failed.",
      );
    } finally {
      setIsLoading(false);
    }
  }

  async function handleCreateBusinessPlan(topic: string) {
    setError("");
    setPlanningTopic(topic);

    const response = await fetch(`${API_BASE_URL}/api/v1/opportunities/evaluate`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        topic,
        niche: niche.trim() || null,
      }),
    });

    if (!response.ok) {
      const message = await readErrorMessage(response);
      throw new Error(message);
    }

    const opportunity = (await response.json()) as { id: number };
    const planResponse = await fetch(
      `${API_BASE_URL}/api/v1/opportunities/${opportunity.id}/business-plan`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_constraints: {
            monthly_budget: null,
            hours_per_week: null,
            target_monthly_revenue: null,
          },
        }),
      },
    );

    if (!planResponse.ok) {
      const message = await readErrorMessage(planResponse);
      throw new Error(message);
    }

    const plan = (await planResponse.json()) as BusinessPlan;
    setPlansByTopic((current) => ({ ...current, [topic]: plan }));
    setPlanningTopic("");
  }

  async function handleCreateCampaign(topic: string, plan: BusinessPlan) {
    setError("");
    setCampaignTopic(topic);

    const response = await fetch(`${API_BASE_URL}/api/v1/campaigns`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        business_plan_id: plan.id,
        goal: plan.next_action,
        priority: "medium",
      }),
    });

    if (!response.ok) {
      const message = await readErrorMessage(response);
      throw new Error(message);
    }

    const campaign = (await response.json()) as CampaignDetail;
    const detailResponse = await fetch(
      `${API_BASE_URL}/api/v1/campaigns/${campaign.id}`,
    );

    if (!detailResponse.ok) {
      const message = await readErrorMessage(detailResponse);
      throw new Error(message);
    }

    const detail = (await detailResponse.json()) as CampaignDetail;
    setCampaignsByPlanId((current) => ({ ...current, [plan.id]: detail }));
    setCampaignTopic("");
  }

  return (
    <main className="dashboard-shell">
      <section className="workspace">
        <div className="header-row">
          <div>
            <p className="eyebrow">Founder Dashboard</p>
            <h1>Atlas AI</h1>
          </div>
          <div className="status-chip">{topicCount} unique topics</div>
        </div>

        <form className="control-panel" onSubmit={handleSubmit}>
          <label className="field">
            <span>Niche</span>
            <input
              type="text"
              value={niche}
              onChange={(event) => setNiche(event.target.value)}
              placeholder="affiliate, coffee, software..."
            />
          </label>

          <label className="field">
            <span>Topics</span>
            <textarea
              value={topicsInput}
              onChange={(event) => setTopicsInput(event.target.value)}
              rows={8}
              placeholder="One topic per line"
            />
          </label>

          <div className="action-row">
            <button type="submit" disabled={isLoading}>
              {isLoading ? "Evaluating..." : "Evaluate Portfolio"}
            </button>
            {error ? <p className="error-state">{error}</p> : null}
          </div>
        </form>

        <section className="results-panel" aria-live="polite">
          {results.length === 0 && !isLoading ? (
            <div className="empty-state">Portfolio results will appear here.</div>
          ) : null}

          {results.map((result) => (
            <article className="result-row" key={`${result.rank}-${result.topic}`}>
              <div className="rank-cell">#{result.rank}</div>
              <div className="topic-cell">
                <div className="topic-header">
                  <h2>{result.topic}</h2>
                  <span
                    className={`recommendation-badge recommendation-${result.recommendation.toLowerCase()}`}
                  >
                    {result.recommendation}
                  </span>
                </div>
                <div className="score-grid">
                  <Metric label="Business" value={result.business_score} />
                  <Metric label="Confidence" value={result.confidence} />
                  <Metric label="Demand" value={result.demand_score} />
                  <Metric label="Competition" value={result.competition_score} />
                  <Metric label="Buyer Intent" value={result.buyer_intent_score} />
                  <Metric label="Affiliate" value={result.affiliate_score} />
                  <Metric label="Pinterest" value={result.pinterest_score} />
                  <Metric label="SEO" value={result.seo_score} />
                </div>
                <div className="plan-summary">
                  {plansByTopic[result.topic] ? (
                    <>
                      <p>
                        Monetization: {plansByTopic[result.topic].primary_monetization}
                      </p>
                      <p>
                        Primary channel:{" "}
                        {plansByTopic[result.topic].primary_acquisition_channel}
                      </p>
                      <p>
                        Revenue: $
                        {plansByTopic[result.topic].revenue_low_monthly} - $
                        {plansByTopic[result.topic].revenue_high_monthly} / month
                      </p>
                      <p>Effort: {plansByTopic[result.topic].effort_level}</p>
                      <p>
                        Assets: {plansByTopic[result.topic].recommended_assets.join(", ")}
                      </p>
                      <p>Next: {plansByTopic[result.topic].next_action}</p>
                      <button
                        className="plan-button"
                        type="button"
                        disabled={campaignTopic === result.topic}
                        onClick={async () => {
                          try {
                            await handleCreateCampaign(
                              result.topic,
                              plansByTopic[result.topic],
                            );
                          } catch (caughtError) {
                            setError(
                              caughtError instanceof Error
                                ? caughtError.message
                                : "Campaign creation failed.",
                            );
                          }
                        }}
                      >
                        {campaignTopic === result.topic ? "Creating Campaign..." : "Create Campaign"}
                      </button>
                    </>
                  ) : null}
                </div>
                <button
                  className="plan-button"
                  type="button"
                  disabled={planningTopic === result.topic}
                  onClick={async () => {
                    try {
                      await handleCreateBusinessPlan(result.topic);
                    } catch (caughtError) {
                      setError(
                        caughtError instanceof Error
                          ? caughtError.message
                          : "Business plan creation failed.",
                      );
                    }
                  }}
                >
                  {planningTopic === result.topic ? "Creating..." : "Create Business Plan"}
                </button>
              </div>
            </article>
          ))}
        </section>

        {Object.values(campaignsByPlanId).length > 0 ? (
          <section className="campaign-detail-panel">
            {Object.values(campaignsByPlanId).map((campaign) => {
              const nextTask = campaign.tasks.find((task) => task.status === "pending");
              return (
                <article className="campaign-card" key={campaign.id}>
                  <h2>{campaign.name}</h2>
                  <p>Status: {campaign.status}</p>
                  <p>Goal: {campaign.goal}</p>
                  <p>Expected revenue: ${campaign.expected_monthly_revenue}/month</p>
                  <p>Estimated build hours: {campaign.estimated_build_hours}</p>
                  <p>Task count: {campaign.tasks.length}</p>
                  <p>Asset count: {campaign.assets.length}</p>
                  <p>Next pending task: {nextTask ? nextTask.title : "None"}</p>
                  <div className="campaign-lists">
                    <div>
                      <h3>Tasks</h3>
                      <ol>
                        {campaign.tasks
                          .slice()
                          .sort((a, b) => a.order_index - b.order_index)
                          .map((task) => (
                            <li key={task.id}>
                              {task.order_index}. {task.title} ({task.category})
                            </li>
                          ))}
                      </ol>
                    </div>
                    <div>
                      <h3>Planned assets</h3>
                      <ul>
                        {campaign.assets.map((asset) => (
                          <li key={asset.id}>
                            {asset.title} ({asset.asset_type}, {asset.channel})
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </article>
              );
            })}
          </section>
        ) : null}
      </section>
    </main>
  );
}

function Metric({ label, value }: { label: string; value: number }) {
  return (
    <div className="metric">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

function normalizeTopics(input: string): string[] {
  const seenTopics = new Set<string>();
  const topics: string[] = [];

  for (const line of input.split("\n")) {
    const topic = line.trim();
    const key = topic.toLowerCase();

    if (topic && !seenTopics.has(key)) {
      topics.push(topic);
      seenTopics.add(key);
    }
  }

  return topics;
}

async function readErrorMessage(response: Response): Promise<string> {
  try {
    const payload = (await response.json()) as { detail?: unknown };
    if (typeof payload.detail === "string") {
      return payload.detail;
    }
  } catch {
    return `Request failed with status ${response.status}.`;
  }

  return `Request failed with status ${response.status}.`;
}
