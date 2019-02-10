import React, { Component } from 'react';
import logo from './logo.svg';

import SlamForm from './components/Form'

import './App.css';

const FORM_KEYS = {

}


class App extends Component {
  constructor(props) {
    super(props);
    this.handleFormCallback = this.handleFormCallback.bind(this);
  }

  render() {
    return (
      <div className="App">
        <header className="App-header">
          <a
            className="App-link"
            href="https://reactjs.org"
            target="_blank"
            rel="noopener noreferrer"
          >
            Learn React
          </a>
          <SlamForm
            formUpdateCallback={this.handleFormCallback}
          />
        </header>
      </div>
    );
  }

  handleFormCallback(values) {
    console.log(values);
  }
}

export default App;
