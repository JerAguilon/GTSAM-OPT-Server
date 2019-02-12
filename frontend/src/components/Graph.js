import React, { Component } from "react";
import { Sigma, RandomizeNodePositions, RelativeSize } from "react-sigma";

class UpdateNodeProps extends React.Component {
  componentWillReceiveProps({ sigma, nodes }) {
    sigma.graph.nodes().forEach(n => {
      console.log("FINDING " + n.id);
      var updated = nodes.find(e => e.id == n.id)
      console.log("UPDATED!");
      console.log(updated);
      Object.assign(n, updated)
    });
    sigma.refresh()
  }

  render = () => null
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
        console.log("PROPERTIES: ");
        console.log(this.props);
        let landmarks = this.props.landmarks.slice();
        let poses = this.props.poses.slice();
        let graph = {
            nodes: poses.concat(landmarks)
        };
        return (<>
            <Sigma
                graph={GLOBAL_GRAPH}
                settings={{ drawEdges: false, clone: false, minNodeSize: 10 }}
            >
                <RelativeSize initialSize={10} />
                <UpdateNodeProps nodes={graph.nodes} />
            </Sigma>
        </>);
    }
}
export default Graph;