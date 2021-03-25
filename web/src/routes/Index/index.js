import React, { useEffect, useState } from "react";
import { connect } from "dva";
import { Select, Spin, List, Card } from "antd";
import styles from "./index.less";
import Map from "./map";
import dayjs from "dayjs";

function IndexPage({ dispatch, map, loading }) {
  useEffect(() => {
    dispatch({
      type: "map/getData",
      payload: `${mag}_${time}`,
    });
  }, []);

  const [mag, setMag] = useState("2.5");
  const [time, setTime] = useState("day");

  const changeTime = (v) => {
    setTime(v);
    dispatch({
      type: "map/getData",
      payload: `${mag}_${v}`,
    });
  };

  const changeMag = (v) => {
    setMag(v);
    dispatch({
      type: "map/getData",
      payload: `${v}_${time}`,
    });
  };
  return (
    <div className={styles.normal}>
      <div className={styles.menu}>
        <div className={styles.column}>
          <div className={styles.label}>Magnitude</div>
          <Select
            defaultValue="2.5"
            style={{ width: "12rem" }}
            onChange={changeMag}
          >
            <Select.Option value="1.0">1.0</Select.Option>
            <Select.Option value="2.5">2.5</Select.Option>
            <Select.Option value="4.5">4.5</Select.Option>
            <Select.Option value="significant">Significant</Select.Option>
            <Select.Option value="all">All</Select.Option>
          </Select>
          <div className={styles.label} style={{ marginTop: "1rem" }}>
            Time
          </div>
          <Select
            defaultValue="day"
            style={{ width: "12rem" }}
            onChange={changeTime}
          >
            <Select.Option value="hour">Past hour</Select.Option>
            <Select.Option value="day">Past day</Select.Option>
            <Select.Option value="week">Past week</Select.Option>
            <Select.Option value="month">Past month</Select.Option>
          </Select>
          {map.data.features && (
            <List
              style={{
                maxHeight: "85vh",
                overflowY: "scroll",
                paddingLeft: "1rem",
                paddingRight: "1rem",
                marginTop: "1rem",
              }}
            >
              {map.data.features.map((item) => (
                <List.Item>
                  <Card
                    style={{ width: "18rem" }}
                    title={item.properties.place}
                    extra={<span>{item.properties.mag}</span>}
                  >
                    <p>
                      Location: {Math.abs(item.geometry.coordinates[0])}°
                      {item.geometry.coordinates[0] > 0 ? "N" : "S"}
                      {Math.abs(item.geometry.coordinates[1])}°
                      {item.geometry.coordinates[1] > 0 ? "E" : "W"}
                    </p>
                    <p>Depth: {item.geometry.coordinates[2]}km</p>
                  </Card>
                </List.Item>
              ))}
            </List>
          )}
        </div>
      </div>
      <div className={styles.mapContainer}>
        {map.data.features && !loading && <Map data={map.data.features} />}
        {loading && <Spin size="large" />}
      </div>
    </div>
  );
}

IndexPage.propTypes = {};

export default connect(({ map, loading }) => ({
  map,
  loading: loading.global,
}))(IndexPage);
