import React, { Component } from "react";
import {commandLogger, errorLogger} from '../transactionLogger.js'
import axios from "axios";
import {
  Button,
  Modal,
  ModalHeader,
  ModalBody,
  ModalFooter,
  Form,
  FormGroup,
  Input,
  Label,
  ListGroup,
  ListGroupItem,
  Collapse,
  Card,
  CardBody
} from "reactstrap";

// This creates a class for the modal created by clicking the Dumplog Button
export default class DumplogModal extends Component {
  constructor(props) {
    super(props);
    this.state = {
        userId: '',
        filename: ''
    };
  }

  // When user input is sent or buttons are clicked, this method updates modal state
  handleChange = (e) => {
    let { name, value } = e.target;
    const state = { ...this.state, [name]: value };
    this.setState(state);
  };

  // Open Dumplog modal
  triggerDumplog = () => {
    this.handleDumplog()
    this.props.toggle()
  }

  // Sends user input as a command to the Dumplog 
  // endpoint, and logs transaction in database
  handleDumplog = () => {
    let userId = this.state.userId;
    let filename = this.state.filename;

    var request = {
      'userId': userId,
      'filename': filename,
      'transactionNum':1,
    }
    axios.post('http://localhost:8080/api/commands/dumplog/', request)
    .then((response) => {
      console.log(response);
      this.handleResponse(response);
      commandLogger(userId,0.0,"DUMPLOG");
    })
    .catch((error) => {
      errorLogger(userId,"DUMPLOG");
    }) 
  }

  handleResponse = (response) => {
    console.log(response);
  }

  // Creates and associates buttons for the modal users to interact with
  render() {
    const { toggle } = this.props;

    return (
      <Modal isOpen={true} toggle={toggle}>
        <ModalHeader toggle={toggle}>Dumplog</ModalHeader>
        <ModalBody>
          <Form>
          <FormGroup>
              <Label for="userId">User ID</Label>
              <Input
                type="text"
                id="userId"
                name="userId"
                value={this.state.userId}
                onChange={this.handleChange}
                placeholder="Enter User ID"
              />
            </FormGroup>
            <FormGroup>
              <Label for="filename">Filename</Label>
              <Input
                type="text"
                id="filename"
                name="filename"
                value={this.state.filename}
                onChange={this.handleChange}
                placeholder="Enter Filename"
              />
            </FormGroup>
          </Form>
        </ModalBody>
        <ModalFooter>
          <Button
            color="success"
            onClick={this.triggerDumplog}
          >
            Dumplog
          </Button>
        </ModalFooter>
      </Modal>
    );
  }
}