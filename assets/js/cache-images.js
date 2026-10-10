// Cache external images locally when running on 127.0.0.1 or localhost
(function() {
  // Only run on local development
  const isLocal = window.location.hostname === '127.0.0.1' ||
                  window.location.hostname === 'localhost';

  if (!isLocal) return;

  document.addEventListener('DOMContentLoaded', function() {
    const images = document.querySelectorAll('img[src^="http://"], img[src^="https://"]');

    images.forEach(img => {
      const originalUrl = img.getAttribute('src');
      if (!originalUrl) return;

      // Parse the URL to extract domain and path
      try {
        const urlObj = new URL(originalUrl);
        const domain = urlObj.hostname;
        const pathname = urlObj.pathname;

        // Create the local cache path: /equilibrium/assets/cache/<domain><pathname>
        // Strip leading underscores from each component: Jekyll excludes any file/directory
        // whose name starts with '_' at any depth, so we sanitize to match what the
        // cache-images.py script writes.
        const sanitizedPathname = pathname.split('/').map(p => p.replace(/^_+/, '')).join('/');
        const localPath = `/equilibrium/assets/cache/${domain}${sanitizedPathname}`;

        img.setAttribute('src', localPath);
      } catch (e) {
        // If URL parsing fails, leave the image as-is
        console.warn('Failed to parse image URL:', originalUrl, e);
      }
    });
  });
})();
