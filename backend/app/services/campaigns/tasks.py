from app.models.campaign_task import CampaignTask


class CampaignTaskGenerator:
    def generate(self, campaign, business_plan) -> list[CampaignTask]:
        tasks: list[dict] = [
            {"title": "Review and approve campaign objective", "category": "strategy", "hours": 2},
            {"title": "Validate brand positioning", "category": "brand", "hours": 3},
            {"title": "Validate monetization strategy", "category": "strategy", "hours": 3},
            {"title": "Validate acquisition-channel strategy", "category": "strategy", "hours": 3},
        ]
        if business_plan.primary_acquisition_channel == "website_seo" or "website" in business_plan.recommended_assets:
            tasks.extend(
                [
                    {"title": "Define website information architecture", "category": "website", "hours": 4},
                    {"title": "Create homepage brief", "category": "website", "hours": 3},
                    {"title": "Create buying-guide brief", "category": "content", "hours": 4},
                    {"title": "Create comparison-page briefs", "category": "content", "hours": 4},
                    {"title": "Configure email capture", "category": "email", "hours": 2},
                ]
            )
        if business_plan.primary_acquisition_channel == "pinterest" or "pinterest_pins" in business_plan.recommended_assets:
            tasks.extend(
                [
                    {"title": "Define Pinterest board strategy", "category": "pinterest", "hours": 2},
                    {"title": "Create Pinterest pin briefs", "category": "pinterest", "hours": 3},
                    {"title": "Review Pinterest compliance requirements", "category": "pinterest", "hours": 2},
                ]
            )
        if business_plan.primary_acquisition_channel == "youtube" or "youtube_shorts" in business_plan.recommended_assets:
            tasks.extend(
                [
                    {"title": "Define YouTube Shorts content angles", "category": "youtube", "hours": 3},
                    {"title": "Create Shorts script briefs", "category": "youtube", "hours": 4},
                ]
            )
        if business_plan.primary_acquisition_channel == "email" or "email_capture" in business_plan.recommended_assets:
            tasks.extend(
                [
                    {"title": "Define lead magnet", "category": "email", "hours": 3},
                    {"title": "Create welcome-sequence brief", "category": "email", "hours": 3},
                ]
            )
        tasks.extend(
            [
                {"title": "Configure analytics and revenue tracking", "category": "analytics", "hours": 3},
                {"title": "Final campaign review", "category": "launch", "hours": 2},
                {"title": "Launch campaign", "category": "launch", "hours": 2},
            ]
        )
        generated: list[CampaignTask] = []
        for index, item in enumerate(tasks, start=1):
            depends = generated[-1].id if generated else None
            generated.append(
                CampaignTask(
                    campaign_id=campaign.id,
                    title=item["title"],
                    category=item["category"],
                    status="pending",
                    priority="medium",
                    estimated_hours=item["hours"],
                    depends_on_task_id=depends,
                    order_index=index,
                )
            )
        return generated
