import React, { Component } from 'react';

import { render } from 'react-dom';
import { Form, Field } from 'react-final-form';


const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));

const onSubmit = async values => {
    await sleep(300);
    window.alert(JSON.stringify(values, 0, 2));
}

class SlamForm extends Component {
    constructor(props) {
        super(props);
        this.state = {
            numPoses: 3,
            numLandmarks: 2,
            numBetweenFactors: 2,
            numMeasurementFactors: 3,
        };
        this.addPose = this.addPose.bind(this);
        this.addLandmark = this.addLandmark.bind(this);
    }

    render() {
        return (
          <Form
            onSubmit={onSubmit}
            render={({ handleSubmit, pristine, invalid }) => (
              <form onSubmit={handleSubmit}>
                <h2>Arguments</h2>
                <h4>Noise</h4>
                <div>
                  <label>Prior Noise</label>
                  <Field name={"priorNoiseX"} component="input" placeholder="x" />
                  <Field name={"priorNoiseY"} component="input" placeholder="y" />
                  <Field name={"priorNoiseTheta"} component="input" placeholder="theta" />
                </div>
                <div>
                  <label>Odometry Noise</label>
                  <Field name={"odometryNoiseX"} component="input" placeholder="x" />
                  <Field name={"odometryNoiseY"} component="input" placeholder="y" />
                  <Field name={"odometryNoiseTheta"} component="input" placeholder="theta" />
                </div>
                <div>
                  <label>Measurement Noise</label>
                  <Field name={"measurementNoiseBearing"} component="input" placeholder="bearing" />
                  <Field name={"measurementNoiseRange"} component="input" placeholder="range" />
                </div>


                <h4>Variables and Initial Estimates</h4>
                {this.getPoses()}
                {this.getLandmarks()}
                <button type="button" onClick={this.addPose}>Add Pose</button>
                <button type="button" onClick={this.addLandmark}>Add Landmark</button>

                <h4>X1 Prior Estimate</h4>
                <div>
                  <label>Prior</label>
                  <Field name={"priorX"} component="input" placeholder="x" />
                  <Field name={"priorY"} component="input" placeholder="y" />
                  <Field name={"priorTheta"} component="input" placeholder="theta" />
                </div>

                <h4>Between Factors</h4>
                {this.getBetweenFactors()}

                <h4>Measurement Factors</h4>
                {this.getMeasurementFactors()}

                <button type="submit" disabled={pristine || invalid}>
                  Submit
                </button>
              </form>
            )}
          />
        );
    }

    addPose() {
        this.setState(
            { numPoses: this.state.numPoses + 1 }
        );
    }

    addLandmark() {
        this.setState(
            { numLandmarks: this.state.numLandmarks + 1 }
        );
    }

    getBetweenFactors() {
        let numBetweenFactors = this.state.numBetweenFactors;
        let output = []
        for (let i = 0; i < numBetweenFactors; i++) {
            let varId = i + 1;
            let name = 'betweeen' + varId.toString();
            let new_component = (
                <div>
                  <label>{name}</label>
                  <Field name={name + "X"} component="input" placeholder="x" />
                  <Field name={name + "Y"} component="input" placeholder="y" />
                  <Field name={name + "Theta"} component="input" placeholder="theta" />
                </div>

            );
            output.push(new_component);
        };
        return output;
    }

    getMeasurementFactors() {
        let numMeasurementFactors = this.state.numMeasurementFactors;
        let output = []
        for (let i = 0; i < numMeasurementFactors; i++) {
            let varId = i + 1;
            let name = 'measurement' + varId.toString();
            let new_component = (
                <div>
                  <label>{name}</label>
                  <Field name={name + "Bearing"} component="input" placeholder="bearing" />
                  <Field name={name + "Range"} component="input" placeholder="range" />
                </div>

            );
            output.push(new_component);
        };
        return output;
    }

    getPoses() {
        let numPoses = this.state.numPoses;
        let output = []
        for (let i = 0; i < numPoses; i++) {
            let varId = i + 1;
            let name = 'x' + varId.toString();
            let new_component = (
                <div>
                  <label>{name}</label>
                  <Field name={name + "X"} component="input" placeholder="x" />
                  <Field name={name + "Y"} component="input" placeholder="y" />
                  <Field name={name + "Theta"} component="input" placeholder="theta" />
                </div>

            );
            output.push(new_component);
        };
        return output;
    }

    getLandmarks() {
        let numLandmarks = this.state.numLandmarks;
        let output = []
        for (let i = 0; i < numLandmarks; i++) {
            let varId = i + 1;
            let name = 'l' + varId.toString();
            let new_component = (
                <div>
                  <label>{name}</label>
                  <Field name={name + "_x"} component="input" placeholder="x" />
                  <Field name={name + "_y"} component="input" placeholder="y" />
                </div>

            );
            output.push(new_component);
        };
        return output;
    }

}

export default SlamForm;
