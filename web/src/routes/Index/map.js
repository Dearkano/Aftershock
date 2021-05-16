import React, { useEffect, useState } from "react";
import { connect } from "dva";
import styles from "./index.less";
import * as d3 from "d3";
import * as topojson from "topojson-client";
import worldmap from "./geo";
import dayjs from "dayjs";
import { Modal, Statistic, Card, Row, Col } from "antd";
import { ArrowUpOutlined, ArrowDownOutlined } from "@ant-design/icons";

function Map({ map, dispatch, showModal }) {
  const { data, prediction } = map;

  useEffect(() => {
    const width = 960;
    const height = 600;
    const projection = d3.geoMercator();
    const path = d3.geoPath().projection(projection);
    const zoom = d3.zoom().scaleExtent([1, 8]).on("zoom", zoomed);
    const svg = d3
      .select("#map")
      .append("svg")
      .attr("viewBox", [0, 0, width, height]);

    const g = svg
      .append("g")
      .attr("fill", "#ddd")
      .attr("cursor", "pointer")
      .selectAll("path")
      .data(worldmap.features)
      .join("path")
      .attr("d", path);

    const div = d3
      .select("body")
      .append("div")
      .attr("class", "tooltip")
      .style("opacity", 0);

    const g1 = svg
      .append("g")
      .selectAll("circles")
      .data(data)
      .enter()
      .append("circle")
      .attr("cx", function (d) {
        return projection([d.longitude, d.latitude])[0];
      })
      .attr("cy", function (d) {
        return projection([d.longitude, d.latitude])[1];
      })
      .attr("r", (d) => d.mag)
      .attr("fill", "red")
      .attr("fill-opacity", 0.5)
      .attr("stroke", "#fff")
      .attr("stroke-width", 0.5)
      .on("mouseover", function (event, d) {
        div.transition().duration(200).style("opacity", 0.9);
        div
          .html(
            d.place +
              "<br/>" +
              "Mag: " +
              d.mag +
              "<br />" +
              dayjs(d.time).format("YYYY-MM-DD hh:mm:ss")
          )
          .style("left", event.pageX + "px")
          .style("top", event.pageY - 28 + "px");
      })
      .on("mouseout", function (d) {
        div.transition().duration(500).style("opacity", 0);
      })
      .on("click", function (e, d) {
        dispatch({
          type: "map/predict",
          payload: {
            data: d,
          },
        });
        showModal();
      });

    svg.call(zoom);

    //   function reset() {
    //     states.transition().style("fill", null);
    //     svg
    //       .transition()
    //       .duration(750)
    //       .call(
    //         zoom.transform,
    //         d3.zoomIdentity,
    //         d3.zoomTransform(svg.node()).invert([width / 2, height / 2])
    //       );
    //   }

    function zoomed(event) {
      const { transform } = event;
      g.attr("transform", transform);
      g.attr("stroke-width", 1 / transform.k);
      g1.attr("transform", transform);
      g1.attr("stroke-width", 1 / transform.k);
    }
  }, []);
  return (
    <React.Fragment>
      <div id="map" className={styles.normal}></div>{" "}
    </React.Fragment>
  );
}

export default connect(({ map }) => ({ map }))(Map);
