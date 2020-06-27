import {
  Redirect,
  Route,
  BrowserRouter as Router,
  Switch,
} from "react-router-dom";
import AboutPage from "./pages/AboutPage";
import HomePage from "./pages/HomePage";
import Navbar from "./components/Navbar";
import React from "react";
import TermsPage from "./pages/TermsPage";
import SnippetPage from "./pages/SnippetPage";

function App() {
  return (
    <Router>
      <Navbar />
      <Switch>
        <Route component={HomePage} exact path="/" />
        <Route component={AboutPage} exact path="/about" />
        <Route component={TermsPage} exact path="/terms" />
        <Route component={SnippetPage} exact path="/:snippetKey" />

        <Redirect to="/" />
      </Switch>
    </Router>
  );
}

export default App;
