import { combineReducers } from "redux";
import appReducer from "./appReducer";
import snippetsReducer from "./snippetsReducer";

const rootReducer = combineReducers({
  app: appReducer,
  snippets: snippetsReducer,
});

export default rootReducer;
