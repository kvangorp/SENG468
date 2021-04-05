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

export default class SetSellTriggerModal extends Component {
  
  constructor(props) {
    super(props);
    this.state = {
        userId: '',
        stockSymbol: '',
        dollarAmount: '',
    };
  }

  handleChange = (e) => {
    let { name, value } = e.target;
    const state = { ...this.state, [name]: value };
    this.setState(state);
  };

  triggerSetSellTrigger = () => {
    this.handleSetSellTrigger()
    this.props.toggle()
  }

  handleSetSellTrigger = () => {
    
    let userId = this.state.userId;
    let stockSymbol = this.state.stockSymbol;
    let amount = this.state.dollarAmount

    var request = {
      'userId': userId,
      'stockSymbol': stockSymbol,
      'amount': amount,
      'transactionNum':1,
    }
    axios.post('http://localhost:8080/api/commands/set_sell_trigger/', request)
    .then((response) => {
      console.log(response);
      commandLogger(userId,amount,"SET_SELL_TRIGGER");
    })
    .catch((error) => {
      errorLogger(userId,"SET_SELL_TRIGGER");
    }) 
  }

  render() {
    const { toggle} = this.props;

    return (
      <Modal isOpen={true} toggle={toggle}>
        <ModalHeader toggle={toggle}>Set Sell Trigger</ModalHeader>
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
            <FormGroup>
              <Label for="dollarAmount">Dollar Amount</Label>
              <Input
                type="text"
                id="dollarAmount"
                name="dollarAmount"
                value={this.state.dollarAmount}
                onChange={this.handleChange}
                placeholder="Enter dollar amount of stock"
              />
            </FormGroup>
          </Form>
        </ModalBody>
        <ModalFooter>
          <Button
            color="success"
            onClick={this.triggerSetSellTrigger}
          >
            Set Sell Trigger
          </Button>
        </ModalFooter>
      </Modal>
    );
  }
}