import React, { Component } from "react";


const s = window.s

class Graph extends Component {
    componentWillReceiveProps(props) {
        let nodes = props.landmarks;
        nodes = nodes.concat(props.poses);
        for (let i = 0; i < nodes.length; i++) {
            let nodeType = nodes[i].id
            if (nodeType.charAt(0) === 'x') {
                nodes[i].color = props.isResult ? "#7FFF00" : "#8B0000";
            }


            if (typeof nodes[i].x === 'undefined') {
                nodes[i].x = 0;
            }
            if (typeof nodes[i].y === 'undefined') {
                nodes[i].y = 0;
            }
            nodes[i].x = parseFloat(nodes[i].x).toFixed(2);
            nodes[i].y = parseFloat(nodes[i].y).toFixed(2);

            let label = nodes[i].id;
            let coords = {
                x: nodes[i].x,
                y: nodes[i].y,
            }
            if (nodes[i].hasOwnProperty('theta')) {
                nodes[i].theta = parseFloat(nodes[i].theta).toFixed(2);
                coords.theta = nodes[i].theta;
            }
            nodes[i].label = nodes[i].id + "  " + JSON.stringify(coords);

            let graphNodes = s.graph.nodes()
            let found = false
            for (let j = 0; j < graphNodes.length; j++) {
                if (graphNodes[j].id === nodes[i].id) {
                    graphNodes[j].x = nodes[i].x;
                    graphNodes[j].y = nodes[i].y;
                    graphNodes[j].color = nodes[i].color;
                    graphNodes[j].label = nodes[i].label;
                    found = true;
                    break;
                }
            }
            if (!found) {
                s.graph.addNode({ ...nodes[i], size: 500 });
            }

        }

        s.refresh();
        let edges = props.edges;
        for (let i = 0; i < edges.length; i++) {
            let edge = edges[i]
            let source = edge.source;
            let target = edge.target;
            let foundSource = false;
            let foundTarget = false;
            let graphNodes = s.graph.nodes();

            for (let j = 0; j < graphNodes.length; j++) {
                if (graphNodes[j].id === source) {
                    foundSource = true;
                }
                if (graphNodes[j].id === target) {
                    foundTarget = true;
                }
            }

            if (!(foundSource && foundTarget)) {
                continue;
            }

            let graphEdges = s.graph.edges();
            let found = false
            for (let j = 0; j < graphEdges.length; j++) {
                let graphEdge = graphEdges[j];
                if (graphEdge.id === edge.id) {
                    found = true;
                    s.graph.dropEdge(graphEdge.id);
                    s.graph.addEdge(edge);
                    break;
                }
            }

            if (!found) {
                console.log("ADDING");
                console.log(edges[i]);
                s.graph.addEdge(edges[i]);
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
