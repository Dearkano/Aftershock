import React, { useEffect, useState } from "react";
import { connect } from "dva";
import { Select, Spin, List, Modal, Statistic, Card, Row, Col } from "antd";
import { ArrowUpOutlined, ArrowDownOutlined } from "@ant-design/icons";
import styles from "./index.less";
import Map from "./map";
import dayjs from "dayjs";

function IndexPage({ dispatch, map, loading }) {
  useEffect(() => {
    dispatch({
      type: "map/getData",
      payload: {
        mag,
        time,
      },
    });
  }, []);
  const { prediction } = map;

  const [mag, setMag] = useState("4.5");
  const [time, setTime] = useState("week");
  const [isModalVisible, setIsModalVisible] = useState(false);

  const showModal = () => {
    setIsModalVisible(true);
  };

  const handleOk = () => {
    setIsModalVisible(false);
  };

  const handleCancel = () => {
    setIsModalVisible(false);
  };

  const predict = (item) => {
    dispatch({
      type: "map/predict",
      data: item,
    });
    showModal();
  };

  const changeTime = (v) => {
    setTime(v);
    dispatch({
      type: "map/getData",
      payload: { mag, time: v },
    });
  };

  const changeMag = (v) => {
    setMag(v);
    dispatch({
      type: "map/getData",
      payload: { mag: v, time },
    });
  };
  return (
    <div className={styles.normal}>
      <div className={styles.menu}>
        <div className={styles.column}>
          <div className={styles.label}>Magnitude</div>
          <Select
            defaultValue="4.5"
            style={{ width: "12rem" }}
            onChange={changeMag}
          >
            <Select.Option value="1.0">1.0</Select.Option>
            <Select.Option value="2.5">2.5</Select.Option>
            <Select.Option value="4.5">4.5</Select.Option>
            <Select.Option value="6.0">Significant</Select.Option>
            <Select.Option value="0">All</Select.Option>
          </Select>
          <div className={styles.label} style={{ marginTop: "1rem" }}>
            Time
          </div>
          <Select
            defaultValue="week"
            style={{ width: "12rem" }}
            onChange={changeTime}
          >
            <Select.Option value="hour">Past hour</Select.Option>
            <Select.Option value="day">Past day</Select.Option>
            <Select.Option value="week">Past week</Select.Option>
            <Select.Option value="month">Past month</Select.Option>
            <Select.Option value="year">Past Year</Select.Option>
          </Select>
          {map.data.length > 0 && (
            <List
              style={{
                maxHeight: "85vh",
                overflowY: "scroll",
                paddingLeft: "1rem",
                paddingRight: "1rem",
                marginTop: "1rem",
              }}
            >
              {map.data.map((item) => (
                <List.Item>
                  <Card
                    style={{ width: "18rem", cursor: "pointer" }}
                    title={item.place}
                    extra={<span>{item.mag}</span>}
                    onClick={(item) => predict(item)}
                  >
                    <p>
                      Location: {Math.abs(item.longitude)}°
                      {item.longitude > 0 ? "N" : "S"}
                      {Math.abs(item.latitude)}
                      {item.latitude > 0 ? "E" : "W"}
                    </p>
                    <p>Depth: {item.depth}km</p>
                  </Card>
                </List.Item>
              ))}
            </List>
          )}
        </div>
      </div>
      <div className={styles.mapContainer}>
        {map.data.length > 0 && <Map showModal={showModal} />}
        {loading && <Spin size="large" />}
      </div>
      <Modal
        title="Aftershock Forecast"
        visible={isModalVisible}
        onOk={handleOk}
        onCancel={handleCancel}
        width={800}
      >
        <div className={styles.card}>
          <Row>Daily Forecast</Row>
          <Row gutter={16}>
            <Col span={8}>
              <Card>
                <Statistic
                  title="Microseism"
                  value={prediction[0]}
                  precision={0}
                  valueStyle={{
                    color:
                      prediction[3] < 5 * prediction[0] ? "#3f8600" : "#cf1322",
                  }}
                  prefix={
                    prediction[3] < 5 * prediction[0] ? (
                      <ArrowUpOutlined />
                    ) : (
                      <ArrowDownOutlined />
                    )
                  }
                />
              </Card>
            </Col>
            <Col span={8}>
              <Card>
                <Statistic
                  title="Normal"
                  value={prediction[1]}
                  precision={0}
                  valueStyle={{
                    color:
                      prediction[4] < 5 * prediction[1] ? "#3f8600" : "#cf1322",
                  }}
                  prefix={
                    prediction[4] < 5 * prediction[1] ? (
                      <ArrowUpOutlined />
                    ) : (
                      <ArrowDownOutlined />
                    )
                  }
                />
              </Card>
            </Col>
            <Col span={8}>
              <Card>
                <Statistic
                  title="Significant"
                  value={prediction[2]}
                  precision={0}
                  valueStyle={{
                    color:
                      prediction[5] < 5 * prediction[2] ? "#3f8600" : "#cf1322",
                  }}
                  prefix={
                    prediction[5] < 5 * prediction[2] ? (
                      <ArrowUpOutlined />
                    ) : (
                      <ArrowDownOutlined />
                    )
                  }
                />
              </Card>
            </Col>
          </Row>
          <Row>Weekly Forecast</Row>
          <Row gutter={16}>
            <Col span={8}>
              <Card>
                <Statistic
                  title="Microseism"
                  value={prediction[3]}
                  precision={0}
                  valueStyle={{
                    color:
                      prediction[6] < 5 * prediction[3] ? "#3f8600" : "#cf1322",
                  }}
                  prefix={
                    prediction[6] < 5 * prediction[3] ? (
                      <ArrowUpOutlined />
                    ) : (
                      <ArrowDownOutlined />
                    )
                  }
                />
              </Card>
            </Col>
            <Col span={8}>
              <Card>
                <Statistic
                  title="Normal"
                  value={prediction[4]}
                  precision={0}
                  valueStyle={{
                    color:
                      prediction[7] < 5 * prediction[4] ? "#3f8600" : "#cf1322",
                  }}
                  prefix={
                    prediction[7] < 5 * prediction[4] ? (
                      <ArrowUpOutlined />
                    ) : (
                      <ArrowDownOutlined />
                    )
                  }
                />
              </Card>
            </Col>
            <Col span={8}>
              <Card>
                <Statistic
                  title="Significant"
                  value={prediction[5]}
                  precision={0}
                  valueStyle={{
                    color:
                      prediction[8] < 5 * prediction[5] ? "#3f8600" : "#cf1322",
                  }}
                  prefix={
                    prediction[8] < 5 * prediction[5] ? (
                      <ArrowUpOutlined />
                    ) : (
                      <ArrowDownOutlined />
                    )
                  }
                />
              </Card>
            </Col>
          </Row>{" "}
          <Row>Monthly Forecast</Row>
          <Row gutter={16}>
            <Col span={8}>
              <Card>
                <Statistic
                  title="Microseism"
                  value={prediction[6]}
                  precision={0}
                  valueStyle={{
                    color:
                      prediction[7] < 5 * prediction[6] ? "#3f8600" : "#cf1322",
                  }}
                  prefix={
                    prediction[7] < 5 * prediction[6] ? (
                      <ArrowUpOutlined />
                    ) : (
                      <ArrowDownOutlined />
                    )
                  }
                />
              </Card>
            </Col>
            <Col span={8}>
              <Card>
                <Statistic
                  title="Normal"
                  value={prediction[7]}
                  precision={0}
                  valueStyle={{
                    color:
                      prediction[8] < 5 * prediction[7] ? "#3f8600" : "#cf1322",
                  }}
                  prefix={
                    prediction[8] < 5 * prediction[7] ? (
                      <ArrowUpOutlined />
                    ) : (
                      <ArrowDownOutlined />
                    )
                  }
                />
              </Card>
            </Col>
            <Col span={8}>
              <Card>
                <Statistic
                  title="Significant"
                  value={prediction[8]}
                  precision={0}
                  valueStyle={{
                    color:
                      prediction[8] > 5 * prediction[7] ? "#3f8600" : "#cf1322",
                  }}
                  prefix={
                    prediction[8] > 5 * prediction[7] ? (
                      <ArrowUpOutlined />
                    ) : (
                      <ArrowDownOutlined />
                    )
                  }
                />
              </Card>
            </Col>
          </Row>
        </div>
      </Modal>
    </div>
  );
}

IndexPage.propTypes = {};

export default connect(({ map, loading }) => ({
  map,
  loading: loading.global,
}))(IndexPage);
