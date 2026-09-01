import { defineRailway, project, service } from "railway/iac";

// This repo deploys the existing canonical static proof-pack service.
export const partial = "refreshing-art";

export default defineRailway(() => {
  const refreshing_art = service("refreshing-art", {
    healthcheck: "/",
    healthcheckTimeout: 60,
    // dockerfilePath from CaC: "Dockerfile"
    // builder from CaC: "DOCKERFILE"
  });
  return project("refreshing-art", {
    resources: [refreshing_art],
  });
});
