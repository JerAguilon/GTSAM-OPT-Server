import React, { Component } from "react";
import { Sigma, RandomizeNodePositions, RelativeSize } from "react-sigma";

let MY_GRAPH = {
    nodes: [
        { id: "x1", x: -0.25, y: 0.2 },
        { id: "x2", x: 2.3, y: 0.1 },
        { id: "x3", x: 4.1, y: 0.1 },
        { id: "l4", x: 1.8, y: 2.1, theta: undefined },
        { id: "l5", x: 4.1, y: 1.8, theta: undefined }
    ]
    // edges: [{ id: "e1", source: "n1", target: "n2", label: "SEES" }]
};

class Graph extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        // let nodeColor = "#000080";
        // if (this.props.isResult) {
        //     nodeColor = "#7FFF00";
        // }

        let landmarks = this.props.landmarks.slice();
        let poses = this.props.poses.slice();
        let MY_GRAPH = {
            nodes: landmarks.concat(poses)
        };

        // myGraph = {
        //     nodes: [
        //         { id: "y1", x: -0.25, y: 0.2 },
        //         { id: "y2", x: 2.3, y: 0.1 },
        //         { id: "x3", x: 4.1, y: 0.1 },
        //         { id: "l4", x: 1.8, y: 2.1, theta: undefined },
        //         { id: "l5", x: 4.1, y: 1.8, theta: undefined }
        //     ]
        //     // edges: [{ id: "e1", source: "n1", target: "n2", label: "SEES" }]
        // };

        console.log("GRAPH IS");
        console.log(MY_GRAPH);

        return (
            <Sigma
                renderer="svg"
                graph={MY_GRAPH}
                settings={{ drawEdges: false, clone: false }}
            >
                <RelativeSize initialSize={10} />

                {/* <RandomizeNodePositions /> */}
            </Sigma>
        );
    }
}
export default Graph;
