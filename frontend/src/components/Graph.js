import React, { Component } from "react";


const s = window.s

class Graph extends Component {
    componentWillReceiveProps(props) {
        let nodes = this.props.landmarks;
        nodes = nodes.concat(this.props.poses);
        for (let i = 0; i < nodes.length; i++) {
            let nodeType = nodes[i].id
            if (nodeType.charAt(0) === 'x') {
                nodes[i].color = this.props.isResult ? "#7FFF00" : "#8B0000";
            }

            nodes[i].label = nodes[i]
            nodes[i].coor = this.props.isResult

            if (typeof nodes[i].x === 'undefined') {
                nodes[i].x = 0;
            }
            if (typeof nodes[i].y === 'undefined') {
                nodes[i].y = 0;
            }
            nodes[i].x = parseFloat(nodes[i].x);
            nodes[i].y = parseFloat(nodes[i].y);

            let graphNodes = s.graph.nodes()
            let found = false
            for (let j = 0; j < graphNodes.length; j++) {
                if (graphNodes[j].id === nodes[i].id) {
                    graphNodes[j].x = nodes[i].x
                    graphNodes[j].y = nodes[i].y
                    // Object.assign(graphNodes[j], nodes[i])
                    s.refresh();
                    found = true;
                    break;
                }
            }
            if (!found) {
                s.graph.addNode({ ...nodes[i], size: 500 });
                s.refresh();
            }
        }
        s.refresh();

    }

    render() {
        return (<div>
        </div>)

    }
}
export default Graph;
