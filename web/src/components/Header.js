import React, { useState } from "react";
import { connect } from "dva";
import { routerRedux } from "dva/router";
import styles from "./index.less";
import logo from "../assets/logo.png";

function Header({ dispatch }) {
  return (
    <div className={styles.container}>
      <img
        onClick={() => dispatch(routerRedux.push("/"))}
        className={styles.logo}
        src={logo}
      />
      <div className={styles.row} style={{ marginRight: "6vw" }}>
        <div
          className={styles.text}
          //onClick={() => dispatch(routerRedux.push("/signup"))}
        >
          Sign up
        </div>
        <div
          className={styles.text}
          //onClick={() => dispatch(routerRedux.push("/partners"))}
        >
          Partners
        </div>
        <div
          className={styles.text}
          style={{ paddingRight: 0 }}
          //onClick={() => dispatch(routerRedux.push("/contact"))}
        >
          Contact us
        </div>
      </div>
    </div>
  );
}

export default connect()(Header);
