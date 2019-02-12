import React, { Component } from "react";
import { Sigma, RandomizeNodePositions, RelativeSize } from "react-sigma";

class SampleGraph extends Component {
    constructor(props) {
        super(props);
    }
    // this.props.landmarks
    // this.props.poses

    render() {
        let myGraph = {
            nodes: [
                { id: "x1", x: -0.25, y: 0.2 },
                { id: "x2", x: 2.3, y: 0.1 },
                { id: "x3", x: 4.1, y: 0.1 },
                { id: "l4", x: 1.8, y: 2.1, theta: undefined },
                { id: "l5", x: 4.1, y: 1.8, theta: undefined }
            ]
            // edges: [{ id: "e1", source: "n1", target: "n2", label: "SEES" }]
        };
        console.log("sample graphi s");
        console.log(myGraph);

        return (
            <Sigma
                graph={myGraph}
                settings={{ drawEdges: false, clone: false }}
            >
                <RelativeSize initialSize={10} />

                {/* <RandomizeNodePositions /> */}
            </Sigma>
        );
    }
}
export default SampleGraph;
