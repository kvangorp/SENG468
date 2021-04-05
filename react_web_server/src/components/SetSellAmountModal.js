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

export default class SetSellAmountModal extends Component {
  
  constructor(props) {
    super(props);
    this.state = {
        userId: '',
        stockSymbol: '',
        stockAmount: '',
    };
  }

  // change state variables
  handleChange = (e) => {
    let { name, value } = e.target;
    const state = { ...this.state, [name]: value };
    this.setState(state);
  };

  // call handle function and close modal
  triggerSetSellAmount = () => {
    this.handleSetSellAmount()
    this.props.toggle()
  }

  // send HTTP request to transaction server and log transaction
  handleSetSellAmount = () => {
    
    let userId = this.state.userId;
    let stockSymbol = this.state.stockSymbol;
    let amount = this.state.stockAmount

    var request = {
      'userId': userId,
      'stockSymbol': stockSymbol,
      'amount': amount,
      'transactionNum':1,
    }
    axios.post('http://localhost:8080/api/commands/set_sell_amount/', request)
    .then((response) => {
      console.log(response);
      commandLogger(userId,amount,"SET_SELL_AMOUNT");
    })
    .catch((error) => {
      errorLogger(userId,"SET_SELL_AMOUNT");
    }) 
  }

  render() {
    const { toggle} = this.props;

    return (
      <Modal isOpen={true} toggle={toggle}>
        <ModalHeader toggle={toggle}>Set Sell Amount</ModalHeader>
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
              <Label for="stockAmount">Stock Amount</Label>
              <Input
                type="text"
                id="stockAmount"
                name="stockAmount"
                value={this.state.stockAmount}
                onChange={this.handleChange}
                placeholder="Enter amount of stock"
              />
            </FormGroup>
          </Form>
        </ModalBody>
        <ModalFooter>
          <Button
            color="success"
            onClick={this.triggerSetSellAmount}
          >
            Set Sell Amount
          </Button>
        </ModalFooter>
      </Modal>
    );
  }
}