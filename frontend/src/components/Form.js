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
            num_poses: 2,
            num_landmarks: 0,
        };
    }

    render() {
        return (
          <Form
            onSubmit={onSubmit}
            render={({ handleSubmit, pristine, invalid }) => (
              <form onSubmit={handleSubmit}>
                <h2>Arguments</h2>
                {this.getPoses()}


                <button type="submit" disabled={pristine || invalid}>
                  Submit
                </button>
              </form>
            )}
          />
        );
    }

    getPoses() {
        let numPoses = this.state.num_poses;
        let output = []
        for (let i = 0; i < numPoses; i++) {
            let varId = i + 1;
            let name = 'x' + varId.toString();
            let new_component = (
                <div>
                  <label>{name}</label>
                  <Field name={name + "_x"} component="input" placeholder="x" />
                  <Field name={name + "_y"} component="input" placeholder="y" />
                  <Field name={name + "_theta"} component="input" placeholder="theta" />
                </div>

            );
            output.push(new_component);
        };
        return output;

    }

}

export default SlamForm;
