import React from "react";
import { connect } from "react-redux";
import { fetchLanguages } from "../actions/snippetsActions";
import axios from "axios";
import { withRouter } from "react-router-dom";

const API_ROOT = process.env.REACT_APP_API_ROOT;

class SnippetEditor extends React.Component {
  state = {
    title: "",
    code: "",
    language: "text",
    has_line_numbers: false,
  };

  componentDidMount() {
    const { dispatch } = this.props;
    dispatch(fetchLanguages());
  }

  handleChange = (e) => {
    const { name } = e.target;
    const value =
      e.target.name === "has_line_numbers" ? e.target.checked : e.target.value;

    this.setState({ [name]: value });
  };

  handleSubmit = (e) => {
    e.preventDefault();
    const { history } = this.props;

    axios.post(`${API_ROOT}/snippets/`, this.state).then((response) => {
      history.push(`/${response.data.key}`);
    });
  };

  render() {
    const { languages } = this.props;
    const { title, code, language, has_line_numbers } = this.state;

    const languageOptions = languages.map((language, index) => (
      <option value={language[0]} key={index}>
        {language[1]}
      </option>
    ));

    return (
      <div>
        <form onSubmit={this.handleSubmit}>
          <div>
            <label htmlFor="title">Title</label>
            <input
              type="text"
              name="title"
              id="title"
              value={title}
              onChange={this.handleChange}
            />
          </div>

          <div>
            <label htmlFor="code">Code</label>
            <textarea
              name="code"
              id="code"
              value={code}
              onChange={this.handleChange}
              cols="30"
              rows="10"
            ></textarea>
          </div>

          <div>
            <label htmlFor="language">Language</label>
            <select
              name="language"
              id="language"
              value={language}
              onChange={this.handleChange}
            >
              {languageOptions}
            </select>
          </div>

          <div>
            <input
              type="checkbox"
              name="has_line_numbers"
              id="has_line_numbers"
              checked={has_line_numbers}
              onChange={this.handleChange}
            />
            <label htmlFor="has_line_numbers">Show Line Numbers?</label>
          </div>

          <div>
            <input type="submit" value="Save" />
          </div>
        </form>
      </div>
    );
  }
}

const mapStateToProps = (state) => ({
  languages: state.snippets.languages,
});

export default withRouter(connect(mapStateToProps)(SnippetEditor));
