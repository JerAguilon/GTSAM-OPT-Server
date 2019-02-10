import React, { Component } from 'react';
import logo from './logo.svg';

import SlamForm from './components/Form'

import './App.css';

const FORM_KEYS = {

}


class App extends Component {
  constructor(props) {
    super(props);
    this.handleFormUpdateCallback = this.handleFormUpdateCallback.bind(this);
    this.handleFormSubmitCallback = this.handleFormSubmitCallback.bind(this);
  }

  render() {
    return (
      <div className="App">
        <header className="App-header">
          <SlamForm
            formUpdateCallback={this.handleFormUpdateCallback}
            formSubmitCallback={this.handleFormSubmitCallback}
          />
        </header>
      </div>
    );
  }

  handleFormSubmitCallback(response) {
      console.log("SUBMITTED");
      console.log(response);
  }

  handleFormUpdateCallback(values) {
      console.log("Updated");
      console.log(values);
  }
}

export default App;
