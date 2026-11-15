# Signal Desk: migrate to a genuinely private website

**Status: migration prepared; NOT activated.** Do not make the GitHub repository private or publish the data until the full authentication path is configured and validated.

## Current architecture and why it must change

The legacy GitHub Pages workflow generates data in CI and deploys it, but does NOT commit generated JSON files to the repo. Cloudflare's Git integration only builds files available in GitHub, so a scheduled workflow must commit fresh JSON to the **private** repository. A separate new scheduled workflow template is supplied here.

The original site `https://bnabdela.github.io/signal-desk/` is public until unpublished or removed. Merely changing GitHub repository visibility does not secure every published copy on every plan.

## Recommended cutover steps

1. Create a Cloudflare account at https://dash.cloudflare.com/ (or sign in). In **Workers & Pages** create a new **Pages** project and connect the GitHub repository `bnabdela/signal-desk`. Authorize the Cloudflare app for that repo only.
2. Set the Pages build configuration:
   - Production branch: `main`.
   - Framework preset: `None`.
   - Build command: `mkdir -p dist/data && cp index.html research.html companies.json dist/ && cp data/dashboard.json data/research.json dist/data/`.
   - Build output directory: `dist`.
   - Do not paste a private API key into the build command or commit secrets.
3. **Immediately protect the deployment**. Pages' Settings → General → Enable access policy protects *preview deployments only*. Follow Cloudflare's current [known issues instructions](https://developers.cloudflare.com/pages/platform/known-issues/#enable-access-on-your-pagesdev-domain) to also secure the production `PROJECT.pages.dev` hostname: in the generated Access application, remove the wildcard from the Subdomain field, save, and re-enable preview access separately. If you use a custom domain, create/extend a Cloudflare Access self-hosted app for that hostname as well. Verify the exact hostnames and all preview URLs; do not leave a bypass route.
4. Configure Access login using One-time PIN or a trusted identity provider and an **Allow** policy scoped only to your email address or identity. Default-deny all other users. Enable MFA at your identity provider.
5. Test in a private/incognito browser session **not logged in**: `/`, `/research.html`, `/data/dashboard.json`, and `/data/research.json` must ALL require authentication (not reveal actual page/JSON). Test preview deployment URLs as well. Then verify that authorized login displays the current dashboard. No anonymous access to assets/JSON may remain.
6. Set GitHub repository visibility to **Private** via **Settings → Danger Zone → Change repository visibility**. On GitHub Free, the existing GitHub Pages publication will normally be unpublished. Independently verify `https://bnabdela.github.io/signal-desk/` is no longer accessible without authorization; disable the legacy Pages workflow and GitHub Pages publishing. Old publicly forked/archived copies cannot be revoked retroactively.
7. Activate private refresh automation: move the file `migration/private-refresh.yml` to `.github/workflows/private-refresh.yml` (GitHub web UI allows creating a new workflow file by copying the template, then deleting the template if desired). Add repository **Actions variable** `SIGNAL_DESK_PRIVATE_READY` with value `true` ONLY after Step 5 + Step 6 are complete.
8. In GitHub Actions, run **Private Signal Desk data refresh (activate after migration)** once. Confirm JSON files in `data/` were updated in the **private** repo, Cloudflare Git integration rebuilt the Pages site, and timestamp/quotes/financial/earnings/news data display. The old workflow is no longer needed and should be disabled or removed.
9. Confirm the scheduled morning and after-close refreshes by checking both the Actions run and the website timestamp the following day. Scheduled runs may be delayed, skipped, or yield stale quotes if upstream providers fail.

## Security recommendations

- Publish only behind Access: secure **all** page, news, financial JSON and deployment hosts, not just an HTML login page.
- Remove/archive the old GitHub Pages workflow once cloud hosting is verified. If it remains enabled, it could keep creating publicly accessible snapshots on paid GitHub plans.
- Keep API keys in encrypted GitHub Actions secrets. GitHub Pages/Cloudflare Pages static assets and generated JSON never contain credentials.
- GitHub repository history was previously public; making it private does not erase copies obtained while public.
- If private investment positions or proprietary analyses are added, do not expose them through publicly hosted static JSON or browser code. Consider a server-side authenticated database architecture.
- A GitHub Actions success check alone does not prove the data is complete. Check per-ticker coverage and timestamps.
- Cloudflare features, pricing, free-tier limits and UI labels may evolve. Use official docs when choosing access policies.
