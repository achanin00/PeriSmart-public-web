/** Vite dev server for the static public website (public-web/). */
export default {
  root: 'public-web',
  server: {
    port: 5500,
    open: true,
    watch: {
      usePolling: true,
    },
  },
};
