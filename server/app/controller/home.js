"use strict";

const Controller = require("egg").Controller;
const fetch = require("node-fetch");
const config = require("../../config/azure");

const databaseId = config.database.id;
const containerId = config.container.id;

class HomeController extends Controller {
  async index() {
    const { ctx } = this;
    ctx.body = "hi, egg";
  }

  async query_earthquake() {
    const { mag, range } = this.ctx.query;
    const now = Date.now();
    console.log(range);
    let hour = 0;
    switch (range) {
      case "hour":
        hour = 1;
        break;
      case "day":
        hour = 24;
        break;
      case "week":
        hour = 24 * 7;
        break;
      case "month":
        hour = 24 * 30;
        break;
      case "year":
        hour = 24 * 365;
        break;
    }
    const time = now - 1000 * 60 * 60 * hour;
    const querySpec = {
      query: "SELECT VALUE r FROM root r WHERE r.mag > @mag AND r.time > @time",
      parameters: [
        {
          name: "@mag",
          value: Number(mag),
        },
        {
          name: "@time",
          value: time,
        },
      ],
    };
    const { resources: results } = await this.app.client
      .database(databaseId)
      .container(containerId)
      .items.query(querySpec)
      .fetchAll();
    this.ctx.body = results;
  }

  async predict() {
    const { mag, mmi, sig, depth, n_foreshocks } = this.ctx.query;
    const maxs = [9.1, 9.422, 2910, 691.6, 4577];
    const mins = [5.0, 0, 385, -1.77, 0];
    const norm = (x, min, max) => (x - min) / (max - min);
    const res = await fetch(
      `http://d65d760a-ffc8-471c-9d4a-61c05dc82b76.westus.azurecontainer.io/score?data=[[${[
        mag,
        sig,
        depth,
        n_foreshocks,
      ].map((x, i) => norm(x, mins[i], maxs[i]))}]]`
    );
    const d = await res.json();
    this.ctx.body = d;
  }
}

module.exports = HomeController;
