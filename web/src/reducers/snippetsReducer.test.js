import snippetsReducer from "./snippetsReducer";
import { loadLanguages } from "../actions/snippetsActions";

it("loads a set of language", () => {
  const state = { languages: [] };
  const languages = [
    ["scheme", "Scheme"],
    ["python", "Python 2.x"],
    ["c++", "C++"],
  ];

  expect(snippetsReducer(state, loadLanguages(languages))).toEqual({
    languages,
  });
});
