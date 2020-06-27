import axios from "axios";

const API_ROOT = process.env.REACT_APP_API_ROOT;

export const LOAD_LANGUAGES = "LOAD_LANGUAGES";

export const loadLanguages = (languages) => ({
  type: LOAD_LANGUAGES,
  languages,
});

export const fetchLanguages = () => {
  return (dispatch) => {
    axios.get(`${API_ROOT}/snippets/languages/`).then((response) => {
      dispatch(loadLanguages(response.data));
    });
  };
};
