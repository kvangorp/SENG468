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
} from "reactstrap";


export default class CancelSetSellModal extends Component {
  constructor(props) {
    super(props);
    this.state = {
        userId: '',
        stockSymbol: '',
    };
  }

  // change state variables
  handleChange = (e) => {
    let { name, value } = e.target;
    const state = { ...this.state, [name]: value };
    this.setState(state);
  };

  // call handle function and close modal
  triggerCancelSetSell = () => {
    this.handleCancelSetSell()
    this.props.toggle()
  }

  // send HTTP request to transaction server and log transaction
  handleCancelSetSell = () => {
    
    let userId = this.state.userId;
    let stockSymbol = this.state.stockSymbol;

    var request = {
      'userId': userId,
      'stockSymbol': stockSymbol,
      'transactionNum':1,
    }
    axios.post('http://localhost:8080/api/commands/cancel_set_sell/', request)
    .then((response) => {
      console.log(response);
      commandLogger(userId,0.0,"CANCEL_SET_SELL");
    })
    .catch((error) => {
      errorLogger(userId,"CANCEL_SET_SELL");
    }) 
  }

  render() {
    const { toggle} = this.props;

    return (
      <Modal isOpen={true} toggle={toggle}>
        <ModalHeader toggle={toggle}>Cancel Set Sell</ModalHeader>
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
              <Label for="stockSymbol">Stock Symbol</Label>
              <Input
                type="text"
                id="stockSymbol"
                name="stockSymbol"
                value={this.state.stockSymbol}
                onChange={this.handleChange}
                placeholder="Enter Stock Symbol"
              />
            </FormGroup>
          </Form>
        </ModalBody>
        <ModalFooter>
          <Button
            color="success"
            onClick={this.triggerCancelSetSell}
          >
            Cancel Set Sell
          </Button>
        </ModalFooter>
      </Modal>
    );
  }
}