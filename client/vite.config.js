import { fileURLToPath, URL } from "node:url";

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

// Exports a default object that defines a Vite configuration
// resolve is an object that defines how to resolve imports in the project
// server is an object that configures the development server used by Vite
// https://vitejs.dev/config/
export default defineConfig({
   plugins: [vue()],
   resolve: {
      alias: {
         "@": fileURLToPath(new URL("./src", import.meta.url)),
      },
   },
   server: {
      proxy: {
         "/api/": {
            target: "http://127.0.0.1:5000",
            rewrite: (path) => path.replace(/^\/api/, ""),
         },
         "/images": {
            target: "http://127.0.0.1:5000"
         }
      },
   },
});
