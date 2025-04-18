import { sveltekit } from "@sveltejs/kit/vite";
import { defineConfig } from "vite";
import copy from "rollup-plugin-copy";

export default defineConfig({
  plugins: [
    copy({
      targets: [
        {
          src: "node_modules/@nutrient-sdk/viewer/dist/nutrient-viewer-lib",
          dest: "static/",
        },
      ],
	  optimizeDeps: {
		include: ['pdfjs-dist/build/pdf'],
	  },
      hook: "buildStart",
    }),
    sveltekit(),
  ],
});

