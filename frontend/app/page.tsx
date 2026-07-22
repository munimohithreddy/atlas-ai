"use client";

import { FormEvent, useEffect, useMemo, useState } from "react";

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
  started_at: string | null;
  completed_at: string | null;
  blocked_reason: string | null;
  completion_notes: string | null;
  actual_hours: number | null;
  assigned_to: string | null;
  due_date: string | null;
  depends_on_task_id: number | null;
  order_index: number;
};

type CampaignAsset = {
  id: number;
  campaign_id: number;
  campaign_task_id: number | null;
  asset_type: string;
  title: string;
  description: string | null;
  channel: string;
  status: string;
  priority: string;
  content_brief: string | null;
  target_audience: string | null;
  primary_keyword: string | null;
  secondary_keywords: string | null;
  call_to_action: string | null;
  assigned_to: string | null;
  estimated_hours: number | null;
  actual_hours: number | null;
  due_date: string | null;
  started_at: string | null;
  completed_at: string | null;
  blocked_reason: string | null;
  review_notes: string | null;
  rejection_reason: string | null;
  approved_at: string | null;
  order_index: number;
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
  total_assets: number;
  planned_assets: number;
  queued_assets: number;
  in_production_assets: number;
  review_assets: number;
  approved_assets: number;
  ready_to_publish_assets: number;
  blocked_assets: number;
  rejected_assets: number;
  asset_completion_percentage: number;
  progress: {
    total_tasks: number;
    completed_tasks: number;
    active_tasks: number;
    blocked_tasks: number;
    cancelled_tasks: number;
    completion_percentage: number;
    next_ready_task: { id: number; title: string; status: string; order_index: number } | null;
    has_blockers: boolean;
  };
  tasks: CampaignTask[];
  assets: CampaignAsset[];
};

type QueueGroupKey = "needs_attention" | "ready_to_start" | "in_progress" | "waiting_for_review" | "ready_to_publish";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

const taskStatusLabel: Record<string, string> = {
  pending: "Waiting on dependency",
  ready: "Ready",
  in_progress: "In progress",
  blocked: "Blocked",
  review: "Waiting for review",
  completed: "Completed",
  cancelled: "Cancelled",
};

const assetStatusLabel: Record<string, string> = {
  planned: "Planned",
  queued: "Ready to start",
  in_production: "In progress",
  review: "Waiting for review",
  approved: "Approved",
  ready_to_publish: "Ready to publish",
  blocked: "Blocked",
  rejected: "Needs revision",
  cancelled: "Cancelled",
};

const taskActionLabel: Record<string, string> = {
  start: "Start work",
  complete: "Complete",
  block: "Block",
  unblock: "Unblock",
  review: "Send for review",
  reopen: "Reopen",
  cancel: "Cancel",
};

const assetActionLabel: Record<string, string> = {
  queue: "Add to queue",
  start: "Start production",
  "submit-for-review": "Send for review",
  approve: "Approve",
  reject: "Request changes",
  resubmit: "Resume production",
  "mark-ready-to-publish": "Confirm ready to publish",
  unblock: "Unblock",
  reopen: "Reopen",
  cancel: "Cancel",
};

