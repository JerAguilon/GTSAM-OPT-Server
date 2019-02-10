import React, { Component } from 'react';

import { render } from 'react-dom';
import { Form, Field } from 'react-final-form';


const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));


const INITIAL_VALUES =  {
   "priorNoise":[
      0.3,
      0.3,
      0.1
   ],
   "odometryNoise":[
      0.2,
      0.2,
      0.1
   ],
   "measurementNoise":[
      0.1,
      0.2
   ],
   "symbols":[
      {
         "estimate":[
            -0.25,
            0.2,
            0.15
         ],
      },
      {
         "estimate":[
            2.3,
            0.1,
            -0.2
         ],
      },
      {
         "estimate":[
            4.1,
            0.1,
            0.1
         ],
      },
      {
         "estimate":[
            1.8,
            2.1
         ],
      },
      {
         "estimate":[
            4.1,
            1.8
         ],
      }
   ],
   "priors":[
      {
         "key":"x1",
         "prior":[
            0,
            0,
            0
         ]
      }
   ],
   "betweenPoseFactors":[
      {
         "connections":[
            "x1",
            "x2"
         ],
         "pose":[
            2,
            0,
            0
         ]
      },
      {
         "connections":[
            "x2",
            "x3"
         ],
         "pose":[
            2,
            0,
            0
         ]
      }
   ],
   "bearingRangeFactors":[
      {
         "connections":[
            "x1",
            "l4"
         ],
         "bearing":45,
         "range":2.8284
      },
      {
         "connections":[
            "x2",
            "l4"
         ],
         "bearing":90,
         "range":2
      },
      {
         "connections":[
            "x3",
            "l5"
         ],
         "bearing":90,
         "range":2
      }
   ]
};



class SlamForm extends Component {
    async onValidate(values) {
        this.props.formUpdateCallback(values);
        return [];
    }
    onSubmit(values) {
        for (let i = 0; i < values.symbols.length; i++) {
            let key = "";
            let type = "";
            if (values.symbols[i].estimate.length === 3) {
                key = "x" + (i + 1).toString();
                type = "pose";
            } else {
                key = "l" + (i + 1).toString();
                type = "point";
            }
            values.symbols[i].key = key
            values.symbols[i].type = type
        }
        console.log("SUBMITTING");
        console.log(values);

        let request = new XMLHttpRequest();
        request.open('POST', 'http://localhost:5000', true);
        request.setRequestHeader('Content-Type', 'application/json');
        request.responseType = 'json'
        let this_props = this.props
        request.onload = function(e) {
            if (request.status < 400) {
                this_props.formSubmitCallback(this.response);
            } else {
                alert(request.status.toString() + " error: " + JSON.stringify(this.response));
            }
        }
        request.send(JSON.stringify(values));
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
        this.onSubmit = this.onSubmit.bind(this);
    }

    render() {
        let poses = this.getPoses();
        let landmarks = this.getLandmarks(poses.length);
        return (
          <Form
            initialValues={INITIAL_VALUES}
            onSubmit={this.onSubmit}
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
                {poses}
                {landmarks}
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
                    <button type="submit" disabled={invalid}>
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
            let varId = i;
            let name = 'betweenPoseFactors[' + varId.toString() + ']';
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
            let varId = i;
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
            let varId = i;
            let name = 'symbols[' + varId.toString() + ']';
            let new_component = (
                <div key={i.toString()}>
                  <label>x{i + 1}</label>
                  <Field name={name + ".estimate[0]"} component="input" placeholder="x" />
                  <Field name={name + ".estimate[1]"} component="input" placeholder="y" />
                  <Field name={name + ".estimate[2]"} component="input" placeholder="theta" />
                </div>

            );
            output.push(new_component);
        };
        return output;
    }

    getLandmarks(initialI) {
        let numLandmarks = this.state.numLandmarks;
        let output = []
        for (let i = initialI; i < initialI + numLandmarks; i++) {
            let varId = i;
            let name = 'symbols[' + varId.toString() + ']';
            let new_component = (
                <div key={i.toString()}>
                  <label>l{i+1}</label>
                  <Field name={name + ".estimate[0]"} component="input" placeholder="x" />
                  <Field name={name + ".estimate[1]"} component="input" placeholder="y" />
                </div>

            );
            output.push(new_component);
        };
        return output;
    }

}

export default SlamForm;
