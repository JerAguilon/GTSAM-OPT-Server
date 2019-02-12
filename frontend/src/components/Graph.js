import React, { Component } from "react";
import { Sigma, RandomizeNodePositions, RelativeSize } from "react-sigma";

class UpdateNodeProps extends React.Component {
    componentWillReceiveProps({ sigma, nodes }) {
        for (let i = 0; i < nodes.length; i++) {
            let graphNodes = sigma.graph.nodes();
            let found = false;
            for (let j = 0; j < graphNodes.length; j++) {
                if (graphNodes[j].id == nodes[i].id) {
                    Object.assign(graphNodes[j], nodes[i]);
                    found = true;
                    break;
                }
            }
            if (!found) {
                console.log("FOO");
                console.log(nodes[i]);
                sigma.graph.addNode(nodes[i]);
            }
        }
        // sigma.graph.nodes().forEach(n => {
        //   var updated = nodes.find(e => e.id == n.id)
        //   Object.assign(n, updated)
        // });
        sigma.refresh();
    }
    render = () => null;
}

class MyCustomSigma extends React.Component {
    constructor(props) {
        super(props);
        props.sigma.graph.addNode({ id: "n3", label: props.label });
    }
}

let GLOBAL_GRAPH = {
    nodes: [
        { id: "x1", x: -0.25, y: 0.2 },
        { id: "x2", x: 2.3, y: 0.1 },
        { id: "x3", x: 4.1, y: 0.1 },
        { id: "l4", x: 1.8, y: 2.1, theta: undefined },
        { id: "l5", x: 4.1, y: 1.8, theta: undefined }
    ]
};

class Graph extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        let landmarks = this.props.landmarks.slice();
        let poses = this.props.poses.slice();
        let graph = {
            nodes: poses.concat(landmarks)
        };

        graph.nodes.forEach(node => {
            node.label = node.id;
            let nodeType = node.id;
            if (nodeType && nodeType.charAt(0) == "x") {
                node.color = this.props.isResult ? "#7FFF00" : "#8B0000";
            }
        });

        console.log("graph shows");
        console.log(graph);

        return (
            <Sigma
                graph={GLOBAL_GRAPH}
                renderer="svg"
                settings={{
                    clone: false,
                    minNodeSize: 10,
                    defaultNodeColor: "#003366",
                    sideMargin: 1
                }}
            >
                <RelativeSize initialSize={10} />
                <UpdateNodeProps nodes={graph.nodes} />
            </Sigma>
        );
    }
}
export default Graph;
