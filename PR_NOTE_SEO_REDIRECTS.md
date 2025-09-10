Title: SEO: Normalize redirects, canonicals, and JSON‑LD IDs

Summary
- Add single-hop HTTP → HTTPS redirects for apex and www.
- Keep www → apex canonicalization.
- Normalize blog URLs: enforce trailing slash for /blog and /blog/:slug.
- Collapse category/tag query variants to canonical /blog/.
- Align JSON‑LD mainEntityOfPage @id with canonical URLs (trailing slash).

Files changed
- netlify.toml
- blog/winter-organization-tips/index.html
- blog/upcycling-guide/index.html
- blog/end-of-summer-deep-clean/index.html
- blog/10-items-you-didnt-know-could-be-recycled/index.html

Notes
- Removed redundant, hard-coded category and slug redirects; covered by generic rules.
- robots.txt and sitemaps already reference HTTPS apex canonicals with trailing slashes.

Verification checklist
- curl -I http://grimetodime.com/ returns 301 → https://grimetodime.com/
- curl -I http://www.grimetodime.com/ returns 301 → https://grimetodime.com/
- curl -I https://www.grimetodime.com/ returns 301 → https://grimetodime.com/
- curl -I 'https://grimetodime.com/blog?category=diy' returns 301 → https://grimetodime.com/blog/
- curl -I 'https://grimetodime.com/blog?tag=spring-cleaning' returns 301 → https://grimetodime.com/blog/
- curl -I https://grimetodime.com/blog/upcycling-guide returns 301 → https://grimetodime.com/blog/upcycling-guide/

Post-deploy
- Purge Netlify cache.
- In GSC, resubmit sitemaps and inspect a few problematic URLs to confirm canonicalization.
