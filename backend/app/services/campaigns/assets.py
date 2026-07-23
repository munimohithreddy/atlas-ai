from app.models.campaign_asset import CampaignAsset


class CampaignAssetPlanner:
    def plan(self, campaign, business_plan) -> list[CampaignAsset]:
        descriptions = {
            "website": "Primary website used to publish campaign content and direct visitors toward monetized actions.",
            "homepage": "Main landing page that introduces the business, audience, and primary recommendations.",
            "buying_guide": "Long-form content helping users choose a product and click relevant affiliate recommendations.",
            "comparison_page": "Content comparing multiple products, features, pricing, and use cases.",
            "analytics_setup": "Tracking configuration used to measure traffic, conversions, and revenue-related events.",
            "pinterest_pin": "Visual social asset used to attract interested visitors from Pinterest.",
            "youtube_short": "Short video script or creative brief used to reach viewers through YouTube Shorts.",
            "email_capture": "Form or interface used to collect visitor email addresses.",
            "lead_magnet": "Downloadable resource offered in exchange for an email address.",
            "welcome_email": "Initial email introducing the business and providing the promised resource.",
            "downloadable_resource": "File delivered to a user after they subscribe or complete the intended action.",
        }
        estimated_hours = {
            "website": 4,
            "homepage": 3,
            "buying_guide": 4,
            "comparison_page": 4,
            "analytics_setup": 2,
            "pinterest_pin": 1,
            "youtube_short": 2,
            "email_capture": 2,
            "lead_magnet": 3,
            "welcome_email": 1,
            "downloadable_resource": 3,
        }
        assets: list[tuple[str, str, str, int]] = [
            ("website", "Website", "website", 1),
            ("homepage", "Homepage", "website", 1),
            ("buying_guide", "Buying Guide", "website", 2),
            ("comparison_page", "Comparison Page", "website", 2),
            ("analytics_setup", "Analytics Setup", "internal", 1),
        ]
        if "pinterest_pins" in business_plan.recommended_assets:
            assets.append(("pinterest_pin", "Pinterest Pins", "pinterest", 6))
        if "youtube_shorts" in business_plan.recommended_assets:
            assets.append(("youtube_short", "YouTube Shorts", "youtube", 4))
        if "email_capture" in business_plan.recommended_assets:
            assets.extend(
                [
                    ("email_capture", "Email Capture", "email", 1),
                    ("lead_magnet", "Lead Magnet", "email", 1),
                    ("welcome_email", "Welcome Email", "email", 3),
                ]
            )
        if "downloadable_resource" in business_plan.recommended_assets:
            assets.append(("downloadable_resource", "Downloadable Resource", "internal", 1))
        return [
            CampaignAsset(
                campaign_id=campaign.id,
                order_index=index,
                asset_type=asset_type,
                title=title,
                description=descriptions.get(asset_type),
                channel=channel,
                status="planned",
                priority="medium",
                estimated_hours=estimated_hours.get(asset_type),
                planned_quantity=quantity,
                generated_quantity=0,
                published_quantity=0,
            )
            for index, (asset_type, title, channel, quantity) in enumerate(assets, start=1)
        ]
