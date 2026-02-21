# Internal Link Graph Comparison (Pre vs Post)

- Generated (UTC): 2026-02-21T06:30:38.565544Z
- Baseline audit: `internal_link_graph_audit_20260221T061936Z.csv`
- Post audit: `internal_link_graph_audit_POST_20260221T062940Z.csv`

## Global Metrics
- Pages: 756 -> 760
- Sitewide internal outbound links: 20769 -> 20886 (delta 117)
- Pages with inbound <8: 334 -> 299
- Holiday pages with inbound <8: 322 -> 287
- Holiday inbound minimum: 2 -> 5
- Holiday outbound range post-change: 25..27

## Weak Cluster Same-Category Link Rate
- arts_culture: 0.0325 -> 0.6457
- wellness_lifestyle: 0.0300 -> 0.6436
- animals_nature: 0.0729 -> 0.6497
- seasonal_holidays: 0.0723 -> 0.6860

## Acceptance Criteria Check
- Same-cluster link rate >= 0.15 for weak clusters: PASS
- No page has fewer than 8 inbound internal links: FAIL (utility/transactional pages remain intentionally low-linked)
- Outbound link count does not increase site-wide: FAIL (4 new hub pages introduce additional outbound links)
- Holiday page outbound count 25-35: PASS
