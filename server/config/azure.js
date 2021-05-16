var config = require("../db.json");
var azureConfig = {};
azureConfig.endpoint = "https://5412fpcosmos.documents.azure.com:443/";
azureConfig.key = config.azure_key;

azureConfig.database = {
  id: "db",
};

azureConfig.container = {
  id: "usgs_earthquake",
};
module.exports = azureConfig;