export default function DashboardPage() {
  const [niche, setNiche] = useState("");
  const [topicsInput, setTopicsInput] = useState(
    "best espresso machines\nhome office ideas\nstanding desk accessories",
  );
  const [results, setResults] = useState<PortfolioResult[]>([]);
  const [plansByTopic, setPlansByTopic] = useState<Record<string, BusinessPlan>>({});
  const [campaignsByPlanId, setCampaignsByPlanId] = useState<Record<number, CampaignDetail>>({});
  const [activeTabByCampaignId, setActiveTabByCampaignId] = useState<Record<number, "overview" | "tasks" | "assets" | "activity">>({});
  const [selectedCampaignId, setSelectedCampaignId] = useState<number | null>(null);
  const [queueAssets, setQueueAssets] = useState<CampaignAsset[]>([]);
  const [queueFilters, setQueueFilters] = useState({
    campaign_id: "",
    channel: "",
    priority: "",
    status: "",
    assigned_to: "",
  });
  const [taskActualHours, setTaskActualHours] = useState<Record<number, string>>({});
  const [taskNotes, setTaskNotes] = useState<Record<number, string>>({});
  const [assetBusy, setAssetBusy] = useState<string>("");
  const [isLoading, setIsLoading] = useState(false);
  const [planningTopic, setPlanningTopic] = useState("");
  const [campaignTopic, setCampaignTopic] = useState("");
  const [error, setError] = useState("");

  const topicCount = useMemo(() => normalizeTopics(topicsInput).length, [topicsInput]);

  useEffect(() => {
    void loadExistingCampaigns();
  }, []);

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
      const response = await fetch(`${API_BASE_URL}/api/v1/opportunities/portfolio`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topics, niche: niche.trim() || null }),
      });
      if (!response.ok) throw new Error(await readErrorMessage(response));
      const payload = (await response.json()) as PortfolioResponse;
      setResults(payload.results);
    } catch (caughtError) {
      setResults([]);
      setError(caughtError instanceof Error ? caughtError.message : "Portfolio evaluation failed.");
    } finally {
      setIsLoading(false);
    }
  }

  async function handleCreateBusinessPlan(topic: string) {
    setError("");
    setPlanningTopic(topic);
    try {
      const opportunityResponse = await fetch(`${API_BASE_URL}/api/v1/opportunities/evaluate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic, niche: niche.trim() || null }),
      });
      if (!opportunityResponse.ok) throw new Error(await readErrorMessage(opportunityResponse));

      const opportunity = (await opportunityResponse.json()) as { id: number };
      const planResponse = await fetch(`${API_BASE_URL}/api/v1/opportunities/${opportunity.id}/business-plan`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_constraints: { monthly_budget: null, hours_per_week: null, target_monthly_revenue: null },
        }),
      });
      if (!planResponse.ok) throw new Error(await readErrorMessage(planResponse));

      const plan = (await planResponse.json()) as BusinessPlan;
      setPlansByTopic((current) => ({ ...current, [topic]: plan }));
    } catch (caughtError) {
      setError(caughtError instanceof Error ? caughtError.message : "Business plan creation failed.");
    } finally {
      setPlanningTopic("");
    }
  }

  async function handleCreateCampaign(topic: string, plan: BusinessPlan) {
    setError("");
    setCampaignTopic(topic);
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/campaigns`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ business_plan_id: plan.id, goal: plan.next_action, priority: "medium" }),
      });
      if (!response.ok) {
        const message = await readErrorMessage(response);
        if (message.toLowerCase().includes("already exists")) {
          await loadExistingCampaigns();
          return;
        }
        throw new Error(message);
      }

      const campaign = (await response.json()) as CampaignDetail;
      const detail = await loadCampaignDetail(campaign.id);
      setCampaignsByPlanId((current) => ({ ...current, [plan.id]: detail }));
    } catch (caughtError) {
      setError(caughtError instanceof Error ? caughtError.message : "Campaign creation failed.");
    } finally {
      setCampaignTopic("");
    }
  }

  async function loadCampaignDetail(campaignId: number) {
    const response = await fetch(`${API_BASE_URL}/api/v1/campaigns/${campaignId}`);
    if (!response.ok) throw new Error(await readErrorMessage(response));
    return (await response.json()) as CampaignDetail;
  }

  async function loadExistingCampaigns() {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/campaigns`);
      if (!response.ok) return;
      const campaigns = (await response.json()) as Array<{ id: number; business_plan_id: number }>;
      const details = await Promise.all(campaigns.map((campaign) => loadCampaignDetail(campaign.id)));
      setCampaignsByPlanId(
        details.reduce<Record<number, CampaignDetail>>((current, campaign) => {
          current[campaign.business_plan_id] = campaign;
          return current;
        }, {}),
      );
    } catch {
      // Ignore startup refresh issues; the rest of the dashboard still works.
    }
  }

  async function refreshCampaign(campaignId: number) {
    const detail = await loadCampaignDetail(campaignId);
    setCampaignsByPlanId((current) => ({ ...current, [detail.business_plan_id]: detail }));
    return detail;
  }

  async function handleTaskAction(
    campaignId: number,
    taskId: number,
    action: "start" | "block" | "unblock" | "review" | "complete" | "cancel" | "reopen",
  ) {
    if (["cancel", "reopen"].includes(action) && !window.confirm(`Are you sure you want to ${taskActionLabel[action]} this task?`)) return;

    setError("");
    try {
      const payloadByAction: Record<string, unknown> = {
        block: { blocked_reason: window.prompt("Why is this task blocked?", "Blocked pending dependency or review.") ?? "" },
        complete: {
          completion_notes: taskNotes[taskId] || "Task completed in the dashboard.",
          actual_hours:
            taskActualHours[taskId] === undefined || taskActualHours[taskId] === ""
              ? null
              : Number(taskActualHours[taskId]),
        },
        reopen: { reason: window.prompt("Why reopen this task?", "Reopened from the dashboard.") ?? "" },
      };

      const response = await fetch(`${API_BASE_URL}/api/v1/campaigns/${campaignId}/tasks/${taskId}/${action}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: action in payloadByAction ? JSON.stringify(payloadByAction[action]) : undefined,
      });
      if (!response.ok) throw new Error(await readErrorMessage(response));
      await refreshCampaign(campaignId);
    } catch (caughtError) {
      setError(buildTaskErrorMessage(caughtError, action));
      console.error(caughtError);
    }
  }

  async function handleAssetAction(
    campaignId: number,
    assetId: number,
    action:
      | "queue"
      | "start"
      | "submit-for-review"
      | "approve"
      | "reject"
      | "resubmit"
      | "mark-ready-to-publish"
      | "unblock"
      | "reopen"
      | "cancel",
  ) {
    const confirmActions = new Set(["reject", "cancel", "reopen", "mark-ready-to-publish"]);
    if (confirmActions.has(action) && !window.confirm(`Are you sure you want to ${assetActionLabel[action]} this asset?`)) return;

    setAssetBusy(`${campaignId}:${assetId}:${action}`);
    setError("");
    try {
      const payloadByAction: Record<string, unknown> = {
        block: { blocked_reason: window.prompt("Why is this asset blocked?", "Blocked pending review or dependency.") ?? "" },
        reject: {
          review_notes: window.prompt("Review notes", "Needs revision before approval.") ?? "",
          rejection_reason: window.prompt("Reason for changes", "Please revise the copy.") ?? "",
        },
      };

      const response = await fetch(
        `${API_BASE_URL}/api/v1/campaigns/${campaignId}/assets/${assetId}/${action}`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: action in payloadByAction ? JSON.stringify(payloadByAction[action]) : undefined,
        },
      );
      if (!response.ok) throw new Error(await readErrorMessage(response));
      await refreshCampaign(campaignId);
    } catch (caughtError) {
      setError(buildAssetErrorMessage(caughtError, action));
      console.error(caughtError);
    } finally {
      setAssetBusy("");
    }
  }

  async function loadAssetQueue() {
    const params = new URLSearchParams();
    for (const [key, value] of Object.entries(queueFilters)) {
      if (value.trim()) params.set(key, value.trim());
    }
    const response = await fetch(`${API_BASE_URL}/api/v1/asset-production-queue?${params.toString()}`);
    if (!response.ok) throw new Error(await readErrorMessage(response));
    setQueueAssets((await response.json()) as CampaignAsset[]);
  }

  const campaigns = Object.values(campaignsByPlanId);
  const selectedCampaign =
    campaigns.find((campaign) => campaign.id === selectedCampaignId) ?? campaigns[0] ?? null;
  const queueGroups = groupQueueAssets(queueAssets);

  return (
    <main className="dashboard-shell">
      <section className="workspace">
        <header className="hero-card">
          <div className="header-row">
            <div>
              <p className="eyebrow">Founder workspace</p>
              <h1>Atlas AI</h1>
              <p className="hero-copy">
                Pick opportunities, shape a campaign, and move work forward with one clear next action.
              </p>
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
              {error ? <p className="error-state">{error}</p> : <p className="helper-copy">Use the dashboard to decide what to build next.</p>}
            </div>
          </form>
        </header>

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
                  <span className={`recommendation-badge recommendation-${result.recommendation.toLowerCase()}`}>
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
                      <p>Monetization: {plansByTopic[result.topic].primary_monetization}</p>
                      <p>Primary channel: {plansByTopic[result.topic].primary_acquisition_channel}</p>
                      <p>
                        Revenue: ${plansByTopic[result.topic].revenue_low_monthly} - $
                        {plansByTopic[result.topic].revenue_high_monthly} / month
                      </p>
                      <p>Effort: {plansByTopic[result.topic].effort_level}</p>
                      <p>Assets: {plansByTopic[result.topic].recommended_assets.join(", ")}</p>
                      <p>Next: {plansByTopic[result.topic].next_action}</p>
                      <button
                        className="plan-button"
                        type="button"
                        disabled={campaignTopic === result.topic}
                        onClick={async () => handleCreateCampaign(result.topic, plansByTopic[result.topic])}
                      >
                        {campaignTopic === result.topic ? "Creating Campaign..." : "Create Campaign"}
                      </button>
                    </>
                  ) : (
                    <>
                      <p>Nothing planned yet.</p>
                      <button
                        className="plan-button"
                        type="button"
                        disabled={planningTopic === result.topic}
                        onClick={async () => handleCreateBusinessPlan(result.topic)}
                      >
                        {planningTopic === result.topic ? "Creating..." : "Create Business Plan"}
                      </button>
                    </>
                  )}
                </div>
              </div>
            </article>
          ))}
        </section>

        <section className="workspace-card">
          <article className="campaign-selector">
            <div>
              <p className="eyebrow">Your campaigns</p>
              <h2>Workspace</h2>
              <p className="helper-copy">Choose one campaign to work on. The page stays focused on that campaign only.</p>
            </div>
            <div className="campaign-selector-list">
              {campaigns.length === 0 ? (
                <div className="empty-state compact">Create a campaign to see it here.</div>
              ) : (
                campaigns.map((campaign) => (
                  <button
                    key={campaign.id}
                    type="button"
                    className={selectedCampaign?.id === campaign.id ? "campaign-chip campaign-chip-active" : "campaign-chip"}
                    onClick={() => setSelectedCampaignId(campaign.id)}
                  >
                    <strong>{campaign.name}</strong>
                    <span>{statusLabel(campaign.status)} · {campaign.progress.completion_percentage}% complete</span>
                  </button>
                ))
              )}
            </div>
          </article>
        </section>

        {selectedCampaign ? (
          <CampaignWorkspace
            campaign={selectedCampaign}
            activeTab={activeTabByCampaignId[selectedCampaign.id] ?? "overview"}
            onSelectTab={(tab) =>
              setActiveTabByCampaignId((current) => ({
                ...current,
                [selectedCampaign.id]: tab,
              }))
            }
            onPrimaryAction={() =>
              setActiveTabByCampaignId((current) => ({
                ...current,
                [selectedCampaign.id]: "overview",
              }))
            }
            handleTaskAction={handleTaskAction}
            handleAssetAction={handleAssetAction}
            setTaskActualHours={setTaskActualHours}
            setTaskNotes={setTaskNotes}
            assetBusy={assetBusy}
          />
        ) : (
          <section className="workspace-card">
            <div className="empty-state">Create or select a campaign to open the workspace.</div>
          </section>
        )}

        <section className="workspace-card">
          <article className="campaign-hero">
            <div>
              <p className="eyebrow">Production queue</p>
              <h2>Asset Production Queue</h2>
              <p className="helper-copy">
                Review the highest-priority work first, grouped by what needs attention and what can move now.
              </p>
            </div>
            <button type="button" className="primary-action" onClick={() => loadAssetQueue().catch((caughtError) => setError(caughtError instanceof Error ? caughtError.message : "Queue load failed."))}>
              Load Queue
            </button>
          </article>

          <div className="field-grid">
            <label className="field"><span>Campaign</span><input value={queueFilters.campaign_id} onChange={(event) => setQueueFilters((current) => ({ ...current, campaign_id: event.target.value }))} /></label>
            <label className="field"><span>Channel</span><input value={queueFilters.channel} onChange={(event) => setQueueFilters((current) => ({ ...current, channel: event.target.value }))} /></label>
            <label className="field"><span>Priority</span><input value={queueFilters.priority} onChange={(event) => setQueueFilters((current) => ({ ...current, priority: event.target.value }))} /></label>
            <label className="field"><span>Status</span><input value={queueFilters.status} onChange={(event) => setQueueFilters((current) => ({ ...current, status: event.target.value }))} /></label>
            <label className="field"><span>Assigned user</span><input value={queueFilters.assigned_to} onChange={(event) => setQueueFilters((current) => ({ ...current, assigned_to: event.target.value }))} /></label>
          </div>

          {queueAssets.length === 0 ? (
            <div className="empty-state">No assets are currently in the production queue.</div>
          ) : (
            <div className="status-groups">
              {queueGroupOrder.map((group) => (
                <div key={group} className="group-column">
                  <h3>{queueGroupLabel[group]}</h3>
                  {queueGroups[group].length === 0 ? (
                    <div className="empty-state compact">{emptyQueueMessage(group)}</div>
                  ) : (
                    queueGroups[group].map((asset) => (
                      <article className="workflow-card" key={asset.id}>
                        <div className="workflow-card-header">
                          <div>
                            <h4>{asset.title}</h4>
                            <p className="helper-copy">
                              {assetStatusLabel[asset.status] ?? asset.status} · {asset.asset_type} · {asset.channel}
                            </p>
                          </div>
                          <span className="status-badge">{asset.priority}</span>
                        </div>
                        <div className="detail-grid">
                          <Info label="Campaign" value={`#${asset.campaign_id}`} />
                          <Info label="Due date" value={asset.due_date ? formatDate(asset.due_date) : "Not set"} />
                          <Info label="Assigned user" value={asset.assigned_to ?? "Unassigned"} />
                          <Info label="Next action" value={nextQueueActionLabel(asset)} />
                        </div>
                      </article>
                    ))
                  )}
                </div>
              ))}
            </div>
          )}
        </section>
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

