import React from "react";
import { Router, Route, Switch } from "dva/router";
import IndexPage from "./routes/Index";
import Header from "./components/Header";

function RouterConfig({ history }) {
  return (
    <React.Fragment>
      <Header />
      <Router history={history}>
        <Switch>
          <Route path="/" exact component={IndexPage} />
        </Switch>
      </Router>
    </React.Fragment>
  );
}

export default RouterConfig;
