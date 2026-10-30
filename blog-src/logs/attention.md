# Needs attention

The routines add a dated line here only when they need the owner.

2026-10-30  Search Console key rejected (invalid_grant: Invalid JWT Signature for reprot-search@rep-rot.iam.gserviceaccount.com, key id b6801bb1…): weekly review can't run. The key was likely deleted, disabled or rotated; create a new JSON key in Google Cloud and update GSC_SERVICE_ACCOUNT_B64 in the environment.
2026-10-30  Resolved: the Search Console key works again on a later run today (authenticated; property just has no data yet). No action needed on the key.
2026-10-30  Daily post ran under a network policy that blocks most hosts: Cloudflare Workers AI (gen_image.py: 403 from proxy, twice), WebFetch of competitor pages and primary sources (pubmed, support.apple.com, etc.). Post published with the existing header plus library photo, stat card and app screenshot; facts verified via search results only. To restore AI inline images and full research, allow api.cloudflare.com (and ideally general web access) in the cloud environment's Network access settings.
