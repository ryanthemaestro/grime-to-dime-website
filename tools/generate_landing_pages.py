import argparse
import html
import json
import os
import re
import textwrap
from pathlib import Path
from typing import Dict, List
from update_sitemap import integrate_with_generator

import requests

# ---------------------------------------------------------------------------
# LLM helpers
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = (
    "You are a senior conversion copywriter and SEO strategist for a junk removal company. "
    "Given structured keyword group data, craft landing page copy that is conversion focused, "
    "locally relevant to Howard County, Maryland, and optimized for paid search and SEO. "
    "Return well-structured JSON that a renderer can drop into an HTML template."
)

CONTENT_PROMPT_TEMPLATE = textwrap.dedent(
    """
    We are launching programmatic landing pages for Grime To Dime, a junk removal company serving Howard County, Maryland.

    Please write conversion-focused copy for a landing page targeting the following service theme:

    Group name: {group_name}
    Description: {description}
    Primary keyword: {primary_keyword}
    Supporting keywords (sample):
    {keywords_bullets}

    Requirements:
    - Tone: confident, friendly, trustworthy local service pros.
    - Audience: homeowners, renters, and property managers searching for this specific service.
    - Highlight same-day or next-day availability when appropriate, upfront pricing, and responsible disposal.
    - Emphasize local expertise in Howard County and surrounding cities (Ellicott City, Columbia, Elkridge, Laurel, Clarksville, Savage, Catonsville).
    - Include strong calls to action that encourage calling or requesting a quote.
    - Button labels should be action-focused (e.g., "Call Now for Fast Pickup", "Get My Quote Now", "Schedule Today") - never include phone numbers or placeholders like XXX in button text.
    - Keep language unique to this service; do not copy wording verbatim between sections.
    - Avoid making guarantees you cannot back up (no "free" unless in the keywords context).

    Return valid JSON with this structure:
    {{
      "page_title": "",  # <= 60 characters, format "Service | City | Brand"
      "meta_description": "",  # 140-165 characters, compelling summary
      "hero": {{
        "heading": "",
        "subheading": "",
        "bullets": ["", "", ""]
      }},
      "quote_form": {{
        "heading": "",
        "details_label": "",
        "details_placeholder": "",
        "submit_label": "",
        "note": "",
        "form_subject": ""  # short subject for the hidden email subject field
      }},
      "what_we_take": [
        {{"title": "", "description": ""}},
        {{"title": "", "description": ""}},
        {{"title": "", "description": ""}}
      ],
      "how_it_works": [
        {{"title": "", "description": ""}},
        {{"title": "", "description": ""}},
        {{"title": "", "description": ""}}
      ],
      "pricing": [
        {{"title": "", "description": ""}},
        {{"title": "", "description": ""}}
      ],
      "faq": [
        {{"question": "", "answer": ""}},
        {{"question": "", "answer": ""}},
        {{"question": "", "answer": ""}},
        {{"question": "", "answer": ""}}
      ],
      "closing_cta": {{
        "button_label": "",
        "closing_copy": ""
      }},
      "service_type": ""  # short phrase for JSON-LD serviceType
    }}

    The text should read naturally when rendered into sections. Use American English spelling.
    """
)


class GrokError(Exception):
    """Custom exception for Grok related errors."""


