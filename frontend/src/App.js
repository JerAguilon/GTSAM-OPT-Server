import React, { Component } from 'react';
import logo from './logo.svg';

import SlamForm from './components/Form'

import './App.css';

const DEFAULT_STATE = {
    isResult:false,
    landmarks:[
        {name:"x1",x:-0.25,y:0.2},
        {name:"x2",x:2.3,y:0.1},
        {name:"x3",x:4.1,y:0.1}
    ],
    poses:[
        {name:"l4",x:1.8,y:2.1},
        {name:"l5",x:4.1,y:1.8}
    ]
}

class App extends Component {
  constructor(props) {
    super(props);
    this.handleFormUpdateCallback = this.handleFormUpdateCallback.bind(this);
    this.handleFormSubmitCallback = this.handleFormSubmitCallback.bind(this);
    this.state = DEFAULT_STATE;
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
      let landmarks = []
      let poses = []
      Object.keys(response.result).forEach(
          function(key) {
            if (response.result[key].length === 2) {
              landmarks.push(
                {
                  name: key,
                  x: response.result[key][0],
                  y: response.result[key][1],
                }
              );
            } else {
              poses.push(
                {
                  name: key,
                  x: response.result[key][0],
                  y: response.result[key][1],
                  theta: response.result[key][2],
                }
              );

            }
          }
      )
      this.setState({
        isResult: true,
        landmarks: landmarks,
        poses: poses,
      })
      console.log("STATE:");
      console.log(this.state);
  }

  handleFormUpdateCallback(values) {
      console.log("Updated");
      console.log(values);
      let landmarks = []
      let poses = []
      values.symbols.forEach(
          function(value) {
            if (value.type === 'pose') {
              landmarks.push(
                {
                  name: value.key,
                  x: value.estimate[0],
                  y: value.estimate[1],
                }
              );
            } else {
              poses.push(
                {
                  name: value.key,
                  x: value.estimate[0],
                  y: value.estimate[1],
                  theta: value.estimate[2],
                }
              );
            }
          }
      )
      console.log(landmarks);
      console.log(poses);
      this.setState({
        isResult: false,
        landmarks: landmarks,
        poses: poses,
      })
      console.log("STATE:");
      console.log(this.state);
  }
}

export default App;
