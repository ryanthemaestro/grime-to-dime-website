export default async function handler(request, context) {
  try {
    const url = new URL(request.url);
    const path = url.pathname;

    // Only act on /blog or /blog/ with undesired query params
    if ((path === '/blog' || path === '/blog/') && (url.searchParams.has('category') || url.searchParams.has('tag'))) {
      return Response.redirect('https://grimetodime.com/blog/', 301);
    }

    // Let other requests continue
    return context.next();
  } catch (e) {
    // Fail open to avoid breaking the site
    return context.next();
  }
}