def call_grok(messages: List[Dict[str, str]], model: str, timeout: int = 60) -> Dict:
    api_key = os.getenv("XAI_API_KEY")
    if not api_key:
        raise GrokError("Environment variable XAI_API_KEY is not set.")

    url = "https://api.x.ai/v1/chat/completions"
    payload = {
        "model": model,
        "temperature": 0.2,
        "stream": False,
        "messages": messages,
        "response_format": {"type": "json_object"},
    }

    try:
        response = requests.post(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
            data=json.dumps(payload),
            timeout=timeout,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise GrokError(f"Failed to contact Grok API: {exc}") from exc

    try:
        data = response.json()
        content = data["choices"][0]["message"]["content"].strip()
        return json.loads(content)
    except (KeyError, json.JSONDecodeError) as exc:
        raise GrokError(f"Unexpected Grok response format: {exc}\nRaw: {response.text[:500]}") from exc


# ---------------------------------------------------------------------------
# Rendering helpers
# ---------------------------------------------------------------------------

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang=\"en\">
<head>
    <script async src=\"https://www.googletagmanager.com/gtag/js?id=G-KGQDKQFZNF\"></script>
    <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-KGQDKQFZNF');gtag('config','AW-11553122519');gtag('config','AW-11553122519/JftTCI3O64QbENfR-oQr',{{'phone_conversion_css_class':'gfn','phone_conversion_number':'(410) 300-6743'}});</script>
    <meta charset=\"UTF-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <meta name=\"description\" content=\"{meta_description}\">
    <title>{page_title}</title>
    <link rel=\"canonical\" href=\"https://grimetodime.com/landing/{slug}/\"><link rel=\"icon\" type=\"image/png\" href=\"/images/Faviconmaster.png\">
    <link rel=\"preconnect\" href=\"https://www.googletagmanager.com\" crossorigin>
    <link rel=\"preconnect\" href=\"https://www.google-analytics.com\" crossorigin>
    <link rel=\"preconnect\" href=\"https://cdnjs.cloudflare.com\" crossorigin>
    <link rel=\"stylesheet\" href=\"https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css\">
    <link rel=\"preload\" as=\"image\" href=\"/images/optimized/warehouse-after-junk-removal-hero-800w.webp\" type=\"image/webp\" fetchpriority=\"high\">
    <style>
        html{{scroll-behavior:smooth}}*{{margin:0;padding:0;box-sizing:border-box}}body{{font-family:'Arial',sans-serif;line-height:1.6;color:#333;background:#f8f9fa}}
        header{{position:fixed;top:0;left:0;right:0;background:rgba(0,0,0,.85);z-index:1000}}.header-container{{max-width:1200px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;padding:.75rem 1rem}}.logo{{display:flex;align-items:center;color:#fff;text-decoration:none;font-weight:800}}.logo img{{height:44px;width:auto;margin-right:.5rem;display:block}}.gfn{{font-weight:800}}.phone-number{{color:#fff;text-decoration:none;font-weight:800;display:inline-flex;align-items:center;gap:.5rem}}.phone-number i{{color:#ff3333}}
        .hero{{background-image:linear-gradient(rgba(0,0,0,.6),rgba(0,0,0,.6)),image-set(url('/images/optimized/warehouse-after-junk-removal-hero-800w.webp') type('image/webp'),url('/images/optimized/warehouse-after-junk-removal-optimized.webp') type('image/webp'));background-size:cover;background-position:center;background-repeat:no-repeat;min-height:100vh;display:flex;align-items:center;padding:96px 1rem 2rem;color:#fff}}
        .hero-inner{{max-width:1200px;margin:0 auto;display:grid;grid-template-columns:1.1fr .9fr;gap:2rem;align-items:center}}.hero-content{{padding:1.5rem}}.hero h1{{font-size:3rem;font-weight:900;letter-spacing:-.02em;margin-bottom:.6rem;text-shadow:2px 2px 6px rgba(0,0,0,.4)}}.hero p.sub{{font-size:1.15rem;opacity:.95;margin-bottom:1rem}}
        .hero-bullets{{list-style:none;margin:1rem 0 1.25rem}}.hero-bullets li{{display:flex;align-items:center;gap:.6rem;margin-bottom:.5rem;font-weight:600}}.hero-bullets i{{color:#ff3333}}
        .cta-button{{background:#ff3333;color:#fff;text-decoration:none;display:inline-flex;align-items:center;justify-content:center;padding:14px 28px;border-radius:10px;font-weight:800;box-shadow:0 8px 24px rgba(255,51,51,.35);transition:transform .2s ease,box-shadow .2s ease,background .2s ease}}.cta-button:hover{{background:#e62e2e;transform:translateY(-2px);box-shadow:0 12px 34px rgba(255,51,51,.45)}}
        .google-rating-badge{{display:inline-flex;align-items:center;gap:.5rem;background:#fff;color:#222;border:1px solid #ff3333;border-radius:999px;padding:10px 14px;box-shadow:0 6px 18px rgba(255,51,51,.15)}}.google-rating-badge .google-icon{{color:#ff3333}}
        .card{{background:#fff;border:1px solid #e9ecef;border-radius:14px;box-shadow:0 8px 24px rgba(0,0,0,.06)}}.quote-card{{padding:1.5rem}}.quote-card h2{{text-align:center;color:#222;margin-bottom:1rem}}
        .form{{display:flex;flex-direction:column;gap:1rem}}label{{font-weight:700;color:#333}}input,textarea,select{{width:100%;padding:.8rem 1rem;border:1px solid #ced4da;border-radius:10px;font-family:inherit;font-size:1rem}}
        textarea{{min-height:110px;resize:vertical}}.submit-button{{background:#ff3333;color:#fff;border:none;border-radius:10px;padding:.9rem 1rem;font-weight:800;cursor:pointer;transition:transform .2s ease,background .2s ease}}.submit-button:hover{{background:#e62e2e;transform:translateY(-2px)}}.form-note{{text-align:center;color:#666;font-size:.92rem}}
        .section{{padding:3.5rem 1rem}}.container{{max-width:1200px;margin:0 auto}}.section h2{{text-align:center;font-size:2.2rem;font-weight:900;color:#222;margin-bottom:1.75rem}}
        .grid-3{{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem}}.grid-2{{display:grid;grid-template-columns:repeat(2,1fr);gap:1rem}}
        .feature{{padding:1.25rem;background:#fff;border:1px solid #e9ecef;border-radius:14px;box-shadow:0 8px 24px rgba(0,0,0,.06)}}.feature i{{color:#ff3333;font-size:1.4rem;margin-right:.4rem}}.feature h3{{font-size:1.2rem;margin-bottom:.35rem;color:#222}}.feature p{{color:#555}}
        .pill{{display:inline-flex;align-items:center;justify-content:center;padding:.6rem .9rem;border-radius:999px;font-weight:800;font-size:.95rem}}
        .chip{{background:rgba(255,51,51,.08);border:1px solid rgba(255,51,51,.22);color:#c22020}}
        @media (max-width:1024px){{.hero-inner{{grid-template-columns:1fr}}}}
        @media (max-width:768px){{.hero{{min-height:100svh;padding-top:72px}}.hero h1{{font-size:2.4rem}}.grid-3,.grid-2{{grid-template-columns:1fr}}.quote-card{{padding:1.25rem}}}}
    </style>
    <script>function gtagSendEvent(u){{var c=function(){{if(typeof u==='string')window.location=u}};gtag('event','select_content',{{content_type:'cta',event_label:'Service CTA',link_url:u,event_callback:c,event_timeout:2000}});return false;}}</script>
    __FORM_SCRIPT__

</head>
<body>
    <header><div class=\"header-container\"><a href=\"/\" class=\"logo\"><img src=\"/images/optimized/Faviconmaster-optimized.webp\" alt=\"Grime To Dime logo\"><span>Grime To Dime</span></a><a href=\"tel:+14103006743\" class=\"phone-number gfn\"><i class=\"fas fa-phone\"></i> (410) 300-6743</a></div></header>
    <section class=\"hero\"><div class=\"hero-inner\">
        <div class=\"hero-content\">
            <h1>{hero_heading}</h1>
            <p class=\"sub\">{hero_subheading}</p>
            <div class=\"google-rating-badge\" aria-label=\"5.0 based on 16 reviews\"><span class=\"google-icon\"><i class=\"fab fa-google\"></i></span><span class=\"rating-score\">5.0</span><span class=\"stars\">★★★★★</span><span class=\"badge-text\">16 reviews</span></div>
            <ul class=\"hero-bullets\">{hero_bullets}</ul>
            <a href=\"tel:+14103006743\" class=\"cta-button gfn\">{cta_button_label}</a>
        </div>
        <div class=\"card quote-card\">
            <h2>{quote_heading}</h2>
            <form id=\"quoteForm\" class=\"form\" action=\"https://formspree.io/f/meoovajl\" method=\"POST\" onsubmit=\"return handleFormSubmit(event)\">
                <input type=\"hidden\" name=\"_subject\" value=\"{form_subject}\">
                <input type=\"hidden\" name=\"_next\" value=\"https://grimetodime.com/thank-you.html\">
                <input type=\"text\" name=\"_gotcha\" style=\"display:none\" aria-hidden=\"true\" tabindex=\"-1\">
                <div><label for=\"name\">Full Name</label><input id=\"name\" name=\"_name\" type=\"text\" required autocomplete=\"name\"></div>
                <div><label for=\"phone\">Phone Number</label><input id=\"phone\" name=\"_phone\" type=\"tel\" required pattern=\"[\\d\\-\\+\\(\\)\\s]{{10,}}\" autocomplete=\"tel\"></div>
                <div><label for=\"email\">Email Address <span style=\"font-weight:400;color:#777\">(optional)</span></label><input id=\"email\" name=\"_replyto\" type=\"email\" autocomplete=\"email\" autocapitalize=\"off\" autocorrect=\"off\" spellcheck=\"false\" inputmode=\"email\"></div>
                <div><label for=\"details\">{details_label}</label><textarea id=\"details\" name=\"_message\" placeholder=\"{details_placeholder}\"></textarea></div>
                <button type=\"submit\" class=\"submit-button\">{submit_label}</button>
                <p class=\"form-note\">{form_note}</p>
            </form>
        </div>
    </div></section>
    <section class=\"section\"><div class=\"container\"><h2>What We Take</h2><div class=\"grid-3\">{what_we_take}</div></div></section>
    <section class=\"section\" style=\"background:#fff;\"><div class=\"container\"><h2>How It Works</h2><div class=\"grid-3\">{how_it_works}</div></div></section>
    <section class=\"section\" style=\"background:#f8f9fa;\"><div class=\"container\"><h2>Pricing & Availability</h2><div class=\"grid-2\">{pricing}</div><p style=\"text-align:center;margin-top:1rem\"><a class=\"cta-button gfn\" href=\"tel:+14103006743\">{pricing_cta}</a></p></div></section>
    <section class=\"section\"><div class=\"container\"><h2>Service Areas</h2><p style=\"text-align:center;margin-bottom:1rem;color:#555\">Howard County and nearby — including:</p><div style=\"display:flex;flex-wrap:wrap;gap:.6rem;justify-content:center\">{service_areas}</div></div></section>
    <section class=\"section\" id=\"faq\" style=\"background:#fff;\"><div class=\"container\"><h2>{faq_heading}</h2><div class=\"grid-2\">{faq}</div><p style=\"text-align:center;margin-top:1rem\"><a class=\"cta-button gfn\" href=\"tel:+14103006743\">{faq_cta}</a></p></div></section>
    <footer style=\"background:#111;color:#ddd;margin-top:2rem;\"><div style=\"max-width:1200px;margin:0 auto;padding:2rem 1rem;display:flex;gap:2rem;flex-wrap:wrap;justify-content:space-between;\"><div style=\"min-width:260px;flex:1;\"><h4 style=\"color:#fff;margin-bottom:.75rem;\">Grime To Dime</h4><p style=\"color:#ccc;line-height:1.6;\">Fast, friendly junk removal across Howard County. Same-day available. Licensed & insured. Upfront pricing.</p><p style=\"margin-top:.75rem;color:#bbb;\"><a class=\"gfn\" href=\"tel:+14103006743\" style=\"color:#fff;text-decoration:none;\">(410) 300-6743</a>&nbsp;·&nbsp;<a href=\"/quote/\" style=\"color:#ff6666;\">Get a free quote</a></p></div><div style=\"display:flex;gap:2rem;flex-wrap:wrap;flex:1;justify-content:flex-end;min-width:260px;\"><div><h4 style=\"color:#fff;margin-bottom:.75rem;\">Links</h4><ul style=\"list-style:none;padding:0;margin:0;line-height:1.9;\"><li><a href=\"/\" style=\"color:#ccc;text-decoration:none;\">Home</a></li><li><a href=\"/quote/\" style=\"color:#ccc;text-decoration:none;\">Quote</a></li><li><a href=\"/privacy-policy.html\" style=\"color:#ccc;text-decoration:none;\">Privacy</a></li></ul></div></div></div><div style=\"border-top:1px solid rgba(255,255,255,.1);padding:1rem;text-align:center;color:#888;\"><p style=\"margin:0;\">&copy; 2025 Grime To Dime. All rights reserved.</p></div></footer>
    <script type=\"application/ld+json\">{{\"@context\":\"https://schema.org\",\"@type\":\"Service\",\"name\":{json_service_name},\"serviceType\":{json_service_type},\"areaServed\":{json_area_served},\"provider\":{{\"@type\":\"LocalBusiness\",\"name\":\"Grime To Dime\",\"telephone\":\"+14103006743\",\"url\":\"https://grimetodime.com/\",\"image\":\"https://grimetodime.com/images/MASTERPARENT.png\"}}}}</script>
    <script type=\"application/ld+json\">{{\"@context\":\"https://schema.org\",\"@type\":\"FAQPage\",\"mainEntity\":{json_faq}}}</script>
</body>
</html>
"""


FORM_SCRIPT = """
    <script>
        function getQueryParam(n){var p=new URLSearchParams(window.location.search);var v=p.get(n);return v&&v.trim()?v.trim():''}
        function setCookie(n,v,a){if(!n)return;var parts=[n+'='+encodeURIComponent(v||'')];parts.push('path=/');if(a)parts.push('max-age='+a);parts.push('samesite=Lax');if(location.protocol==='https:')parts.push('secure');document.cookie=parts.join('; ')}
        function getCookie(n){var m=document.cookie.match(new RegExp('(?:^|; )'+n.replace(/([.$?*|{{}}()\[\]\/\+^])/g,'\\$1')+'=([^;]*)'));return m?decodeURIComponent(m[1]):''}
        function storeGclidFromUrl(){var g=getQueryParam('gclid');if(!g)return;try{localStorage.setItem('gclid',g);}catch(e){} setCookie('gclid',g,60*60*24*90)}
        function getStoredGclid(){try{var ls=localStorage.getItem('gclid');if(ls)return ls;}catch(e){} return getCookie('gclid')||''}
        function ensureGclidInput(f){if(!f)return;var el=f.querySelector('input[name="gclid"]');if(!el){el=document.createElement('input');el.type='hidden';el.name='gclid';f.appendChild(el)}var v=getStoredGclid();if(v)el.value=v}
        document.addEventListener('DOMContentLoaded',function(){try{storeGclidFromUrl();}catch(e){} var f=document.getElementById('quoteForm'); if(f) try{ensureGclidInput(f);}catch(e){}});
        function handleFormSubmit(ev){ev.preventDefault();var name=document.getElementById('name').value;var phone=document.getElementById('phone').value;var email=document.getElementById('email').value; if(!name||!phone){alert('Please provide your name and phone.');return false} var er=/^[^\s@]+@[^\s@]+\.[^\s@]+$/; if(email && !er.test(email)){alert('Please enter a valid email.');return false} var pr=/(\+?1[-. ]?)?\(?([0-9]{{3}})\)?[-. ]?([0-9]{{3}})[-. ]?([0-9]{{4}})$/; if(!pr.test(phone)){alert('Please enter a valid phone.');return false}
            var form=document.getElementById('quoteForm'); try{ensureGclidInput(form);}catch(e){} var btn=document.querySelector('.submit-button'); var t=btn.innerHTML; btn.innerHTML='<i class="fas fa-spinner fa-spin"></i> Processing...'; btn.disabled=true; var fd=new FormData(form); fetch(form.action,{method:'POST',body:fd,headers:{'Accept':'application/json'}}).then(function(r){ if(r.ok){ if(typeof gtag!=='undefined'){ gtag('event','generate_lead'); gtag('event','form_submission',{ 'event_category':'Quote','event_label':'{form_event_label}' }); gtag('event','conversion',{ 'send_to':'AW-11553122519/0KjoCPG_6oQbENfR-oQr','value':1.0,'transaction_id':'lead_'+Date.now().toString() }); } window.location.href=form.getAttribute('_next')||'/thank-you.html'; } else { throw new Error('Network response was not ok'); }}).catch(function(e){ console.error('Error:',e); btn.innerHTML=t; btn.disabled=false; alert('There was a problem submitting your form. Please try again.');}); return false; }
    </script>
"""

SERVICE_AREAS = [
    ("Ellicott City", "/locations/ellicott-city-md/"),
    ("Columbia", "/locations/columbia-md/"),
    ("Elkridge", "/locations/elkridge-md/"),
    ("Clarksville", "/locations/clarksville-md/"),
    ("Laurel", "/locations/laurel-md/"),
    ("Savage", "/locations/savage-md/"),
    ("Catonsville", "/locations/catonsville-md/"),
]


def slugify(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower())
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug or "landing-page"


def bullet_list_html(items: List[str]) -> str:
    return "".join(
        f"<li><i class=\"fas fa-check-circle\"></i>{html.escape(item)}</li>" for item in items
    )


def feature_cards_html(items: List[Dict[str, str]]) -> str:
    icons = ["fa-tv", "fa-recycle", "fa-couch", "fa-box", "fa-bolt", "fa-calendar-check"]
    html_blocks = []
    for idx, item in enumerate(items):
        icon = icons[idx % len(icons)]
        title = html.escape(item.get("title", ""))
        desc = html.escape(item.get("description", ""))
        html_blocks.append(
            f"<div class=\"feature\"><h3><i class=\"fas {icon}\"></i> {title}</h3><p>{desc}</p></div>"
        )
    return "".join(html_blocks)


def faq_html(items: List[Dict[str, str]]) -> str:
    html_blocks = []
    for item in items:
        q = html.escape(item.get("question", ""))
        a = html.escape(item.get("answer", ""))
        html_blocks.append(f"<div class=\"feature\"><h3>{q}</h3><p>{a}</p></div>")
    return "".join(html_blocks)


def service_areas_html() -> str:
    return "".join(
        f"<a class=\"pill chip\" href=\"{html.escape(url)}\">{html.escape(name)}</a>"
        for name, url in SERVICE_AREAS
    )


def faq_json_ld(items: List[Dict[str, str]]) -> List[Dict[str, str]]:
    entities = []
    for item in items:
        question = item.get("question", "").strip()
        answer = item.get("answer", "").strip()
        if question and answer:
            entities.append(
                {
                    "@type": "Question",
                    "name": question,
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": answer,
                    },
                }
            )
    return entities


# ---------------------------------------------------------------------------
# Generation pipeline
# ---------------------------------------------------------------------------


def load_groups(path: Path) -> List[Dict]:
    with path.open() as f:
        data = json.load(f)
    groups = data.get("groups") or []
    if not isinstance(groups, list):
        raise ValueError("JSON structure invalid: expected 'groups' list")
    return groups


def build_prompt_for_group(group: Dict) -> List[Dict[str, str]]:
    keywords = group.get("keywords", [])
    top_keywords = keywords[:20]
    keywords_bullets = "\n".join(f"- {kw}" for kw in top_keywords)

    user_prompt = CONTENT_PROMPT_TEMPLATE.format(
        group_name=group.get("name", ""),
        description=group.get("description", ""),
        primary_keyword=group.get("primary_keyword", ""),
        keywords_bullets=keywords_bullets or "- (keywords unavailable)",
    )

    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]


def render_page_html(slug: str, group: Dict, content: Dict) -> str:
    hero = content.get("hero") or {}
    quote_form = content.get("quote_form") or {}
    what_we_take = content.get("what_we_take") or []
    how_it_works = content.get("how_it_works") or []
    pricing = content.get("pricing") or []
    faq_items = content.get("faq") or []
    closing_cta = content.get("closing_cta") or {}

    faq_entities = faq_json_ld(faq_items)

    html_output = HTML_TEMPLATE.format(
        meta_description=html.escape(content.get("meta_description", "")),
        page_title=html.escape(content.get("page_title", "")),
        slug=slug,
        hero_heading=html.escape(hero.get("heading", group.get("name", ""))),
        hero_subheading=html.escape(hero.get("subheading", group.get("description", ""))),
        hero_bullets=bullet_list_html(hero.get("bullets", [])[:3]),
        cta_button_label=html.escape(closing_cta.get("button_label", "Get Free Quote")),
        quote_heading=html.escape(quote_form.get("heading", "Free Quote")),
        form_subject=html.escape(quote_form.get("form_subject", f"{group.get('name', 'Service')} Quote Request")),
        details_label=html.escape(quote_form.get("details_label", "What are we removing?")),
        details_placeholder=html.escape(quote_form.get("details_placeholder", "Item details, access notes, photos")),
        submit_label=html.escape(quote_form.get("submit_label", "Get My Quote")),
        form_note=html.escape(quote_form.get("note", "Prefer text? Send photos to (410) 300-6743.")),
        what_we_take=feature_cards_html(what_we_take[:3]),
        how_it_works=feature_cards_html(how_it_works[:3]),
        pricing=feature_cards_html(pricing[:2]),
        pricing_cta=html.escape(closing_cta.get("button_label", "Check My Price")),
        service_areas=service_areas_html(),
        faq_heading=html.escape(f"{group.get('name', 'Service')} FAQ"),
        faq=faq_html(faq_items[:4]),
        faq_cta=html.escape(closing_cta.get("button_label", "Book My Pickup")),
        json_service_name=json.dumps(content.get("hero", {}).get("heading", group.get("name", ""))),
        json_service_type=json.dumps(content.get("service_type", group.get("name", ""))),
        json_area_served=json.dumps([name for name, _ in SERVICE_AREAS]),
        json_faq=json.dumps(faq_entities),
    )
    
    # Replace the form script placeholder
    # Simple form script injection without complex formatting
    simple_form_script = """
    <script>
        function getQueryParam(n){var p=new URLSearchParams(window.location.search);var v=p.get(n);return v&&v.trim()?v.trim():''}
        function setCookie(n,v,a){if(!n)return;var parts=[n+'='+encodeURIComponent(v||'')];parts.push('path=/');if(a)parts.push('max-age='+a);parts.push('samesite=Lax');if(location.protocol==='https:')parts.push('secure');document.cookie=parts.join('; ')}
        function getCookie(n){var m=document.cookie.match(new RegExp('(?:^|; )'+n.replace(/([.$?*|{}()\\[\\]\\\\\\+^])/g,'\\\\$1')+'=([^;]*)'));return m?decodeURIComponent(m[1]):''}
        function storeGclidFromUrl(){var g=getQueryParam('gclid');if(!g)return;try{localStorage.setItem('gclid',g);}catch(e){} setCookie('gclid',g,60*60*24*90)}
        function getStoredGclid(){try{var ls=localStorage.getItem('gclid');if(ls)return ls;}catch(e){} return getCookie('gclid')||''}
        function ensureGclidInput(f){if(!f)return;var el=f.querySelector('input[name="gclid"]');if(!el){el=document.createElement('input');el.type='hidden';el.name='gclid';f.appendChild(el)}var v=getStoredGclid();if(v)el.value=v}
        document.addEventListener('DOMContentLoaded',function(){try{storeGclidFromUrl();}catch(e){} var f=document.getElementById('quoteForm'); if(f) try{ensureGclidInput(f);}catch(e){}});
        function handleFormSubmit(ev){ev.preventDefault();var name=document.getElementById('name').value;var phone=document.getElementById('phone').value;var email=document.getElementById('email').value; if(!name||!phone){alert('Please provide your name and phone.');return false} var er=/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/; if(email && !er.test(email)){alert('Please enter a valid email.');return false} var pr=/(\\+?1[-. ]?)?\\(?([0-9]{3})\\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$/; if(!pr.test(phone)){alert('Please enter a valid phone.');return false}
            var form=document.getElementById('quoteForm'); try{ensureGclidInput(form);}catch(e){} var btn=document.querySelector('.submit-button'); var t=btn.innerHTML; btn.innerHTML='<i class="fas fa-spinner fa-spin"></i> Processing...'; btn.disabled=true; var fd=new FormData(form); fetch(form.action,{method:'POST',body:fd,headers:{'Accept':'application/json'}}).then(function(r){ if(r.ok){ if(typeof gtag!=='undefined'){ gtag('event','generate_lead'); gtag('event','form_submission',{ 'event_category':'Quote','event_label':'""" + html.escape(group.get("name", "Landing Page")) + """' }); gtag('event','conversion',{ 'send_to':'AW-11553122519/0KjoCPG_6oQbENfR-oQr','value':1.0,'transaction_id':'lead_'+Date.now().toString() }); } window.location.href=form.getAttribute('_next')||'/thank-you.html'; } else { throw new Error('Network response was not ok'); }}).catch(function(e){ console.error('Error:',e); btn.innerHTML=t; btn.disabled=false; alert('There was a problem submitting your form. Please try again.');}); return false; }
    </script>
    """
    
    return html_output.replace("__FORM_SCRIPT__", simple_form_script)


def ensure_output_directory(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    default_groups = project_root / "keyword_groups_for_landing_pages.json"
    default_output = project_root / "landing"

    parser = argparse.ArgumentParser(description="Generate landing pages from keyword groups using Grok-4-fast")
    parser.add_argument("--groups", type=Path, default=default_groups, help="Path to grouped keyword JSON")
    parser.add_argument("--output", type=Path, default=default_output, help="Directory to write generated landing pages")
    parser.add_argument("--model", type=str, default="grok-4-fast", help="Model name for Grok")
    parser.add_argument("--limit", type=int, default=None, help="Optional limit on number of groups to render")
    parser.add_argument("--skip-existing", action="store_true", help="Skip groups whose slug directory already exists")

    args = parser.parse_args()

    groups = load_groups(args.groups)
    if args.limit is not None:
        groups = groups[: args.limit]

    print(f"Loaded {len(groups)} keyword groups from {args.groups}")
    ensure_output_directory(args.output)

    for idx, group in enumerate(groups, 1):
        group_name = group.get("name", f"Group {idx}")
        slug = slugify(group_name)
        output_dir = args.output / slug
        output_file = output_dir / "index.html"

        if args.skip_existing and output_file.exists():
            print(f"[{idx}/{len(groups)}] Skipping {group_name} (exists)")
            continue

        print(f"[{idx}/{len(groups)}] Generating copy for '{group_name}' …")
        messages = build_prompt_for_group(group)
        try:
            content = call_grok(messages, model=args.model)
        except GrokError as exc:
            print(f"  Error from Grok: {exc}")
            continue

        ensure_output_directory(output_dir)
        page_html = render_page_html(slug, group, content)
        output_file.write_text(page_html, encoding="utf-8")
        print(f"  Saved {output_file}")

    print("Generation complete.")
    
    # Update sitemap with new pages
    try:
        print("\n🗺️  Updating sitemap.xml...")
        integrate_with_generator()
    except Exception as e:
        print(f"⚠️  Sitemap update failed: {e}")


if __name__ == "__main__":
    main()
