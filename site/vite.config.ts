import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "node:path";

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@charts": path.resolve(__dirname, "../charts"),
      "@design": path.resolve(__dirname, "../design-system"),
    },
  },
});
