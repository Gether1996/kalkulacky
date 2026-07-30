export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000/api',
  // Base URL the SSR server uses to reach the API (server-to-server). In dev
  // this is the Docker service name; set it per environment rather than
  // hardcoding it in a service.
  ssrApiUrl: 'http://backend:8000/api',
  googleClientId: '', // Add your Google OAuth Client ID here
  adsensePublisherId: '' // e.g. 'ca-pub-XXXXXXXXXXXXXXXX' — empty = ads off
};
