import { LOAD_LANGUAGES } from "../actions/snippetsActions";

const initialState = {
  languages: [],
};

const snippetsReducer = (state = initialState, action) => {
  switch (action.type) {
    case LOAD_LANGUAGES:
      return {
        ...state,
        languages: [...action.languages],
      };
    default:
      return state;
  }
};

export default snippetsReducer;
