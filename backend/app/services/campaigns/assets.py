from app.models.campaign_asset import CampaignAsset


class CampaignAssetPlanner:
    def plan(self, campaign, business_plan) -> list[CampaignAsset]:
        assets: list[tuple[str, str, str, int]] = [
            ("website", "Website", "website", 1),
            ("homepage", "Homepage", "website", 1),
            ("buying_guide", "Buying Guides", "website", 2),
            ("comparison_page", "Comparison Pages", "website", 2),
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
                channel=channel,
                status="planned",
                priority="medium",
                planned_quantity=quantity,
                generated_quantity=0,
                published_quantity=0,
            )
            for index, (asset_type, title, channel, quantity) in enumerate(assets, start=1)
        ]
