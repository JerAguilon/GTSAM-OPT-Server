import React, { Component } from 'react';

import { render } from 'react-dom';
import { Form, Field } from 'react-final-form';


const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));

const onSubmit = async values => {
    await sleep(300);
    window.alert(JSON.stringify(values, 0, 2));
}

const INITIAL_VALUES =  {
    'priors': [
        {
            'key': 'x1',
        }
    ]
}



class SlamForm extends Component {
    async onValidate(values) {
        this.props.formUpdateCallback(values);
    }

    constructor(props) {
        super(props);
        this.state = {
            numPoses: 3,
            numLandmarks: 2,
            numBetweenFactors: 2,
            numMeasurementFactors: 3,
        };
        this.addCount = this.addCount.bind(this);
        this.onValidate = this.onValidate.bind(this);
    }

    render() {
        return (
          <Form
            initialValues={INITIAL_VALUES}
            onSubmit={onSubmit}
            validate={this.onValidate}
            render={({ handleSubmit, pristine, invalid }) => (
              <form onSubmit={handleSubmit}>
                <h2>Arguments</h2>
                <h4>Noise</h4>
                <div>
                  <label>Prior Noise</label>
                  <Field name={"priorNoise[0]"} component="input" placeholder="x" />
                  <Field name={"priorNoise[1]"} component="input" placeholder="y" />
                  <Field name={"priorNoise[2]"} component="input" placeholder="theta" />
                </div>
                <div>
                  <label>Odometry Noise</label>
                  <Field name={"odometryNoise[0]"} component="input" placeholder="x" />
                  <Field name={"odometryNoise[1]"} component="input" placeholder="y" />
                  <Field name={"odometryNoise[2]"} component="input" placeholder="theta" />
                </div>
                <div>
                  <label>Measurement Noise</label>
                  <Field name={"measurementNoise[0]"} component="input" placeholder="bearing" />
                  <Field name={"measurementNoise[1]"} component="input" placeholder="range" />
                </div>


                <h4>Variables and Initial Estimates</h4>
                {this.getPoses()}
                {this.getLandmarks()}
                <button type="button" onClick={(e) => this.addCount('numPoses')}>Add Pose</button>
                <button type="button" onClick={(e) => this.addCount('numLandmarks')}>Add Landmark</button>


                <h4>X1 Prior Estimate</h4>
                <div>
                  <label>Prior</label>
                  <Field name={"priors[0].prior[0]"} component="input" placeholder="x" />
                  <Field name={"priors[0].prior[1]"} component="input" placeholder="y" />
                  <Field name={"priors[0].prior[2]"} component="input" placeholder="theta" />
                </div>

                <h4>Between Factors</h4>
                {this.getBetweenFactors()}
                <button type="button" onClick={(e) => this.addCount('numBetweenFactors')}>Add Between Factor</button>

                <h4>Measurement Factors</h4>
                {this.getMeasurementFactors()}
                <button type="button" onClick={(e) => this.addCount('numMeasurementFactors')}>Add Measurement Factor</button>

                <div>
                    <button type="submit" disabled={pristine || invalid}>
                      Submit
                    </button>
                </div>
              </form>
            )}
          />
        );
    }

    addCount(key) {
        this.setState(
            { [key]: this.state[key] + 1 }
        );
        this.forceUpdate()
    }

    getBetweenFactors() {
        let numBetweenFactors = this.state.numBetweenFactors;
        let output = []
        for (let i = 0; i < numBetweenFactors; i++) {
            let varId = i + 1;
            let name = 'betweeenPoseFactors[' + varId.toString() + ']';
            let new_component = (
                <div key={i.toString()}>
                  <Field name={name + ".connections[0]"} component="input" placeholder="var1" />
                  <Field name={name + ".connections[1]"} component="input" placeholder="var2" />
                  <Field name={name + ".pose[0]"} component="input" placeholder="x" />
                  <Field name={name + ".pose[1]"} component="input" placeholder="y" />
                  <Field name={name + ".pose[2]"} component="input" placeholder="theta" />
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
            let name = 'bearingRangeFactors.[' + varId.toString() + ']';
            let new_component = (
                <div key={i.toString()}>
                  <Field name={name + ".connections[0]"} component="input" placeholder="var1" />
                  <Field name={name + ".connections[1]"} component="input" placeholder="var2" />
                  <Field
                    name={name + ".bearing"}
                    component="input"
                    placeholder="bearing"
                    allowNull="false"
                  />
                  <Field name={name + "range"} component="input" placeholder="range" />
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
            let name = 'symbols[' + varId.toString() + ']';
            let new_component = (
                <div key={i.toString()}>
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
                <div key={i.toString()}>
                  <label>{name}</label>
                  <Field name={name + "X"} component="input" placeholder="x" />
                  <Field name={name + "Y"} component="input" placeholder="y" />
                </div>

            );
            output.push(new_component);
        };
        return output;
    }

}

export default SlamForm;
