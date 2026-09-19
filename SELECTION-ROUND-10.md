# Fifteen additional marketplace templates

Selection date: September 19, 2026. Starting workspace inventory: 85 published
templates and no unpublished drafts. Publication is complete: the verified final inventory is 100 published with no drafts. See [release details](RELEASES-ROUND-10.md).

Each candidate qualifies through product and alias searches that found no
matching public Railway listing. This is bounded marketplace evidence; private,
unindexed and differently named listings may exist. The 46 product/alias checks have complete pagination. Search receipts, exclusions
and upstream references are recorded in `eligibility.round10.json` and
`sources.round10.lock.json`. Existing listings were not assumed broken merely
because they were old or had few deployments.

| Template | Purpose |
| --- | --- |
| Raneto | A Markdown knowledge base |
| Movary | A personal movie diary |
| Pinry | Private image boards |
| Mikochi | File browsing and streaming |
| Airstation | A personal music station |
| Swagger Editor | Editing OpenAPI specifications |
| Redoc | Rendering API reference documentation |
| PlantUML | Rendering diagrams from text |
| Mountebank | Private API test doubles |
| Stoplight Prism | OpenAPI mock responses |
| Speedtest Tracker | Tracking network tests from the Railway region |
| Backrest | Managing restic backup repositories |
| LibreBooking | Scheduling shared resources |
| DomainMOD | Tracking domain portfolios |
| farmOS | Managing farm records |

Swagger Editor is distinct from Swagger UI. Broad Redoc and Prism searches
contain incidental or unrelated results; the evidence identifies the exclusions.
Structurizr was excluded after deployment-mode restrictions were found.
Request Baskets was excluded during upstream review. Products already represented
in the marketplace or the owner's catalog were not used to fill the count.

The templates use generated owner access at their public endpoint. Application
services and databases use private networking. Persistent applications have
explicit volume paths and recovery instructions. Speedtest Tracker tests the
Railway region's connectivity, not the operator's home network. Backrest can
access its own configured sources and repositories; it does not automatically
mount other Railway services' volumes.

Validation covers source/configuration review, digest references, service
references, public exposure, persistent paths, startup-script checks and
publication metadata. A local Docker daemon was unavailable. Container builds,
fresh Railway application deployments, functional workflows, restart behavior,
backup restoration and measured cost remain unverified. The individual overviews
disclose these limits and provide acceptance steps. Publication creates template
listings; it does not create application deployments.

Nine actual Nginx authentication tests subsequently passed for the round-ten owner gateway, including cookie issuance, native Bearer forwarding, credential rejection and healthcheck isolation. Application runtime verification remains outstanding.
