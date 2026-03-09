/** Vite dev server for the static public website. In this repo, files are at repo root; in monorepo, use root: 'public-web'. */
export default {
  root: '.',
  server: {
    port: 5500,
    open: true,
    watch: {
      usePolling: true,
    },
  },
};
