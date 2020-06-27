import React from "react";
import SnippetEditor from "../components/SnippetEditor";

const HomePage = () => {
  return (
    <>
      <h1>Welcome to the Home Page!</h1>

      <p>Create your first Snippet below:</p>
      <SnippetEditor />
    </>
  );
};

export default HomePage;
