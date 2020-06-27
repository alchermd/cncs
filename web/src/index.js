import React from "react";
import { render } from "react-dom";
import thunk from "redux-thunk";
import { createStore, applyMiddleware } from "redux";
import { Provider } from "react-redux";
import { composeWithDevTools } from "redux-devtools-extension";

import App from "./App";
import rootReducer from "./reducers";

const store = createStore(
  rootReducer,
  composeWithDevTools(applyMiddleware(thunk))
);

render(
  <React.StrictMode>
    <Provider store={store}>
      <App />
    </Provider>
  </React.StrictMode>,
  document.getElementById("root")
);
