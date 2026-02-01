// Cache external images locally when running on 127.0.0.1 or localhost
(function() {
  // Only run on local development
  const isLocal = window.location.hostname === '127.0.0.1' ||
                  window.location.hostname === 'localhost';

  if (!isLocal) return;

  document.addEventListener('DOMContentLoaded', function() {
    const images = document.querySelectorAll('img[src^="http://"], img[src^="https://"]');

    images.forEach(img => {
      let originalUrl = img.getAttribute('src');
      if (!originalUrl) return;

      // Apply Pinterest 400x optimization if applicable
      if (originalUrl.includes('i.pinimg.com/originals/')) {
        // Convert /originals/ to /400x/ and change extension to .jpg
        originalUrl = originalUrl.replace('/originals/', '/400x/');
        // Convert .png, .webp, .gif to .jpg (handle query strings)
        originalUrl = originalUrl.replace(/\.(png|webp|gif)(\?|$)/i, '.jpg$2');
      }

      // Parse the URL to extract domain and path
      try {
        const urlObj = new URL(originalUrl);
        const domain = urlObj.hostname;
        const pathname = urlObj.pathname;

        // Create the local cache path: /equilibrium/assets/cache/<domain><pathname>
        const localPath = `/equilibrium/assets/cache/${domain}${pathname}`;

        img.setAttribute('src', localPath);
      } catch (e) {
        // If URL parsing fails, leave the image as-is
        console.warn('Failed to parse image URL:', originalUrl, e);
      }
    });
  });
})();
