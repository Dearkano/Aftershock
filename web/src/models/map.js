export default {
  namespace: "map",

  state: {
    data: {},
    prediction: [],
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
      const { mag, time } = payload;
      const res = yield fetch(
        `http://13.82.140.200:7001/query?mag=${mag}&range=${time}`
      );
      const data = yield res.json();
      yield put({ type: "save", payload: data });
    },
    *predict({ payload }, { put }) {
      const { data } = payload;
      const res = yield fetch(
        `http://13.82.140.200:7001/predict?mag=${data.mag || 0}&mmi=${
          data.mmi || 0
        }&sig=${data.sig || 0}&depth=${data.depth || 0}&n_foreshocks=${
          data.n_foreshocks || 0
        }`
      );
      const d = yield res.json();
      yield put({ type: "savePrediction", payload: d[0] });
    },
  },

  reducers: {
    save(state, action) {
      return { ...state, data: action.payload };
    },
    savePrediction(state, action) {
      return { ...state, prediction: action.payload };
    },
  },
};
