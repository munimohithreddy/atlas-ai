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

type Opportunity = {
  id: number;
  topic: string;
  niche: string | null;
  demand_score: number;
  competition_score: number;
  buyer_intent_score: number;
  affiliate_score: number;
  pinterest_score: number;
  seo_score: number;
  opportunity_score: number;
  recommendation: string;
  reasoning: string;
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
type AssetStageKey =
  | "planned"
  | "ready_to_start"
  | "in_progress"
  | "waiting_for_review"
  | "approved"
  | "ready_to_publish"
  | "needs_revision"
  | "blocked"
  | "cancelled";
type TaskActionFn = (
  campaignId: number,
  taskId: number,
  action: "start" | "block" | "unblock" | "review" | "complete" | "cancel" | "reopen",
) => void;

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

const taskStatusLabel: Record<string, string> = {
  pending: "Waiting",
  ready: "Ready to Start",
  in_progress: "In Progress",
  blocked: "Blocked",
  review: "Waiting for Review",
  completed: "Completed",
  cancelled: "Cancelled",
};

const assetStatusLabel: Record<string, string> = {
  planned: "Planned",
  queued: "Ready to Start",
  in_production: "In Progress",
  review: "Waiting for Review",
  approved: "Approved",
  ready_to_publish: "Ready to Publish",
  blocked: "Blocked",
  rejected: "Needs revision",
  cancelled: "Cancelled",
};

const taskActionLabel: Record<string, string> = {
  start: "Start Task",
  complete: "Complete Task",
  block: "Block Task",
  unblock: "Unblock Task",
  review: "Send for Review",
  reopen: "Reopen",
  cancel: "Cancel",
};

const assetActionLabel: Record<string, string> = {
  queue: "Add to Production Queue",
  start: "Start Production",
  block: "Block Asset",
  "submit-for-review": "Send for Review",
  approve: "Approve",
  reject: "Request changes",
  resubmit: "Resume production",
  "mark-ready-to-publish": "Confirm ready to publish",
  unblock: "Unblock",
  reopen: "Reopen",
  cancel: "Cancel",
};

const glossaryTerms = [
  { term: "Opportunity", meaning: "A business idea Atlas can evaluate.", example: "Example: standing desk accessories." },
  { term: "Opportunity Score", meaning: "A summary of demand, competition, buying intent, and monetization potential.", example: "Higher scores are better candidates." },
  { term: "Demand", meaning: "How much interest appears to exist for the idea.", example: "People actively search for espresso machines." },
  { term: "Competition", meaning: "How difficult the market may be to enter.", example: "Many strong review sites means higher competition." },
  { term: "Buyer Intent", meaning: "How likely the audience is to take a revenue-related action.", example: "Best X for Y searches often show buying intent." },
  { term: "Monetization Model", meaning: "How the business is expected to make money.", example: "Affiliate, display advertising, lead generation, or digital product." },
  { term: "Business Plan", meaning: "The strategy connecting an opportunity to audience, revenue, channels, and launch work.", example: "Affiliate growth plan for standing desks." },
  { term: "Target Audience", meaning: "The people the business is built to help.", example: "Remote workers upgrading a home office." },
  { term: "Acquisition Channel", meaning: "Where visitors or customers will come from.", example: "Website SEO, Pinterest, YouTube, or email." },
  { term: "Campaign", meaning: "The execution workspace created from a business plan.", example: "Standing Desk Display Advertising Campaign." },
  { term: "Campaign Task", meaning: "A step that must be completed to move a campaign forward.", example: "Validate brand positioning." },
  { term: "Task Dependency", meaning: "A task that must finish before another task can start.", example: "Create homepage brief waits for website architecture." },
  { term: "Estimated Hours", meaning: "Expected effort before work starts.", example: "3 hours." },
  { term: "Actual Hours", meaning: "Time recorded after work is completed.", example: "1.5 hours." },
  { term: "Asset", meaning: "A deliverable required for launch.", example: "Buying guide, homepage, email capture, or lead magnet." },
  { term: "Asset Type", meaning: "The kind of deliverable being produced.", example: "Buying Guide or Comparison Page." },
  { term: "Channel", meaning: "Where the asset will be used.", example: "Website, email, Pinterest, or YouTube." },
  { term: "Priority", meaning: "How urgently the work should be handled.", example: "High priority assets are handled first." },
  { term: "Production Queue", meaning: "The global list of assets needing production or review.", example: "All campaigns' assets waiting for review." },
  { term: "Content Brief", meaning: "Instructions for producing an asset.", example: "Audience, keywords, and call to action." },
  { term: "Ready to Publish", meaning: "Approved asset state before publishing integrations exist.", example: "A buying guide approved for publication." },
  { term: "Launch Readiness", meaning: "How close a campaign is to publication based on tasks, assets, and blockers.", example: "Blocked if required assets are not approved." },
];

export default function DashboardPage() {
  const [niche, setNiche] = useState("");
  const [topicsInput, setTopicsInput] = useState(
    "best espresso machines\nhome office ideas\nstanding desk accessories",
  );
  const [results, setResults] = useState<PortfolioResult[]>([]);
  const [opportunities, setOpportunities] = useState<Opportunity[]>([]);
  const [businessPlanList, setBusinessPlanList] = useState<BusinessPlan[]>([]);
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
  const [isHydrating, setIsHydrating] = useState(true);
  const [queueLoading, setQueueLoading] = useState(false);
  const [planningTopic, setPlanningTopic] = useState("");
  const [campaignTopic, setCampaignTopic] = useState("");
  const [error, setError] = useState("");
  const [successMessage, setSuccessMessage] = useState("");
  const [activeNavId, setActiveNavId] = useState("dashboard");

  const topicCount = useMemo(() => normalizeTopics(topicsInput).length, [topicsInput]);

  useEffect(() => {
    void loadWorkspace();
    // Existing workspace hydration should only run on initial dashboard load.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setSuccessMessage("");
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
      setSuccessMessage(`Evaluated ${payload.results.length} opportunities.`);
    } catch (caughtError) {
      setResults([]);
      setError(caughtError instanceof Error ? caughtError.message : "Portfolio evaluation failed.");
    } finally {
      setIsLoading(false);
    }
  }

  async function handleCreateOpportunity() {
    setError("");
    setSuccessMessage("");
    const topic = normalizeTopics(topicsInput)[0];
    if (!topic) {
      setError("Enter one business idea to create an opportunity.");
      return;
    }

    setIsLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/opportunities/evaluate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic, niche: niche.trim() || null }),
      });
      if (!response.ok) throw new Error(await readErrorMessage(response));
      const opportunity = (await response.json()) as Opportunity;
      setOpportunities((current) => [opportunity, ...current.filter((item) => item.id !== opportunity.id)]);
      setResults((current) => [
        opportunityToResult(opportunity, current.length + 1),
        ...current.filter((item) => item.topic.toLowerCase() !== opportunity.topic.toLowerCase()),
      ]);
      setSuccessMessage(`Opportunity created: ${opportunity.topic}.`);
    } catch (caughtError) {
      setError(caughtError instanceof Error ? caughtError.message : "Opportunity creation failed.");
    } finally {
      setIsLoading(false);
    }
  }

  async function handleCreateBusinessPlan(topic: string) {
    setError("");
    setSuccessMessage("");
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
      setBusinessPlanList((current) => [plan, ...current.filter((item) => item.id !== plan.id)]);
      setSuccessMessage(`Business plan created for ${topic}.`);
    } catch (caughtError) {
      setError(caughtError instanceof Error ? caughtError.message : "Business plan creation failed.");
    } finally {
      setPlanningTopic("");
    }
  }

  async function handleCreateCampaign(topic: string, plan: BusinessPlan) {
    setError("");
    setSuccessMessage("");
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
          setSuccessMessage("Existing campaign loaded for this business plan.");
          return;
        }
        throw new Error(message);
      }

      const campaign = (await response.json()) as CampaignDetail;
      const detail = await loadCampaignDetail(campaign.id);
      setCampaignsByPlanId((current) => ({ ...current, [plan.id]: detail }));
      setSelectedCampaignId(detail.id);
      setSuccessMessage(`Campaign created: ${detail.name}.`);
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

  async function loadWorkspace() {
    setIsHydrating(true);
    await Promise.all([loadExistingOpportunities(), loadExistingBusinessPlans(), loadExistingCampaigns(), loadAssetQueue(false).catch(() => undefined)]);
    setIsHydrating(false);
  }

  async function loadExistingOpportunities() {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/opportunities`);
      if (!response.ok) return;
      setOpportunities((await response.json()) as Opportunity[]);
    } catch {
      // Ignore startup refresh issues; the rest of the dashboard still works.
    }
  }

  async function handleCreateBusinessPlanForOpportunity(opportunity: Opportunity) {
    setError("");
    setSuccessMessage("");
    setPlanningTopic(opportunity.topic);
    try {
      const existingPlan = combinedPlanList.find((plan) => plan.opportunity_id === opportunity.id);
      if (existingPlan) {
        setSuccessMessage("This opportunity already has a business plan.");
        return;
      }
      const planResponse = await fetch(`${API_BASE_URL}/api/v1/opportunities/${opportunity.id}/business-plan`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_constraints: { monthly_budget: null, hours_per_week: null, target_monthly_revenue: null },
        }),
      });
      if (!planResponse.ok) throw new Error(await readErrorMessage(planResponse));

      const plan = (await planResponse.json()) as BusinessPlan;
      setBusinessPlanList((current) => [plan, ...current.filter((item) => item.id !== plan.id)]);
      setPlansByTopic((current) => ({ ...current, [opportunity.topic]: plan }));
      setSuccessMessage(`Business plan created for ${opportunity.topic}.`);
    } catch (caughtError) {
      setError(caughtError instanceof Error ? caughtError.message : "Business plan creation failed.");
    } finally {
      setPlanningTopic("");
    }
  }

  async function loadExistingBusinessPlans() {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/business-plans`);
      if (!response.ok) return;
      const plans = (await response.json()) as BusinessPlan[];
      setBusinessPlanList(plans);
    } catch {
      // Ignore startup refresh issues; the rest of the dashboard still works.
    }
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
    setSuccessMessage("");
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
      setSuccessMessage(`Task ${taskActionLabel[action].toLowerCase()} saved.`);
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
      | "block"
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
    setSuccessMessage("");
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
      setSuccessMessage(`Asset ${assetActionLabel[action].toLowerCase()} saved.`);
    } catch (caughtError) {
      setError(buildAssetErrorMessage(caughtError, action));
      console.error(caughtError);
    } finally {
      setAssetBusy("");
    }
  }

  async function loadAssetQueue(showSuccess = true) {
    setQueueLoading(true);
    const params = new URLSearchParams();
    try {
      for (const [key, value] of Object.entries(queueFilters)) {
        if (value.trim()) params.set(key, value.trim());
      }
      const response = await fetch(`${API_BASE_URL}/api/v1/asset-production-queue?${params.toString()}`);
      if (!response.ok) throw new Error(await readErrorMessage(response));
      setQueueAssets((await response.json()) as CampaignAsset[]);
      if (showSuccess) setSuccessMessage("Production queue refreshed.");
    } finally {
      setQueueLoading(false);
    }
  }

  const campaigns = Object.values(campaignsByPlanId);
  const selectedCampaign =
    campaigns.find((campaign) => campaign.id === selectedCampaignId) ?? campaigns[0] ?? null;
  const queueGroups = groupQueueAssets(queueAssets);
  const combinedPlanList = [
    ...businessPlanList,
    ...Object.values(plansByTopic).filter((plan) => !businessPlanList.some((item) => item.id === plan.id)),
  ];
  const businessPlans = combinedPlanList.map((plan) => [topicForPlan(plan, opportunities), plan] as [string, BusinessPlan]);
  const allTasks = campaigns.flatMap((campaign) => campaign.tasks ?? []);
  const allAssets = campaigns.flatMap((campaign) => campaign.assets ?? []);
  const readyTasks = allTasks.filter((task) => task.status === "ready").length;
  const blockedTasks = allTasks.filter((task) => task.status === "blocked").length;
  const assetsWaitingForReview = allAssets.filter((asset) => asset.status === "review").length;
  const assetsReadyToPublish = allAssets.filter((asset) => asset.status === "ready_to_publish").length;
  const plansWithCampaigns = new Set(campaigns.map((campaign) => campaign.business_plan_id));
  const opportunitiesWithPlans = new Set(combinedPlanList.map((plan) => plan.opportunity_id));
  const isFirstRun = !isHydrating && opportunities.length === 0 && combinedPlanList.length === 0 && campaigns.length === 0;
  const orphanedCampaigns = campaigns.filter((campaign) => !combinedPlanList.some((plan) => plan.id === campaign.business_plan_id));
  const dashboardMetrics = [
    { label: "Opportunities", value: String(opportunities.length), detail: "Business ideas Atlas has evaluated", target: "opportunities" },
    { label: "Business plans", value: String(combinedPlanList.length), detail: "Ideas with a launch strategy", target: "business-plans" },
    {
      label: "Active campaigns",
      value: String(campaigns.filter((campaign) => !["cancelled", "completed"].includes(campaign.status)).length),
      detail: "Launch plans in progress",
      target: "campaigns",
    },
    { label: "Tasks Ready to Start", value: String(readyTasks), detail: "Campaign work that can move now", target: "campaigns" },
    { label: "Blocked Tasks", value: String(blockedTasks), detail: "Work that needs a decision", target: "campaigns" },
    { label: "Assets Waiting for Review", value: String(assetsWaitingForReview), detail: "Deliverables ready for approval", target: "production-queue" },
    { label: "Assets Ready to Publish", value: String(assetsReadyToPublish), detail: "Approved deliverables waiting for publishing", target: "production-queue" },
  ];
  const attentionItems = [
    ...campaigns
      .filter((campaign) => campaign.progress.has_blockers || campaign.blocked_assets > 0)
      .map((campaign) => ({
        key: `campaign-${campaign.id}`,
        title: campaign.name,
        detail: `${campaign.progress.blocked_tasks} blocked tasks and ${campaign.blocked_assets} blocked assets.`,
      })),
    ...allTasks
      .filter((task) => task.status === "ready")
      .slice(0, 3)
      .map((task) => ({
        key: `task-${task.id}`,
        title: task.title,
        detail: "Ready to start.",
      })),
  ].slice(0, 5);
  const dashboardAction = dashboardNextRecommendedAction({
    campaigns,
    businessPlans: combinedPlanList,
    opportunities,
    plansWithCampaigns,
    opportunitiesWithPlans,
  });
  const navigationItems = [
    { id: "dashboard", label: "Dashboard" },
    { id: "opportunities", label: "Opportunities" },
    { id: "business-plans", label: "Business Plans" },
    { id: "campaigns", label: "Campaigns" },
    { id: "production-queue", label: "Production Queue" },
    { id: "documentation", label: "Documentation" },
    { id: "settings", label: "Settings" },
  ];

  return (
    <main className="dashboard-shell">
      <div className="app-shell">
        <aside className="app-sidebar">
          <div>
            <p className="eyebrow">Atlas AI</p>
            <h1 className="sidebar-title">Launch Planner</h1>
            <p className="helper-copy">Guided business workflow</p>
          </div>
          <nav className="sidebar-nav" aria-label="Primary">
            {navigationItems.map((item) => (
              <button
                key={item.id}
                type="button"
                className={activeNavId === item.id ? "sidebar-link sidebar-link-active" : "sidebar-link"}
                onClick={() => {
                  setActiveNavId(item.id);
                  document.getElementById(item.id)?.scrollIntoView({ behavior: "smooth", block: "start" });
                }}
              >
                {item.label}
              </button>
            ))}
          </nav>
          <div className="env-chip">Development</div>
        </aside>

        <section className="workspace">
        <header id="dashboard" className="hero-card">
          <div className="topbar">
            <div className="breadcrumbs">Dashboard / Workflow / Overview</div>
            <div className="topbar-actions">
              <span className="env-chip env-chip-inline">Development</span>
              <button type="button" className="secondary-action" onClick={() => window.scrollTo({ top: 0, behavior: "smooth" })}>
                Back to top
              </button>
            </div>
          </div>
          <label className="mobile-nav-label">
            <span>Navigate workspace</span>
            <select
              className="mobile-nav"
              value={activeNavId}
              onChange={(event) => {
                setActiveNavId(event.target.value);
                document.getElementById(event.target.value)?.scrollIntoView({ behavior: "smooth", block: "start" });
              }}
            >
              {navigationItems.map((item) => (
                <option key={item.id} value={item.id}>
                  {item.label}
                </option>
              ))}
            </select>
          </label>
          <div className="header-row">
            <div>
              <p className="eyebrow">Business launch planner</p>
              <h1>Atlas AI</h1>
              <p className="hero-copy">
                Turn a business idea into an executable launch plan.
              </p>
            </div>
            <div className="status-chip">{topicCount} ideas entered</div>
          </div>

          {successMessage ? <div className="success-state">{successMessage}</div> : null}
          {orphanedCampaigns.length > 0 ? (
            <div className="warning-state">
              Development warning: {orphanedCampaigns.length} campaign records were loaded without a matching business plan. Review legacy data before trusting totals.
            </div>
          ) : null}

          {isHydrating ? (
            <div className="loading-skeleton">Loading your Atlas workspace...</div>
          ) : isFirstRun ? (
            <section className="first-run-card">
              <p className="eyebrow">Welcome to Atlas AI</p>
              <h2>Turn your first business idea into an actionable launch plan.</h2>
              <WorkflowIndicator currentStage="Opportunity" />
              <ol className="guided-list">
                <li>Create an Opportunity</li>
                <li>Review its potential</li>
                <li>Create a Business Plan</li>
                <li>Create a Campaign</li>
                <li>Complete Campaign Tasks</li>
                <li>Produce Campaign Assets</li>
                <li>Prepare Assets for Publishing</li>
              </ol>
              <IdeaForm
                niche={niche}
                topicsInput={topicsInput}
                isLoading={isLoading}
                onNicheChange={setNiche}
                onTopicsChange={setTopicsInput}
                onCreateOpportunity={handleCreateOpportunity}
                onEvaluateMultiple={handleSubmit}
              />
              <button
                type="button"
                className="secondary-action"
                onClick={() => document.getElementById("documentation")?.scrollIntoView({ behavior: "smooth", block: "start" })}
              >
                Learn How Atlas Works
              </button>
            </section>
          ) : (
            <>
              <div className="dashboard-metrics" aria-label="Workspace summary">
                {dashboardMetrics.map((metric) => (
                  <button
                    type="button"
                    className="dashboard-metric"
                    key={metric.label}
                    onClick={() => document.getElementById(metric.target)?.scrollIntoView({ behavior: "smooth", block: "start" })}
                  >
                    <span>{metric.label}</span>
                    <strong>{metric.value}</strong>
                    <p>{metric.detail}</p>
                  </button>
                ))}
              </div>

              <WorkflowIndicator currentStage="Dashboard" />

              <IdeaForm
                niche={niche}
                topicsInput={topicsInput}
                isLoading={isLoading}
                onNicheChange={setNiche}
                onTopicsChange={setTopicsInput}
                onCreateOpportunity={handleCreateOpportunity}
                onEvaluateMultiple={handleSubmit}
              />

              {error ? <p className="error-state spacious">{error}</p> : null}

              <div className="workspace-grid">
                <section className="panel-card">
                  <p className="eyebrow">Next Recommended Action</p>
                  <div className="next-action-panel">
                    <h3>{dashboardAction.title}</h3>
                    <p>{dashboardAction.detail}</p>
                    <button
                      type="button"
                      className="secondary-action"
                      onClick={() => document.getElementById(dashboardAction.target)?.scrollIntoView({ behavior: "smooth", block: "start" })}
                    >
                      {dashboardAction.actionLabel}
                    </button>
                  </div>
                </section>
                <section className="panel-card">
                  <p className="eyebrow">Needs attention</p>
                  {attentionItems.length === 0 ? (
                    <div className="empty-state compact">No launch blockers currently identified.</div>
                  ) : (
                    <ul className="stack-list">
                      {attentionItems.map((item) => (
                        <li key={item.key}>
                          <strong>{item.title}</strong>
                          <span>{item.detail}</span>
                        </li>
                      ))}
                    </ul>
                  )}
                </section>
              </div>
            </>
          )}
        </header>

        <section id="opportunities" className="results-panel" aria-live="polite">
          <div className="section-head">
            <div>
              <p className="eyebrow">Opportunity</p>
              <h2>Opportunities</h2>
            </div>
            <p className="helper-copy">An opportunity is a business idea Atlas evaluates for demand, competition, and monetization potential.</p>
          </div>
          {opportunities.length === 0 && results.length === 0 && !isLoading ? (
            <div className="empty-state">
              <h3>No opportunities yet.</h3>
              <p>An opportunity is a business idea Atlas can evaluate for demand, competition, and monetization potential.</p>
              <button type="button" onClick={() => document.getElementById("dashboard")?.scrollIntoView({ behavior: "smooth", block: "start" })}>
                Create Opportunity
              </button>
            </div>
          ) : null}

          {opportunities.map((opportunity) => {
            const linkedPlan = combinedPlanList.find((plan) => plan.opportunity_id === opportunity.id);
            const linkedCampaigns = campaigns.filter((campaign) => campaign.opportunity_id === opportunity.id);
            return (
              <article className="result-row" key={opportunity.id}>
                <div className="rank-cell">{Math.round(opportunity.opportunity_score)}</div>
                <div className="topic-cell">
                  <WorkflowIndicator currentStage="Opportunity" />
                  <div className="topic-header">
                    <h2>{titleCase(opportunity.topic)}</h2>
                    <span className={`recommendation-badge recommendation-${opportunity.recommendation.toLowerCase()}`}>
                      {formatLabel(opportunity.recommendation)}
                    </span>
                  </div>
                  <div className="score-grid">
                    <Metric label="Opportunity Score" value={opportunity.opportunity_score} />
                    <Metric label="Demand" value={opportunity.demand_score} />
                    <Metric label="Competition" value={opportunity.competition_score} />
                    <Metric label="Buyer Intent" value={opportunity.buyer_intent_score} />
                    <Metric label="Monetization Potential" value={opportunity.affiliate_score} />
                    <Metric label="Pinterest" value={opportunity.pinterest_score} />
                    <Metric label="SEO" value={opportunity.seo_score} />
                  </div>
                  <div className="plan-summary">
                    <p>Target audience: {linkedPlan?.target_audience ?? "Create a business plan to define the audience."}</p>
                    <p>Monetization model: {linkedPlan ? formatLabel(linkedPlan.primary_monetization) : "Not selected yet"}</p>
                    <p>Linked business plan: {linkedPlan ? linkedPlan.value_proposition : "None yet"}</p>
                    <p>Linked campaigns: {linkedCampaigns.length ? linkedCampaigns.map((campaign) => campaign.name).join(", ") : "None yet"}</p>
                    <p>Recommended next action: {linkedPlan ? "View Business Plan" : "Create Business Plan"}</p>
                    <button
                      className="plan-button"
                      type="button"
                      disabled={planningTopic === opportunity.topic}
                      onClick={() =>
                        linkedPlan
                          ? document.getElementById("business-plans")?.scrollIntoView({ behavior: "smooth", block: "start" })
                          : handleCreateBusinessPlanForOpportunity(opportunity)
                      }
                    >
                      {linkedPlan ? "View Business Plan" : planningTopic === opportunity.topic ? "Creating..." : "Create Business Plan"}
                    </button>
                  </div>
                </div>
              </article>
            );
          })}

          {results.length > 0 ? (
            <div className="section-subhead">
              <p className="eyebrow">Idea comparison</p>
              <h3>Multiple idea evaluation</h3>
              <p className="helper-copy">These comparison results are not saved as opportunities until you create one.</p>
            </div>
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
                      <p>Monetization: {formatLabel(plansByTopic[result.topic].primary_monetization)}</p>
                      <p>Primary channel: {formatLabel(plansByTopic[result.topic].primary_acquisition_channel)}</p>
                      <p>
                        Revenue: ${plansByTopic[result.topic].revenue_low_monthly} - $
                        {plansByTopic[result.topic].revenue_high_monthly} / month
                      </p>
                      <p>Effort: {formatLabel(plansByTopic[result.topic].effort_level)}</p>
                      <p>Assets: {plansByTopic[result.topic].recommended_assets.map(formatLabel).join(", ")}</p>
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

        <section id="campaigns" className="workspace-card">
          <div className="section-head">
            <div>
              <p className="eyebrow">Campaign execution</p>
              <h2>Campaigns</h2>
            </div>
            <p className="helper-copy">Select one campaign to continue the workflow.</p>
          </div>
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
                    <span>{statusLabel(campaign.status)} - {campaign.progress.completion_percentage}% complete</span>
                  </button>
                ))
              )}
            </div>
          </article>
        </section>

        {selectedCampaign ? (
          <CampaignWorkspace
            campaign={selectedCampaign}
            opportunities={opportunities}
            businessPlans={combinedPlanList}
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

        <section id="production-queue" className="workspace-card">
          <div className="section-head">
            <div>
              <p className="eyebrow">Operations</p>
              <h2>Production Queue</h2>
            </div>
            <p className="helper-copy">Review work by priority and stage.</p>
          </div>
          <article className="campaign-hero">
            <div>
              <p className="eyebrow">Production queue</p>
              <h2>Asset Production Queue</h2>
              <p className="helper-copy">
                Review the highest-priority work first, grouped by what needs attention and what can move now.
              </p>
            </div>
            <button type="button" className="primary-action" disabled={queueLoading} onClick={() => loadAssetQueue().catch((caughtError) => setError(caughtError instanceof Error ? caughtError.message : "Queue load failed."))}>
              {queueLoading ? "Refreshing Queue..." : "Refresh Queue"}
            </button>
          </article>

          <div className="field-grid">
            <label className="field">
              <span>Campaign</span>
              <select value={queueFilters.campaign_id} onChange={(event) => setQueueFilters((current) => ({ ...current, campaign_id: event.target.value }))}>
                <option value="">All campaigns</option>
                {campaigns.map((campaign) => (
                  <option key={campaign.id} value={campaign.id}>{campaign.name}</option>
                ))}
              </select>
            </label>
            <label className="field">
              <span>Channel</span>
              <select value={queueFilters.channel} onChange={(event) => setQueueFilters((current) => ({ ...current, channel: event.target.value }))}>
                <option value="">All channels</option>
                {uniqueValues(allAssets.map((asset) => asset.channel)).map((channel) => <option key={channel} value={channel}>{formatLabel(channel)}</option>)}
              </select>
            </label>
            <label className="field">
              <span>Priority</span>
              <select value={queueFilters.priority} onChange={(event) => setQueueFilters((current) => ({ ...current, priority: event.target.value }))}>
                <option value="">All priorities</option>
                {["low", "medium", "high", "critical"].map((priority) => <option key={priority} value={priority}>{formatLabel(priority)}</option>)}
              </select>
            </label>
            <label className="field">
              <span>Status</span>
              <select value={queueFilters.status} onChange={(event) => setQueueFilters((current) => ({ ...current, status: event.target.value }))}>
                <option value="">All statuses</option>
                {Object.keys(assetStatusLabel).map((status) => <option key={status} value={status}>{assetStatusLabel[status]}</option>)}
              </select>
            </label>
            <label className="field">
              <span>Assigned user</span>
              <select value={queueFilters.assigned_to} onChange={(event) => setQueueFilters((current) => ({ ...current, assigned_to: event.target.value }))}>
                <option value="">Anyone</option>
                {uniqueValues(allAssets.map((asset) => asset.assigned_to).filter(Boolean) as string[]).map((user) => <option key={user} value={user}>{user}</option>)}
              </select>
            </label>
          </div>
          <button
            type="button"
            className="secondary-action filter-clear"
            onClick={() => setQueueFilters({ campaign_id: "", channel: "", priority: "", status: "", assigned_to: "" })}
          >
            Clear Filters
          </button>

          {queueLoading ? (
            <div className="loading-skeleton">Loading production queue...</div>
          ) : queueAssets.length === 0 ? (
            <div className="empty-state">
              <h3>No assets currently require production work.</h3>
              <p>Assets will appear here after they are added to the queue.</p>
            </div>
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
                              {assetStatusLabel[asset.status] ?? asset.status}
                            </p>
                          </div>
                          <span className="status-badge">{formatLabel(asset.priority)}</span>
                        </div>
                        <div className="detail-grid">
                          <Info label="Campaign" value={campaignName(campaigns, asset.campaign_id)} />
                          <Info label="Type" value={formatLabel(asset.asset_type)} />
                          <Info label="Channel" value={formatLabel(asset.channel)} />
                          <Info label="Due date" value={asset.due_date ? formatDate(asset.due_date) : "Not set"} />
                          <Info label="Assigned user" value={asset.assigned_to ?? "Unassigned"} />
                          <Info label="Next action" value={nextQueueActionLabel(asset)} />
                        </div>
                        <div className="item-actions">
                          <button
                            type="button"
                            className="secondary-action"
                            onClick={() => {
                              setSelectedCampaignId(asset.campaign_id);
                              setActiveTabByCampaignId((current) => ({ ...current, [asset.campaign_id]: "assets" }));
                              document.getElementById("campaigns")?.scrollIntoView({ behavior: "smooth", block: "start" });
                            }}
                          >
                            Open Campaign Assets
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
        <section id="business-plans" className="workspace-card">
          <div className="section-head">
            <div>
              <p className="eyebrow">Planning</p>
              <h2>Business Plans</h2>
            </div>
          </div>
          {businessPlans.length === 0 ? (
            <div className="empty-state">
              <h3>No business plans yet.</h3>
              <p>Create a business plan from an opportunity to define the audience, revenue model, channels, and content strategy.</p>
              <button type="button" onClick={() => document.getElementById("opportunities")?.scrollIntoView({ behavior: "smooth", block: "start" })}>
                View Opportunities
              </button>
            </div>
          ) : (
            <div className="card-list">
              {businessPlans.map(([topic, plan]) => {
                const linkedOpportunity = opportunities.find((opportunity) => opportunity.id === plan.opportunity_id);
                const linkedCampaigns = campaigns.filter((campaign) => campaign.business_plan_id === plan.id);
                return (
                  <article className="workflow-card" key={plan.id}>
                    <WorkflowIndicator currentStage="Business Plan" />
                    <div className="workflow-card-header">
                      <div>
                        <p className="eyebrow">{topic}</p>
                        <h3>{plan.value_proposition}</h3>
                        <p className="helper-copy">{plan.recommendation_summary}</p>
                      </div>
                      <span className="status-badge">{statusLabel(plan.status)}</span>
                    </div>
                    <div className="detail-grid">
                      <Info label="Linked opportunity" value={linkedOpportunity?.topic ?? `Opportunity #${plan.opportunity_id}`} />
                      <Info label="Audience" value={plan.target_audience} />
                      <Info label="Monetization model" value={formatLabel(plan.primary_monetization)} />
                      <Info label="Acquisition channels" value={[plan.primary_acquisition_channel, ...plan.secondary_acquisition_channels].map(formatLabel).join(", ")} />
                      <Info label="Content strategy" value={plan.recommended_assets.map(formatLabel).join(", ")} />
                      <Info label="Launch plan" value={`${plan.estimated_launch_days} days - ${formatLabel(plan.effort_level)} effort`} />
                      <Info label="Revenue objective" value={`$${plan.revenue_low_monthly} - $${plan.revenue_high_monthly} / month`} />
                      <Info label="Linked campaigns" value={linkedCampaigns.length ? linkedCampaigns.map((campaign) => campaign.name).join(", ") : "None yet"} />
                    </div>
                    <div className="item-actions">
                      <button
                        type="button"
                        className="secondary-action"
                        disabled={campaignTopic === topic || Boolean(campaignsByPlanId[plan.id])}
                        onClick={() =>
                          linkedCampaigns.length
                            ? document.getElementById("campaigns")?.scrollIntoView({ behavior: "smooth", block: "start" })
                            : handleCreateCampaign(topic, plan)
                        }
                      >
                        {linkedCampaigns.length ? "View Campaigns" : campaignTopic === topic ? "Creating Campaign..." : "Create Campaign"}
                      </button>
                    </div>
                  </article>
                );
              })}
            </div>
          )}
        </section>

        <section id="documentation" className="workspace-card">
          <div className="section-head">
            <div>
              <p className="eyebrow">Reference</p>
              <h2>Documentation</h2>
            </div>
          </div>
          <div className="card-list">
            <article className="workflow-card">
              <h3>Operating model</h3>
              <p className="helper-copy">Work flows from opportunity evaluation into business planning, campaign execution, task readiness, asset production, review, and publishing readiness.</p>
            </article>
            <article className="workflow-card">
              <h3>Atlas glossary</h3>
              <div className="glossary-grid">
                {glossaryTerms.map((term) => (
                  <div className="glossary-item" key={term.term}>
                    <strong>{term.term}</strong>
                    <span>{term.meaning}</span>
                    <em>{term.example}</em>
                  </div>
                ))}
              </div>
            </article>
          </div>
        </section>

        <section id="settings" className="workspace-card">
          <div className="section-head">
            <div>
              <p className="eyebrow">Administration</p>
              <h2>Settings</h2>
            </div>
          </div>
          <div className="empty-state">Settings are intentionally left as a placeholder for now.</div>
        </section>
        </section>
      </div>
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

function WorkflowIndicator({ currentStage }: { currentStage: string }) {
  const stages = ["Opportunity", "Business Plan", "Campaign", "Tasks and Assets", "Production Queue", "Ready to Publish"];
  const currentIndex = stages.findIndex((stage) => stage === currentStage);
  return (
    <nav className="workflow-overview" aria-label="Atlas workflow">
      {stages.map((stage, index) => {
        const state = currentIndex === -1 ? "available" : index < currentIndex ? "complete" : index === currentIndex ? "current" : "future";
        return (
          <div className={`workflow-step workflow-step-${state}`} key={stage} aria-current={state === "current" ? "step" : undefined}>
            <span>{index + 1}</span>
            <strong>{stage}</strong>
          </div>
        );
      })}
    </nav>
  );
}

function IdeaForm({
  niche,
  topicsInput,
  isLoading,
  onNicheChange,
  onTopicsChange,
  onCreateOpportunity,
  onEvaluateMultiple,
}: {
  niche: string;
  topicsInput: string;
  isLoading: boolean;
  onNicheChange: (value: string) => void;
  onTopicsChange: (value: string) => void;
  onCreateOpportunity: () => void;
  onEvaluateMultiple: (event: FormEvent<HTMLFormElement>) => void;
}) {
  return (
    <form className="control-panel" onSubmit={onEvaluateMultiple}>
      <label className="field">
        <span>Niche</span>
        <input
          type="text"
          value={niche}
          onChange={(event) => onNicheChange(event.target.value)}
          placeholder="coffee, home office, software..."
        />
      </label>

      <label className="field">
        <span>Business idea</span>
        <textarea
          value={topicsInput}
          onChange={(event) => onTopicsChange(event.target.value)}
          rows={8}
          placeholder="Start with one idea. Add more lines to compare multiple ideas."
        />
      </label>

      <div className="action-row">
        <button type="button" disabled={isLoading} onClick={onCreateOpportunity}>
          {isLoading ? "Creating Opportunity..." : "Create Opportunity"}
        </button>
        <button type="submit" className="secondary-action" disabled={isLoading}>
          {isLoading ? "Evaluating Ideas..." : "Evaluate Multiple Ideas"}
        </button>
        <p className="helper-copy">An opportunity is a business idea Atlas can evaluate for demand, competition, and monetization potential.</p>
      </div>
    </form>
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

function opportunityToResult(opportunity: Opportunity, rank: number): PortfolioResult {
  return {
    rank,
    topic: opportunity.topic,
    business_score: opportunity.opportunity_score,
    recommendation: opportunity.recommendation as Recommendation,
    confidence: Math.round((opportunity.demand_score + opportunity.buyer_intent_score + opportunity.affiliate_score) / 3),
    demand_score: opportunity.demand_score,
    competition_score: opportunity.competition_score,
    buyer_intent_score: opportunity.buyer_intent_score,
    affiliate_score: opportunity.affiliate_score,
    pinterest_score: opportunity.pinterest_score,
    seo_score: opportunity.seo_score,
  };
}

function formatLabel(value: string | null | undefined): string {
  if (!value) return "Not set";
  const labels: Record<string, string> = {
    display_ads: "Display Advertising",
    lead_generation: "Lead Generation",
    digital_product: "Digital Product",
    buying_guide: "Buying Guide",
    comparison_page: "Comparison Page",
    analytics_setup: "Analytics Setup",
    email_capture: "Email Capture",
    lead_magnet: "Lead Magnet",
    welcome_email: "Welcome Email",
    downloadable_resource: "Downloadable Resource",
    ready_to_publish: "Ready to Publish",
    in_production: "In Progress",
    website_seo: "Website SEO",
  };
  return labels[value] ?? titleCase(value.replace(/[_-]/g, " "));
}

function titleCase(value: string): string {
  return value
    .split(" ")
    .filter(Boolean)
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1).toLowerCase())
    .join(" ");
}

function topicForPlan(plan: BusinessPlan, opportunities: Opportunity[]): string {
  return opportunities.find((opportunity) => opportunity.id === plan.opportunity_id)?.topic ?? `Opportunity #${plan.opportunity_id}`;
}

function uniqueValues(values: string[]): string[] {
  return Array.from(new Set(values.filter(Boolean))).sort((a, b) => a.localeCompare(b));
}

function campaignName(campaigns: CampaignDetail[], campaignId: number): string {
  return campaigns.find((campaign) => campaign.id === campaignId)?.name ?? `Campaign #${campaignId}`;
}

function assetDescription(assetType: string): string {
  return {
    website: "Primary website used to publish campaign content and direct visitors toward monetized actions.",
    homepage: "Main landing page that introduces the business, audience, and primary recommendations.",
    buying_guide: "Long-form content helping users choose a product and click relevant affiliate recommendations.",
    comparison_page: "Content comparing multiple products, features, pricing, and use cases.",
    analytics_setup: "Tracking configuration used to measure traffic, conversions, and revenue-related events.",
    email_capture: "Form or interface used to collect visitor email addresses.",
    lead_magnet: "Downloadable resource offered in exchange for an email address.",
    welcome_email: "Initial email introducing the business and providing the promised resource.",
    downloadable_resource: "File delivered to a user after they subscribe or complete the intended action.",
  }[assetType] ?? "A campaign deliverable required to move the launch plan forward.";
}

function statusLabel(status: string): string {
  return {
    planning: "Planning",
    ready: "Ready",
    approved: "Approved",
    building: "Building",
    archived: "Archived",
    draft: "Draft",
    paused: "Paused",
    published: "Published",
    optimizing: "Optimizing",
    cancelled: "Cancelled",
    completed: "Completed",
  }[status] ?? formatLabel(status);
}

function tabLabel(tab: "overview" | "tasks" | "assets" | "activity"): string {
  return { overview: "Overview", tasks: "Tasks", assets: "Assets", activity: "Activity" }[tab];
}

function formatDate(value: string): string {
  return new Date(value).toLocaleDateString();
}

function dependencyTask(tasks: CampaignTask[], task: CampaignTask): CampaignTask | null {
  if (task.depends_on_task_id == null) return null;
  return tasks.find((candidate) => candidate.id === task.depends_on_task_id) ?? null;
}

function linkedTaskLabel(tasks: CampaignTask[], taskId: number | null): string {
  if (taskId == null) return "None";
  return tasks.find((task) => task.id === taskId)?.title ?? `Task #${taskId}`;
}

function taskActions(task: CampaignTask): Array<"start" | "block" | "unblock" | "complete" | "reopen"> {
  if (task.status === "ready") return ["start"];
  if (task.status === "in_progress") return ["complete", "block"];
  if (task.status === "blocked") return ["unblock"];
  if (task.status === "review") return ["complete"];
  if (task.status === "completed") return ["reopen"];
  if (task.status === "cancelled") return ["reopen"];
  return [];
}

function taskDisplayStatus(tasks: CampaignTask[], task: CampaignTask): string {
  if (task.status === "pending" && task.depends_on_task_id == null) return "Waiting";
  return taskStatusLabel[task.status] ?? formatLabel(task.status);
}

function pendingTaskMessage(tasks: CampaignTask[], task: CampaignTask): string {
  const dependency = dependencyTask(tasks, task);
  if (task.status !== "pending") return "No action is available for this task.";
  if (!dependency) return "This task is waiting for the campaign to become executable.";
  return `Waiting for ${dependency.title} to be completed.`;
}

function taskDescription(task: CampaignTask): string {
  return {
    strategy: "Confirm the campaign strategy before downstream execution work begins.",
    brand: "Confirm the campaign audience, value proposition, and market positioning.",
    website: "Define the website work required for the campaign launch.",
    content: "Prepare content briefs that explain what needs to be produced.",
    email: "Prepare the email capture and follow-up experience for the campaign.",
    analytics: "Set up measurement so campaign outcomes can be reviewed later.",
    launch: "Review the work and prepare the campaign for launch readiness.",
  }[task.category] ?? "Complete this step to move the campaign forward.";
}

function openTaskAction(
  campaignId: number,
  task: CampaignTask,
  handleTaskActionFn: TaskActionFn,
  setTaskActualHoursFn: React.Dispatch<React.SetStateAction<Record<number, string>>>,
  setTaskNotesFn: React.Dispatch<React.SetStateAction<Record<number, string>>>,
  action: "start" | "block" | "unblock" | "complete" | "reopen",
) {
  if (action === "start") {
    handleTaskActionFn(campaignId, task.id, "start");
    return;
  }
  if (action === "block") {
    handleTaskActionFn(campaignId, task.id, "block");
    return;
  }
  if (action === "unblock") {
    handleTaskActionFn(campaignId, task.id, "unblock");
    return;
  }
  if (action === "complete") {
    const hours = window.prompt("Actual hours", task.actual_hours?.toString() ?? "");
    if (hours !== null) setTaskActualHoursFn((current) => ({ ...current, [task.id]: hours }));
    const notes = window.prompt("Completion notes", task.completion_notes ?? "");
    if (notes !== null) setTaskNotesFn((current) => ({ ...current, [task.id]: notes }));
    handleTaskActionFn(campaignId, task.id, "complete");
    return;
  }
  if (action === "reopen") {
    handleTaskActionFn(campaignId, task.id, "reopen");
  }
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

function dashboardNextRecommendedAction({
  campaigns,
  businessPlans,
  opportunities,
  plansWithCampaigns,
  opportunitiesWithPlans,
}: {
  campaigns: CampaignDetail[];
  businessPlans: BusinessPlan[];
  opportunities: Opportunity[];
  plansWithCampaigns: Set<number>;
  opportunitiesWithPlans: Set<number>;
}): { title: string; detail: string; actionLabel: string; target: string } {
  const blockedCampaign = campaigns.find((campaign) => campaign.progress.blocked_tasks > 0 || campaign.blocked_assets > 0);
  if (blockedCampaign) {
    return {
      title: `Resolve blockers in ${blockedCampaign.name}`,
      detail: `${blockedCampaign.progress.blocked_tasks} tasks and ${blockedCampaign.blocked_assets} assets need attention.`,
      actionLabel: "View Blockers",
      target: "campaigns",
    };
  }

  const reviewAssetCampaign = campaigns.find((campaign) => campaign.assets.some((asset) => asset.status === "review"));
  const reviewAsset = reviewAssetCampaign?.assets.find((asset) => asset.status === "review");
  if (reviewAssetCampaign && reviewAsset) {
    return {
      title: `Review ${reviewAsset.title}`,
      detail: `Campaign: ${reviewAssetCampaign.name}. Status: ${assetStatusLabel[reviewAsset.status]}.`,
      actionLabel: "Review Asset",
      target: "production-queue",
    };
  }

  const readyTaskCampaign = campaigns.find((campaign) => campaign.tasks.some((task) => task.status === "ready"));
  const readyTask = readyTaskCampaign?.tasks.find((task) => task.status === "ready");
  if (readyTaskCampaign && readyTask) {
    return {
      title: `Start ${readyTask.title}`,
      detail: `Campaign: ${readyTaskCampaign.name}. Estimated effort: ${readyTask.estimated_hours} hours.`,
      actionLabel: "Start Task",
      target: "campaigns",
    };
  }

  const queuedAssetCampaign = campaigns.find((campaign) => campaign.assets.some((asset) => asset.status === "queued"));
  const queuedAsset = queuedAssetCampaign?.assets.find((asset) => asset.status === "queued");
  if (queuedAssetCampaign && queuedAsset) {
    return {
      title: `Start ${queuedAsset.title}`,
      detail: `Campaign: ${queuedAssetCampaign.name}. This asset is ready for production.`,
      actionLabel: "Start Production",
      target: "production-queue",
    };
  }

  const planningCampaign = campaigns.find((campaign) => campaign.status === "planning");
  if (planningCampaign) {
    return {
      title: `Approve ${planningCampaign.name}`,
      detail: "This campaign is planned but not executable yet.",
      actionLabel: "View Campaign",
      target: "campaigns",
    };
  }

  const planWithoutCampaign = businessPlans.find((plan) => !plansWithCampaigns.has(plan.id));
  if (planWithoutCampaign) {
    return {
      title: "Create a campaign",
      detail: "A business plan is ready to become an execution workspace.",
      actionLabel: "View Business Plans",
      target: "business-plans",
    };
  }

  const opportunityWithoutPlan = opportunities.find((opportunity) => !opportunitiesWithPlans.has(opportunity.id));
  if (opportunityWithoutPlan) {
    return {
      title: `Create a business plan for ${opportunityWithoutPlan.topic}`,
      detail: "This opportunity has been evaluated but does not have a launch strategy yet.",
      actionLabel: "View Opportunities",
      target: "opportunities",
    };
  }

  return {
    title: "Create your first opportunity",
    detail: "Start with one business idea. Atlas will evaluate it and guide the next step.",
    actionLabel: "Create Opportunity",
    target: "dashboard",
  };
}

const assetStageOrder: Array<AssetStageKey> = [
  "planned",
  "ready_to_start",
  "in_progress",
  "waiting_for_review",
  "approved",
  "ready_to_publish",
  "needs_revision",
  "blocked",
  "cancelled",
];

const assetStageLabel: Record<AssetStageKey, string> = {
  planned: "Planned",
  ready_to_start: "Ready to start",
  in_progress: "In progress",
  waiting_for_review: "Waiting for review",
  approved: "Approved",
  ready_to_publish: "Ready to publish",
  needs_revision: "Needs revision",
  blocked: "Blocked",
  cancelled: "Cancelled",
};

const queueGroupOrder: Array<QueueGroupKey> = [
  "needs_attention",
  "ready_to_start",
  "in_progress",
  "waiting_for_review",
  "ready_to_publish",
];

const queueGroupLabel: Record<QueueGroupKey, string> = {
  needs_attention: "Needs attention",
  ready_to_start: "Ready to start",
  in_progress: "In progress",
  waiting_for_review: "Waiting for review",
  ready_to_publish: "Ready to publish",
};

function groupedAssets(assets: CampaignAsset[]): Record<AssetStageKey, CampaignAsset[]> {
  const groups: Record<AssetStageKey, CampaignAsset[]> = {
    planned: [],
    ready_to_start: [],
    in_progress: [],
    waiting_for_review: [],
    approved: [],
    ready_to_publish: [],
    needs_revision: [],
    blocked: [],
    cancelled: [],
  };
  for (const asset of assets) groups[assetStageForStatus(asset.status)].push(asset);
  return groups;
}

function groupQueueAssets(assets: CampaignAsset[]): Record<QueueGroupKey, CampaignAsset[]> {
  const groups: Record<QueueGroupKey, CampaignAsset[]> = {
    needs_attention: [],
    ready_to_start: [],
    in_progress: [],
    waiting_for_review: [],
    ready_to_publish: [],
  };
  for (const asset of assets) groups[queueGroupForStatus(asset.status)].push(asset);
  return groups;
}

function assetStageForStatus(status: string): AssetStageKey {
  if (status === "planned") return "planned";
  if (status === "queued") return "ready_to_start";
  if (status === "in_production") return "in_progress";
  if (status === "review") return "waiting_for_review";
  if (status === "approved") return "approved";
  if (status === "blocked") return "blocked";
  if (status === "rejected") return "needs_revision";
  if (status === "cancelled") return "cancelled";
  return "ready_to_publish";
}

function queueGroupForStatus(status: string): QueueGroupKey {
  if (status === "planned" || status === "blocked" || status === "rejected") return "needs_attention";
  if (status === "queued") return "ready_to_start";
  if (status === "in_production") return "in_progress";
  if (status === "review") return "waiting_for_review";
  return "ready_to_publish";
}

function emptyAssetGroupMessage(group: AssetStageKey): string {
  return {
    planned: "No planned assets in this stage.",
    ready_to_start: "No assets are ready to start.",
    in_progress: "No assets are in progress.",
    waiting_for_review: "Nothing is waiting for review.",
    approved: "No assets are approved yet.",
    ready_to_publish: "No assets are ready to publish.",
    needs_revision: "No assets need revision.",
    blocked: "No assets are blocked.",
    cancelled: "No cancelled assets.",
  }[group];
}

function emptyQueueMessage(group: QueueGroupKey): string {
  return {
    needs_attention: "No assets need attention right now.",
    ready_to_start: "No assets are ready to start.",
    in_progress: "No assets are in progress.",
    waiting_for_review: "Nothing is waiting for review.",
    ready_to_publish: "No assets are ready to publish.",
  }[group];
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

function assetActions(asset: CampaignAsset): Array<
  | "queue"
  | "start"
  | "block"
  | "submit-for-review"
  | "approve"
  | "reject"
  | "resubmit"
  | "mark-ready-to-publish"
  | "unblock"
  | "reopen"
> {
  if (asset.status === "planned") return ["queue"];
  if (asset.status === "queued") return ["start"];
  if (asset.status === "in_production") return ["submit-for-review", "block"];
  if (asset.status === "review") return ["approve", "reject"];
  if (asset.status === "rejected") return ["resubmit"];
  if (asset.status === "approved") return ["mark-ready-to-publish"];
  if (asset.status === "blocked") return ["unblock"];
  if (asset.status === "cancelled") return ["reopen"];
  return [];
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
  opportunities,
  businessPlans,
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
  opportunities: Opportunity[];
  businessPlans: BusinessPlan[];
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
      | "block"
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
  const linkedPlan = businessPlans.find((plan) => plan.id === campaign.business_plan_id);
  const linkedOpportunity = opportunities.find((opportunity) => opportunity.id === campaign.opportunity_id);

  return (
    <section className="workspace-card">
      <article className="campaign-hero">
        <div>
          <p className="eyebrow">Campaign workspace</p>
          <h2>{campaign.name}</h2>
          <p className="helper-copy">{campaign.goal}</p>
          <WorkflowIndicator currentStage="Campaign" />
        </div>
        <div className="campaign-kpis">
          <Kpi label="Status" value={statusLabel(campaign.status)} />
          <Kpi label="Linked opportunity" value={linkedOpportunity?.topic ?? `Opportunity #${campaign.opportunity_id}`} />
          <Kpi label="Linked business plan" value={linkedPlan?.value_proposition ?? `Business Plan #${campaign.business_plan_id}`} />
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
            <p className="eyebrow">Recent updates</p>
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
                .map((task) => {
                  const dependency = dependencyTask(campaign.tasks, task);
                  const actions = taskActions(task);
                  return (
                  <article className="workflow-card" key={task.id}>
                    <div className="workflow-card-header">
                      <div>
                        <p className="eyebrow">Step {task.order_index}</p>
                        <h3>{task.title}</h3>
                        <p className="helper-copy">{task.description ?? taskDescription(task)}</p>
                      </div>
                      <span className="status-badge">{taskDisplayStatus(campaign.tasks, task)}</span>
                    </div>
                    <div className="detail-grid">
                      {dependency ? <Info label={task.status === "pending" ? "Waiting for" : "Depends on"} value={dependency.title} /> : null}
                      <Info label="Estimated effort" value={`${task.estimated_hours} hours`} />
                      {task.actual_hours == null ? null : <Info label="Actual effort" value={`${task.actual_hours} hours`} />}
                      {task.assigned_to ? <Info label="Assigned user" value={task.assigned_to} /> : null}
                      {task.due_date ? <Info label="Due date" value={formatDate(task.due_date)} /> : null}
                      {task.blocked_reason ? <Info label="Blocked reason" value={task.blocked_reason} /> : null}
                      {task.completion_notes ? <Info label="Completion notes" value={task.completion_notes} /> : null}
                    </div>
                    <div className="item-actions">
                      {actions.length === 0 ? <p className="helper-copy">{pendingTaskMessage(campaign.tasks, task)}</p> : null}
                      {actions.map((action, index) => (
                        <button
                          type="button"
                          key={action}
                          className={index === 0 ? "primary-action" : "secondary-action"}
                          onClick={() => openTaskAction(campaign.id, task, handleTaskAction, setTaskActualHours, setTaskNotes, action)}
                        >
                          {taskActionLabel[action]}
                        </button>
                      ))}
                    </div>
                  </article>
                  );
                })}
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
              {assetStageOrder.map((group) => (
                <div key={group} className="group-column">
                  <h3>{assetStageLabel[group]}</h3>
                  {groupedAssets(campaign.assets)[group].length === 0 ? (
                    <div className="empty-state compact">{emptyAssetGroupMessage(group)}</div>
                  ) : (
                    groupedAssets(campaign.assets)[group].map((asset) => (
                      <article className="workflow-card" key={asset.id}>
                        <div className="workflow-card-header">
                          <div>
                            <h4>{asset.title}</h4>
                            <p className="helper-copy">
                              {assetDescription(asset.asset_type)}
                            </p>
                          </div>
                          <span className="status-badge">{formatLabel(asset.priority)}</span>
                        </div>
                        <div className="detail-grid">
                          {asset.description ? <Info label="Purpose" value={asset.description} /> : <Info label="Purpose" value={assetDescription(asset.asset_type)} />}
                          <Info label="Type" value={formatLabel(asset.asset_type)} />
                          <Info label="Channel" value={formatLabel(asset.channel)} />
                          <Info label="Status" value={assetStatusLabel[asset.status] ?? asset.status} />
                          {asset.campaign_task_id ? <Info label="Linked task" value={linkedTaskLabel(campaign.tasks, asset.campaign_task_id)} /> : null}
                          {asset.estimated_hours == null ? null : <Info label="Estimated effort" value={`${asset.estimated_hours} hours`} />}
                          {asset.actual_hours == null ? null : <Info label="Actual effort" value={`${asset.actual_hours} hours`} />}
                          {asset.due_date ? <Info label="Due date" value={formatDate(asset.due_date)} /> : null}
                          {asset.assigned_to ? <Info label="Assigned user" value={asset.assigned_to} /> : null}
                        </div>
                        <div className="item-actions">
                          {assetActions(asset).map((action, index) => (
                            <button
                              type="button"
                              key={action}
                              className={index === 0 ? "primary-action" : "secondary-action"}
                              disabled={assetBusy === `${campaign.id}:${asset.id}:${action}`}
                              onClick={() => handleAssetAction(campaign.id, asset.id, action)}
                            >
                              {assetActionLabel[action]}
                            </button>
                          ))}
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
          <p className="helper-copy">Atlas does not store a full activity log yet, so this tab summarizes current campaign updates from real campaign state.</p>
          <ul className="stack-list">
            <li>
              <strong>Task progress</strong>
              <span>
                {campaign.progress.completed_tasks} of {campaign.progress.total_tasks} tasks complete with {campaign.progress.blocked_tasks} blocked.
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