function Kpi({ label, value }: { label: string; value: string }) {
  return (
    <div className="kpi">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

function Info({ label, value }: { label: string; value: string }) {
  return (
    <div className="info">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

function ProgressBar({ value }: { value: number }) {
  return (
    <div className="progress-shell" aria-label={`Campaign completion ${value}%`}>
      <div className="progress-fill" style={{ width: `${Math.min(Math.max(value, 0), 100)}%` }} />
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

function statusLabel(status: string): string {
  return {
    planning: "Planning",
    ready: "Ready",
    approved: "Approved",
    building: "Building",
    archived: "Archived",
  }[status] ?? status;
}

function tabLabel(tab: "overview" | "tasks" | "assets" | "activity"): string {
  return { overview: "Overview", tasks: "Tasks", assets: "Assets", activity: "Activity" }[tab];
}

function formatDate(value: string): string {
  return new Date(value).toLocaleDateString();
}

function dependencyLabel(tasks: CampaignTask[], task: CampaignTask): string {
  if (task.depends_on_task_id == null) return "None";
  const dependency = tasks.find((candidate) => candidate.id === task.depends_on_task_id);
  return dependency ? dependency.title : `Task #${task.depends_on_task_id}`;
}

function linkedTaskLabel(tasks: CampaignTask[], taskId: number | null): string {
  if (taskId == null) return "None";
  return tasks.find((task) => task.id === taskId)?.title ?? `Task #${taskId}`;
}

function primaryTaskAction(task: CampaignTask): string {
  if (task.status === "pending") return "Waiting on dependency";
  if (task.status === "ready") return "Start work";
  if (task.status === "in_progress") return "Complete";
  if (task.status === "blocked") return "Unblock";
  if (task.status === "review") return "Complete";
  if (task.status === "completed") return "View details";
  if (task.status === "cancelled") return "Reopen";
  return "View details";
}

function openTaskAction(
  campaignId: number,
  task: CampaignTask,
  handleTaskActionFn: typeof handleTaskActionProxy,
  setTaskActualHoursFn: React.Dispatch<React.SetStateAction<Record<number, string>>>,
  setTaskNotesFn: React.Dispatch<React.SetStateAction<Record<number, string>>>,
) {
  if (task.status === "ready") {
    handleTaskActionFn(campaignId, task.id, "start");
    return;
  }
  if (task.status === "blocked") {
    handleTaskActionFn(campaignId, task.id, "unblock");
    return;
  }
  if (task.status === "in_progress" || task.status === "review") {
    const hours = window.prompt("Actual hours", task.actual_hours?.toString() ?? "");
    if (hours !== null) setTaskActualHoursFn((current) => ({ ...current, [task.id]: hours }));
    const notes = window.prompt("Completion notes", task.completion_notes ?? "");
    if (notes !== null) setTaskNotesFn((current) => ({ ...current, [task.id]: notes }));
    handleTaskActionFn(campaignId, task.id, "complete");
    return;
  }
  if (task.status === "cancelled") {
    handleTaskActionFn(campaignId, task.id, "reopen");
  }
}

function handleTaskActionProxy(
  campaignId: number,
  taskId: number,
  action: "start" | "block" | "unblock" | "review" | "complete" | "cancel" | "reopen",
) {
  void campaignId;
  void taskId;
  void action;
}

function buildTaskErrorMessage(caughtError: unknown, action: string): string {
  const message = caughtError instanceof Error ? caughtError.message : "Task action failed.";
  if (message.includes("Invalid") && action === "complete") {
    return "This task cannot be completed yet. Start it first or move it into review.";
  }
  if (message.includes("Invalid") && action === "start") {
    return "This task cannot start yet. It is still waiting on another task.";
  }
  return message;
}

function buildAssetErrorMessage(caughtError: unknown, action: string): string {
  const message = caughtError instanceof Error ? caughtError.message : "Asset action failed.";
  if (message.includes("Invalid") && action === "reject") {
    return "This asset cannot be rejected right now. Send it for review first.";
  }
  if (message.includes("Invalid") && action === "mark-ready-to-publish") {
    return "This asset is not approved yet. Approve it before marking it ready to publish.";
  }
  return message;
}

function nextActionPanelContent(campaign: CampaignDetail, nextTask: CampaignTask | null, nextAsset: CampaignAsset | null) {
  if (nextTask) {
    return (
      <>
        <h3>{nextTask.title}</h3>
        <p>Why it matters: it is the next task that keeps the campaign moving.</p>
        <p>Status: {taskStatusLabel[nextTask.status] ?? nextTask.status}</p>
        <p>Estimated effort: {nextTask.estimated_hours} hours</p>
        <p>Action: Start work</p>
      </>
    );
  }

  if (nextAsset) {
    return (
      <>
        <h3>{nextAsset.title}</h3>
        <p>Why it matters: it is the next asset ready to move through production.</p>
        <p>Status: {assetStatusLabel[nextAsset.status] ?? nextAsset.status}</p>
        <p>Estimated effort: {nextAsset.estimated_hours ?? "—"} hours</p>
        <p>Action: {nextQueueActionLabel(nextAsset)}</p>
      </>
    );
  }

  return (
    <>
      <h3>All available work is complete.</h3>
      <p>There is no ready task or asset right now.</p>
      <p>Status: {statusLabel(campaign.status)}</p>
      <p>Action: Check the queue or plan the next campaign update.</p>
    </>
  );
}

function launchReadinessLabel(campaign: CampaignDetail): string {
  if (campaign.status === "approved" && campaign.progress.completion_percentage === 0) return "Ready to begin";
  if (campaign.progress.blocked_tasks > 0 || campaign.blocked_assets > 0) return "Blocked";
  if (campaign.progress.completion_percentage >= 100) return "Ready for launch";
  return "In progress";
}

function topBlockers(campaign: CampaignDetail): Array<{ key: string; title: string; reason: string }> {
  const taskBlockers = campaign.tasks
    .filter((task) => task.status === "blocked")
    .map((task) => ({ key: `task-${task.id}`, title: task.title, reason: task.blocked_reason ?? "Blocked work needs attention." }));
  const assetBlockers = campaign.assets
    .filter((asset) => asset.status === "blocked" || asset.status === "rejected")
    .map((asset) => ({
      key: `asset-${asset.id}`,
      title: asset.title,
      reason: asset.blocked_reason ?? asset.rejection_reason ?? "Asset needs attention.",
    }));
  return [...taskBlockers, ...assetBlockers].slice(0, 4);
}

function recentActivity(campaign: CampaignDetail): Array<{ key: string; title: string; detail: string }> {
  return [
    { key: "progress", title: "Campaign progress", detail: `${campaign.progress.completion_percentage}% complete.` },
    { key: "tasks", title: "Task work", detail: `${campaign.progress.completed_tasks} tasks completed and ${campaign.progress.blocked_tasks} blocked.` },
    { key: "assets", title: "Asset work", detail: `${campaign.ready_to_publish_assets} assets ready to publish.` },
  ];
}

const assetGroupOrder: Array<QueueGroupKey> = [
  "needs_attention",
  "ready_to_start",
  "in_progress",
  "waiting_for_review",
  "ready_to_publish",
];

const assetGroupLabel: Record<QueueGroupKey, string> = {
  needs_attention: "Needs attention",
  ready_to_start: "Ready to start",
  in_progress: "In progress",
  waiting_for_review: "Waiting for review",
  ready_to_publish: "Ready to publish",
};

const queueGroupOrder: Array<QueueGroupKey> = assetGroupOrder;

const queueGroupLabel = assetGroupLabel;

function groupedAssets(assets: CampaignAsset[]): Record<QueueGroupKey, CampaignAsset[]> {
  const groups: Record<QueueGroupKey, CampaignAsset[]> = {
    needs_attention: [],
    ready_to_start: [],
    in_progress: [],
    waiting_for_review: [],
    ready_to_publish: [],
  };
  for (const asset of assets) {
    groups[assetGroupForStatus(asset.status)].push(asset);
  }
  return groups;
}

function groupQueueAssets(assets: CampaignAsset[]): Record<QueueGroupKey, CampaignAsset[]> {
  return groupedAssets(assets);
}

function assetGroupForStatus(status: string): QueueGroupKey {
  if (status === "planned" || status === "blocked" || status === "rejected") return "needs_attention";
  if (status === "queued") return "ready_to_start";
  if (status === "in_production") return "in_progress";
  if (status === "review") return "waiting_for_review";
  return "ready_to_publish";
}

function emptyAssetGroupMessage(group: QueueGroupKey): string {
  return {
    needs_attention: "No assets need attention right now.",
    ready_to_start: "No assets are ready to start.",
    in_progress: "No assets are in progress.",
    waiting_for_review: "Nothing is waiting for review.",
    ready_to_publish: "No assets are ready to publish.",
  }[group];
}

function emptyQueueMessage(group: QueueGroupKey): string {
  return emptyAssetGroupMessage(group);
}

function nextAssetAction(asset: CampaignAsset):
  | "queue"
  | "start"
  | "submit-for-review"
  | "approve"
  | "reject"
  | "resubmit"
  | "mark-ready-to-publish"
  | "unblock"
  | "reopen"
  | "cancel" {
  if (asset.status === "planned") return "queue";
  if (asset.status === "queued") return "start";
  if (asset.status === "in_production") return "submit-for-review";
  if (asset.status === "review") return "approve";
  if (asset.status === "approved") return "mark-ready-to-publish";
  if (asset.status === "ready_to_publish") return "mark-ready-to-publish";
  if (asset.status === "blocked") return "unblock";
  if (asset.status === "rejected") return "resubmit";
  return "reopen";
}

function nextQueueActionLabel(asset: CampaignAsset): string {
  return assetActionLabel[nextAssetAction(asset)];
}

function pickNextAsset(assets: CampaignAsset[]): CampaignAsset | null {
  return (
    assets.find((asset) => asset.status === "queued") ??
    assets.find((asset) => asset.status === "in_production") ??
    assets.find((asset) => asset.status === "review") ??
    assets.find((asset) => asset.status === "planned") ??
    null
  );
}

function primaryCampaignActionLabel(campaign: CampaignDetail, nextTask: CampaignTask | null, nextAsset: CampaignAsset | null): string {
  if (nextTask) return `Focus on ${nextTask.title}`;
  if (nextAsset) return `Advance ${nextAsset.title}`;
  if (campaign.progress.blocked_tasks > 0 || campaign.blocked_assets > 0) return "Resolve blockers";
  return "Review campaign";
}

async function readErrorMessage(response: Response): Promise<string> {
  try {
    const payload = (await response.json()) as { detail?: unknown };
    if (typeof payload.detail === "string") return payload.detail;
  } catch {
    return `Request failed with status ${response.status}.`;
  }
  return `Request failed with status ${response.status}.`;
}

function CampaignWorkspace({
  campaign,
  activeTab,
  onSelectTab,
  onPrimaryAction,
  handleTaskAction,
  handleAssetAction,
  setTaskActualHours,
  setTaskNotes,
  assetBusy,
}: {
  campaign: CampaignDetail;
  activeTab: "overview" | "tasks" | "assets" | "activity";
  onSelectTab: (tab: "overview" | "tasks" | "assets" | "activity") => void;
  onPrimaryAction: () => void;
  handleTaskAction: (
    campaignId: number,
    taskId: number,
    action: "start" | "block" | "unblock" | "review" | "complete" | "cancel" | "reopen",
  ) => void;
  handleAssetAction: (
    campaignId: number,
    assetId: number,
    action:
      | "queue"
      | "start"
      | "submit-for-review"
      | "approve"
      | "reject"
      | "resubmit"
      | "mark-ready-to-publish"
      | "unblock"
      | "reopen"
      | "cancel",
  ) => void;
  setTaskActualHours: React.Dispatch<React.SetStateAction<Record<number, string>>>;
  setTaskNotes: React.Dispatch<React.SetStateAction<Record<number, string>>>;
  assetBusy: string;
}) {
  const nextTask = campaign.progress.next_ready_task
    ? campaign.tasks.find((task) => task.id === campaign.progress.next_ready_task?.id) ?? null
    : null;
  const nextAsset = pickNextAsset(campaign.assets);

  return (
    <section className="workspace-card">
      <article className="campaign-hero">
        <div>
          <p className="eyebrow">Campaign workspace</p>
          <h2>{campaign.name}</h2>
          <p className="helper-copy">{campaign.goal}</p>
        </div>
        <div className="campaign-kpis">
          <Kpi label="Status" value={statusLabel(campaign.status)} />
          <Kpi label="Completion" value={`${campaign.progress.completion_percentage}%`} />
          <Kpi label="Launch target" value={campaign.launch_target_date ? formatDate(campaign.launch_target_date) : "Not set"} />
          <Kpi label="Expected monthly revenue" value={`$${campaign.expected_monthly_revenue}`} />
          <button type="button" className="primary-action" onClick={onPrimaryAction}>
            {primaryCampaignActionLabel(campaign, nextTask, nextAsset)}
          </button>
        </div>
      </article>

      <div className="tabs">
        {(["overview", "tasks", "assets", "activity"] as const).map((value) => (
          <button
            key={value}
            type="button"
            className={activeTab === value ? "tab tab-active" : "tab"}
            onClick={() => onSelectTab(value)}
          >
            {tabLabel(value)}
          </button>
        ))}
      </div>

      {activeTab === "overview" ? (
        <div className="workspace-grid">
          <section className="panel-card">
            <p className="eyebrow">What should I do next?</p>
            <div className="next-action-panel">{nextActionPanelContent(campaign, nextTask, nextAsset)}</div>
          </section>

          <section className="panel-card">
            <p className="eyebrow">Campaign progress</p>
            <ProgressBar value={campaign.progress.completion_percentage} />
            <div className="compact-grid">
              <Kpi label="Tasks complete" value={`${campaign.progress.completed_tasks}/${campaign.progress.total_tasks}`} />
              <Kpi label="Assets complete" value={`${campaign.approved_assets + campaign.ready_to_publish_assets}/${campaign.total_assets}`} />
              <Kpi label="Blocked items" value={`${campaign.progress.blocked_tasks + campaign.blocked_assets}`} />
              <Kpi label="Launch readiness" value={launchReadinessLabel(campaign)} />
            </div>
          </section>

          <section className="panel-card">
            <p className="eyebrow">Top blockers</p>
            {topBlockers(campaign).length === 0 ? (
              <div className="empty-state compact">No work is currently blocked.</div>
            ) : (
              <ul className="stack-list">
                {topBlockers(campaign).map((item) => (
                  <li key={item.key}>
                    <strong>{item.title}</strong>
                    <span>{item.reason}</span>
                  </li>
                ))}
              </ul>
            )}
          </section>

          <section className="panel-card">
            <p className="eyebrow">Recent activity</p>
            <ul className="stack-list">
              {recentActivity(campaign).map((item) => (
                <li key={item.key}>
                  <strong>{item.title}</strong>
                  <span>{item.detail}</span>
                </li>
              ))}
            </ul>
          </section>
        </div>
      ) : null}

      {activeTab === "tasks" ? (
        <section className="panel-card">
          <p className="helper-copy">Tasks are shown in execution order. The primary button reflects the next valid step.</p>
          {campaign.tasks.length === 0 ? (
            <div className="empty-state">No tasks have been created yet.</div>
          ) : (
            <div className="card-list">
              {campaign.tasks
                .slice()
                .sort((a, b) => a.order_index - b.order_index)
                .map((task) => (
                  <article className="workflow-card" key={task.id}>
                    <div className="workflow-card-header">
                      <div>
                        <p className="eyebrow">Task {task.order_index}</p>
                        <h3>{task.title}</h3>
                        <p className="helper-copy">{task.description ?? "No description provided."}</p>
                      </div>
                      <span className="status-badge">{taskStatusLabel[task.status] ?? task.status}</span>
                    </div>
                    <div className="detail-grid">
                      <Info label="Dependency" value={dependencyLabel(campaign.tasks, task)} />
                      <Info label="Estimated hours" value={String(task.estimated_hours)} />
                      <Info label="Actual hours" value={task.actual_hours == null ? "—" : String(task.actual_hours)} />
                      <Info label="Assigned user" value={task.assigned_to ?? "Unassigned"} />
                      <Info label="Due date" value={task.due_date ? formatDate(task.due_date) : "Not set"} />
                      <Info label="Status" value={taskStatusLabel[task.status] ?? task.status} />
                    </div>
                    <div className="item-actions">
                      <button
                        type="button"
                        className="secondary-action"
                        onClick={() => openTaskAction(campaign.id, task, handleTaskAction, setTaskActualHours, setTaskNotes)}
                      >
                        {primaryTaskAction(task)}
                      </button>
                    </div>
                  </article>
                ))}
            </div>
          )}
        </section>
      ) : null}

      {activeTab === "assets" ? (
        <section className="panel-card">
          <p className="helper-copy">Assets are grouped by the work stage so the team can see what needs attention and what is ready to move.</p>
          {campaign.assets.length === 0 ? (
            <div className="empty-state">No assets have been planned yet.</div>
          ) : (
            <div className="status-groups">
              {assetGroupOrder.map((group) => (
                <div key={group} className="group-column">
                  <h3>{assetGroupLabel[group]}</h3>
                  {groupedAssets(campaign.assets)[group].length === 0 ? (
                    <div className="empty-state compact">{emptyAssetGroupMessage(group)}</div>
                  ) : (
                    groupedAssets(campaign.assets)[group].map((asset) => (
                      <article className="workflow-card" key={asset.id}>
                        <div className="workflow-card-header">
                          <div>
                            <h4>{asset.title}</h4>
                            <p className="helper-copy">
                              {assetStatusLabel[asset.status] ?? asset.status} · {asset.asset_type} · {asset.channel}
                            </p>
                          </div>
                          <span className="status-badge">{asset.priority}</span>
                        </div>
                        <div className="detail-grid">
                          <Info label="Linked task" value={linkedTaskLabel(campaign.tasks, asset.campaign_task_id)} />
                          <Info label="Due date" value={asset.due_date ? formatDate(asset.due_date) : "Not set"} />
                          <Info label="Assigned user" value={asset.assigned_to ?? "Unassigned"} />
                          <Info label="Status" value={assetStatusLabel[asset.status] ?? asset.status} />
                        </div>
                        <div className="item-actions">
                          <button
                            type="button"
                            className="secondary-action"
                            disabled={assetBusy === `${campaign.id}:${asset.id}:start`}
                            onClick={() => handleAssetAction(campaign.id, asset.id, nextAssetAction(asset))}
                          >
                            {assetActionLabel[nextAssetAction(asset)]}
                          </button>
                        </div>
                      </article>
                    ))
                  )}
                </div>
              ))}
            </div>
          )}
        </section>
      ) : null}

      {activeTab === "activity" ? (
        <section className="panel-card">
          <p className="helper-copy">A simple activity feed keeps the team oriented without exposing technical terms.</p>
          <ul className="stack-list">
            <li>
              <strong>Campaign created</strong>
              <span>{campaign.name} was added to the workspace.</span>
            </li>
            <li>
              <strong>Progress updated</strong>
              <span>
                {campaign.progress.completion_percentage}% complete with {campaign.progress.blocked_tasks} blocked tasks.
              </span>
            </li>
            <li>
              <strong>Asset readiness</strong>
              <span>{campaign.ready_to_publish_assets} assets are ready to publish.</span>
            </li>
          </ul>
        </section>
      ) : null}
    </section>
  );
}
