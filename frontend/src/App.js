import React, { Component } from "react";
import logo from "./logo.svg";

import SlamForm from "./components/Form";
import Graph from "./components/Graph";

import "./css/App.css";

const DEFAULT_STATE = {
    isResult: false,
    landmarks: [
        { id: "x1", x: -0.25, y: 0.2 },
        { id: "x2", x: 2.3, y: 0.1 },
        { id: "x3", x: 4.1, y: 0.1 }
    ],
    poses: [{ id: "l4", x: 1.8, y: 2.1 }, { id: "l5", x: 4.1, y: 1.8 }]
};

class App extends Component {
    constructor(props) {
        super(props);
        this.handleFormUpdateCallback = this.handleFormUpdateCallback.bind(
            this
        );
        this.handleFormSubmitCallback = this.handleFormSubmitCallback.bind(
            this
        );
        this.state = DEFAULT_STATE;
    }

    render() {
        return (
            <div className="App">
                <header className="App-header">
                    <Graph
                        landmarks={this.state.landmarks}
                        poses={this.state.poses}
                        edges={this.state.edges}
                        isResult={this.state.isResult}
                    />
                    <SlamForm
                        formUpdateCallback={this.handleFormUpdateCallback}
                        formSubmitCallback={this.handleFormSubmitCallback}
                    />
                </header>
            </div>
        );
    }

    handleFormSubmitCallback(response) {
        let landmarks = [];
        let poses = [];
        Object.keys(response.result).forEach(function(key) {
            if (response.result[key].length === 2) {
                landmarks.push({
                    id: key,
                    x: response.result[key][0],
                    y: -response.result[key][1]
                });
            } else {
                poses.push({
                    id: key,
                    x: response.result[key][0],
                    y: -response.result[key][1],
                    theta: response.result[key][2]
                });
            }
        });
        this.setState({
            isResult: true,
            landmarks: landmarks,
            poses: poses
        });
        this.forceUpdate();
    }

    handleFormUpdateCallback(values) {
        let landmarks = [];
        let poses = [];
        let edges = [];
        values.symbols.forEach(function(value) {
            if (value.type === "pose") {
                poses.push({
                    id: value.key,
                    x: value.estimate[0],
                    y: -value.estimate[1],
                    theta: value.estimate[2]
                });
            } else {
                landmarks.push({
                    id: value.key,
                    x: value.estimate[0],
                    y: -value.estimate[1],
                });
            }
        });

        let index = 0;
        values.betweenPoseFactors.forEach(function(value) {
            let source = value.connections[0];
            let target = value.connections[1];
            let eid = "e" + index.toString();
            edges.push({source: source, target: target, id: eid});
            index += 1;
        });

        values.bearingRangeFactors.forEach(function(value) {
            let source = value.connections[0];
            let target = value.connections[1];
            let eid = "e" + index.toString();
            edges.push({source: source, target: target, id: eid});
            index += 1;
        });

        this.setState({
            isResult: false,
            landmarks: landmarks,
            poses: poses,
            edges: edges,
        });
        this.forceUpdate();
    }
}

export default App;
