# Publication and support

1. Validate the catalog and commit source/image pins to the source repository. Do not publish `.local`, receipts, credentials, or private revenue research.
2. Create the five unpublished drafts using `scripts/create-drafts.py`. Inspect each draft's services, Dockerfile paths, ports, variables, and volumes against its `template.json`.
3. Deploy each draft into a new test project. Generated variables must resolve to distinct secrets; dependencies must have no public TCP proxies or service domains. Verify public HTTPS and internal service DNS.
4. Complete the functional check in each product README. Test a restart, a volume-preserving redeploy, a backup, and restoration into a separate test instance. Record measured Railway usage; local idle memory is not a monthly cost estimate.
5. Publish only a template whose fresh deployment passes these checks. Use the per-template README as the marketplace overview. Choose the owning workspace deliberately so attribution is correct.

```sh
railway templates publish TEMPLATE_ID --category Other \
  --description "Deploy and host the application with persistent storage" \
  --readme-file templates/APP/README.md
```

Replace the command's arguments with the receipt's real template ID, appropriate category, and product-specific description. There are no fabricated deploy badges in this repository.

Maintain a support queue and answer deployment questions promptly. Railway's maximum kickback depends on the applicable program and support eligibility, not merely putting an image in the catalog. Do not advertise fixed hosting prices or forecast earnings from deployment counts. A fix to another creator's repository does not transfer that creator's attribution.

Primary references: [template creation](https://docs.railway.com/templates/create), [template CLI](https://docs.railway.com/cli/templates), [template metrics](https://docs.railway.com/templates/metrics).
