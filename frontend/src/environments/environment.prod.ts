export const environment = {
  production: true,
  apiUrl: 'https://kalkulacky.sk/api',
  // SSR server-to-API base URL. Defaults to the public API; override to an
  // internal address if the SSR server reaches the backend on a private network.
  ssrApiUrl: 'https://kalkulacky.sk/api',
  googleClientId: '', // Add your production Google OAuth Client ID here
  adsensePublisherId: '' // e.g. 'ca-pub-XXXXXXXXXXXXXXXX' — empty = ads off
};
