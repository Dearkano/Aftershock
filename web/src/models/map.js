export default {
  namespace: "map",

  state: {
    data: {},
  },

  subscriptions: {
    setup({ dispatch, history }) {
      // eslint-disable-line
    },
  },

  effects: {
    *fetch({ payload }, { call, put }) {
      // eslint-disable-line
      yield put({ type: "save" });
    },
    *getData({ payload }, { put }) {
      const res = yield fetch(
        `https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/${payload}.geojson`
      );
      const data = yield res.json();
      yield put({ type: "save", payload: data });
    },
  },

  reducers: {
    save(state, action) {
      return { ...state, data: action.payload };
    },
  },
};
